import os
from shapely.geometry import shape
from groclient import GroClient


COUNTRY_ID=1065
REGION_LEVEL=5


def init_region_mapping(tables):
    client = GroClient('api.gro-intelligence.com', os.environ['GROAPI_TOKEN'])
    gro_regions = [r['id'] for r in client.get_descendant_regions(COUNTRY_ID, REGION_LEVEL)]
    region_mapping = {}
    for region in filter(lambda x: x, tables.keys()):
        for r in client.search('regions', region):
            if r['id'] in gro_regions:
                region_mapping[region] = r['id']
                break
        if region not in region_mapping:
            region_mapping[region] = None
    return region_mapping


def get_geometry(region_id):
    client = GroClient('api.gro-intelligence.com', os.environ['GROAPI_TOKEN'])
    geom = client.get_geojson(region_id)
    if not geom:
        return None
    return shape(geom['geometries'][0])
    
    
# region_mapping initialized as above and manually edited.
region_mapping = {
    'Addis_Ababa_Statistical-table_3.1': 10918,
    'AKAKI KALITI SUB CITY': None,
    'NEFAS SILK-LAFTO SUB CITY': None,
    'Addis_Ababa_Statistical-table_3.1?': None,
    'GULELE SUB CITY': None,
    'LIDETA SUB CITY': None,
    'Addis_Ababa_Statistical-table_3.1??': None,
    'ARADA SUB CITY': None,
    'ADDIS KETEMA SUB CITY': None,
    'Addis_Ababa_Statistical-table_3.1???': None,
    'BOLE SUB CITY': None,
#    'Affar_Statistical-table_3.1': 10919,
    'ZONE 1': 114954,
    'ZONE 2': 114955,
    'ZONE 3': 114956,
    'ZONE 4': 114957,
    'ZONE 5': 114958,
#    'Statistical_Amhara-table_3.1': 10920,
    'NORTH GONDAR ZONE': 114962,
    'SOUTH GONDAR ZONE': 114966,
    'NORTH WELLO ZONE': 114964,
    'SOUTH WELLO ZONE': 114967,
    'NORTH SHEWA ZONE': 114963,
    'EAST GOJJAM ZONE': 114961,
    'WEST GOJJAM ZONE': 114969,
    'WAGHEMIRA ZONE': 114968,
    'AWI-ZONE': 142801, #114959,    # ?
    'OROMIYA ZONE': 114965,
    'BAHIR DAR SPECIAL ZONE': 114960,
    'ARGOBA SPECIAL ZONE': 142802,
#    'Benishangu_Gumuz_Statistical-table_3.1': 10921,
    'METEKEL ZONE': 114972,
    'ASOSSA ZONE': 114970,
    'Benishangu_Gumuz_Statistical-table_3.1?': 114971,
    'PAWE SPECIAL WEREDA': None,
    'MAO KOMO SPECIAL WEREDA': None,
    'Dire_Dawa_Statistical-table_3.1': 10922,
#    'Gambella_Statistical-table_3.1': 10923,
    'AGNEWAK ZONE': 142804,
    'NUWER ZONE': 142803,
    'MEZHENGER ZONE': 142805,
    'ETANG SPECIAL WEREDA': 114974,    # ?
    'Harari_Statistical-table_3.1': 10924,
#    'Statistical_Oromiya-table_3.1': 10925,
    'WEST WELLEGA ZONE': 114988,
    'EAST WELLEGA ZONE': 114982,
    'ILU ABA BORA ZONE': 114983,
    'JIMMA ZONE': 114984,
    'WEST SHEWA ZONE': 114987,
    'NORTH SHEWA ZONE~': 114985,
    'EAST SHEWA ZONE': 114981,
    'ARSI ZONE': 114977,
    'WEST HARARGE ZONE': 114986,
    'EAST HARARGE ZONE': 114980,
    'BALE ZONE': 114978,
    'BORENA ZONE': 114979,
    'SOUTH WEST SHEWA ZONE': 142810,
    'GUJI ZONE': 142811,
    'ADAMA SPECIAL ZONE': None,
    'JIMMA SPECIAL ZONE': 114984,
    'WEST ARSI ZONE': 142809,
    'KELEM WELEGA ZONE': 142808,
    'HORO GUDRU WELEGA ZONE': 142807,
    'BURAYU SPECIAL ZONE': None,
#    'Statistical_SNNPR-table_3.1': 10927,
    'GURAGE ZONE': 115003,
    'HADIYA ZONE': 115004,
    'KEMBATA TIMBARO ZONE': 142820,
    'SIDAMA ZONE': 115010,
    'GEDEO ZONE': 115002,
    'WOLYITA ZONE': 115012,
    'SOUTH OMO ZONE': 115011,
    'SHEKA ZONE': 115009,
    'KEFFA ZONE': 115005,
    'GAMO GOFA ZONE': 115001,
    'BENCH MAJI ZONE': 114997,
    'YEM SPECIAL WEREDA': 115013,
    'AMARO SPECIAL WEREDA': 142823, # includes old 114995,
    'BURJI SPECIAL WEREDA': 142823, # includes old 114998,
    'KONSO SPECIAL WEREDA': 142823, # includes old 115007,
    'DERASHE SPECIAL WEREDA': 142823, # includes old 115000,
    'DAWURO ZONE': 114999,
    'BASKETO SPECIAL WEREDA': 114996,
    'KONTA SPECIAL WEREDA': 115008,
    'SILTI ZONE': 142821,
    'ALABA SPECIAL WEREDA': 142822,
    'Statistical_SNNPR-table_3.1?': 1000123,  # HAWASSA CITY ADMINISTRATION-ZONE
 #   'Somali_Statistical-table_3.1': 10926,
    'SHINILE ZONE': 142812, # 114992,     # ?
    'JIJIGA ZONE': 142813, # 114990,
    'DEGEHABUR ZONE': 142815, # 114989,
    'WARDER ZONE': 142816, #114994,      # ?
    'KORAHE ZONE': 142817,
    'FIK ZONE': 142814,
    'GODE ZONE': 142819, #1000136,     #?
    'AFDER ZONE': 142818,
    'LIBEN ZONE': 114991,
#    'Tigray_Statistical-table_3.1': 10928,
    'Tigray_Statistical-table_3.1?': 142825,
    'Tigray_Statistical-table_3.1??': 115014,
    'Tigray_Statistical-table_3.1???': 115015,
    'Tigray_Statistical-table_3.1????': 115017,
    'Tigray_Statistical-table_3.1?????': 115018,
    'Tigray_Statistical-table_3.1??????': 142824, # 115016, # 1000143,  # MEKELE SPECIAL ZONE
}


