import locale
import logging
import re
import tabula
import pandas as pd


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # number style: commas for thousands
nameonly_pattern = re.compile("^[A-Za-z\-\s/']+$")  # names have -, / and space and ' in them
nannum_pattern = re.compile("-(\d+)")  # '-' followed by digits
nanend_pattern = re.compile("-$")  # '-' at the end
namenum_pattern = re.compile("([A-Za-z\-/']+)(\d+)")  # name followed by number
numnum_pattern = re.compile("(\d{3})([^,])")  # three digits not followed by comma
logger = logging.getLogger()


def parse_row(row, num_cols=10):
    """Parse:

    ["Foo", "3,723", "-"] -> ["Foo", 3723, 0]
    ["Foo", "3,7231,9481,7753,7231,9481,775"] -> ["Foo", 3723, 1948, 1775, 3723, 1948, 1775]
    ["Foo123", "456"] -> ["Foo", 123, 456]

    Note: if a number is less than three digits, and the next columns
    first chunk is also less than 3 digits, there's no single way to
    unglue them.  E.g. if we see "123,456" we will return [123456].
    but it could have been "12 3,456" or "1 23,456".
    """
    outrow = []
    for val in row:
        if pd.isna(val):
            continue
        # separate name and num columns that are stuck together
        s = namenum_pattern.sub("\g<1>\t\g<2>", val)
        # separate number columns that are stuck together
        s = numnum_pattern.sub("\g<1>\t\g<2>", s)
        s = nannum_pattern.sub("\t0\t\g<1>", s)
        s = nanend_pattern.sub("\t0", s)
        s = re.sub('\t+','\t', s).strip()
        for sn in s.split('\t'):
            try:
                outrow.append(locale.atoi(sn))
            except ValueError as e:
                if re.match(nameonly_pattern, sn):
                    outrow.append(sn)
                else:
                    raise e
    assert len(outrow) <= num_cols, "Too many values: {}->{}".format(list(row), outrow)
    if len(outrow) < num_cols and len(outrow)>1:
        outrow += ['']*(num_cols-len(outrow))
        outrow.append("Ambiguous 'glued' values. Before parsing: {}".format(list(row)))
    return outrow


def parse_file(fname):
    """Generate one df for each table in the file according to tabula.
    """
    for table in tabula.read_pdf(fname, pages="all", multiple_tables=True, pandas_options={'dtype': str}):
        table = table.apply(parse_row, axis=1).apply(pd.Series)
        yield table


def is_break(r):
    if re.match('^[A-Z\s]+$', r[0]):
        return True
    return False


def process_file(fname):
    # parse_file breaks tables on page breaks and doesn't recognize
    # the real breaks.  So we merge all the tables across pages into
    # one find the real breaks and separate tables.
    df = pd.concat([t for t in parse_file(fname)])
    df['break'] = df.apply(is_break, axis=1)
    rows = []
    tables = {'': []}
    for i, row in df.iterrows():
        if row['break'] == True:
            rows = tables.setdefault(row[0], [])
        else:
            rows.append(row)
    for name, rows in tables.items():
        tables[name] = pd.DataFrame(rows)
        if not tables[name].empty:
            tables[name].drop(columns=['break'], inplace=True)
            tables[name].set_index(0, inplace=True)

    return tables
