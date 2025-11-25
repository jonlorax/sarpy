import pathlib

import pytest

# python -m pytest tests\utils\test_dted_void_work.py

from sarpy.utils.dted_check_voids import check_for_voids

import sarpy.io.DEM.DTED as sarpy_dted

import tests
# Note
# export SARPY_TEST_PATH='/sar/CuratedData_SomeDomestic/sarpy_test/'

test_data = tests.find_test_data_files(pathlib.Path(__file__).parent / "geoid.json")


# @pytest.mark.skipif(egm96_file is None, reason="EGM 96 data does not exist")
def test_check_for_voids_by_list_of_files_true():
    # debug scratch
    import pdb
    import json
    # pdb.set_trace()
    platform_tests = {}
    parent_path    = os.environ.get('SARPY_TEST_PATH', None)
    test_data      = tests.find_test_data_files(pathlib.Path(__file__).parent / "geoid.json")
    print( "parent_path: {}".format( parent_path))
    if parent_path is not None and not os.path.isdir(parent_path):
        raise IOError('SARPY_TEST_PATH is given as {}, but is not a directory'.format(parent_path))
    if sys.platform.startswith('win'): # Windows
        # more hack testint
        myTestData = json.load( open( 'C:\\src\\python\\git\\gitHub\\jonlorax\\sarpy\\tests\\utils\\geoid.json', 'r'))
        print( "___myTestData: {}".format( json.dumps( myTestData, indent=2  )))
        print( " test * list os.join:{}".format( myTestData['xplatform_dted_with_null'][0]['predirs'] ) )
        print( " test * list os.join:{}".format( os.path.join(parent_path, *myTestData['xplatform_dted_with_null'][0]['predirs'], myTestData['xplatform_dted_with_null'][0]['path'] ) )) # works
        ## __WORKS__   predirs, path  This needs to go into __init__.py
        with open( os.path.join(parent_path, *myTestData['xplatform_dted_with_null'][0]['predirs'], myTestData['xplatform_dted_with_null'][0]['path'] ) ) as f:  ###  __WORKS__
            print( f)
        
        # this worked but moving this code to __init__
        # platform_tests["windows_specific_test"] = os.path.join(parent_path, test_data['xplatform_dted_with_null'][0]['predirs'] )
        # print( "platform_test: {}".format( platform_tests))
        
        print( "test_data:".format( test_data ))
    # end debug Xplatofrmm scrath
    
    print( "OS list of files: {}".format( check_for_voids( [ "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n33_w119_3arc_v1.dt1" , "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1" ])))  
    ## __NEED__ this format
    print( "__test_data: {}".format( json.dumps(test_data, indent=2 )))
    # test_data["dted_with_null"][1], test_data["dted_with_null"][4]
    print( "trying testData work: {}".format ( test_data["xplatform_dted_with_null"][1]))
   #  print( "tyring testData work: {}".format ( test_data["dted_with_null"][1]))
    quickCheck = check_for_voids( [ test_data["xplatform_dted_with_null"][1], test_data["xplatform_dted_with_null"][4] ] )
    print( "quickCheck: {}".format( json.dumps( quickCheck, indent=2 )))
    # quickCheck  = check_for_voids( [ "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n33_w119_3arc_v1.dt1" , "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1" ])
    
    quickAnswer = {
  "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n33_w119_3arc_v1.dt1": "True",
  "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1": "True"
}
    assert quickCheck == quickAnswer


def test_check_for_voids_by_dir_true():
    quickCheck = check_for_voids(   "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\"  )
    quickAnswer = {"c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n27_e084_3arc_v1.dt1": 'True', "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n33_w119_3arc_v1.dt1": 'True', "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s01_w070_3arc_v1.dt1": 'True', "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s04_w061_3arc_v1.dt1": 'True', "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1": 'True'}
    assert quickCheck == quickAnswer


def test_check_for_voids_by_file_true():
    response = check_for_voids(   "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1")
    answer = { "c:\\Users\\JohnO\'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1": "True"}
    assert response == answer

    fullResponse = check_for_voids( "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1", True)
    fullAnswer   = {"c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\s36_e149_3arc_v1.dt1": {'indices': [(96, 97, 97, 97, 98, 98, 98, 99, 183, 183, 547, 547, 548, 548, 549, 549, 823, 823, 823, 1103, 1103, 1122, 1122, 1122, 1125, 1125, 1125, 1173, 1173, 1174), (657, 657, 658, 659, 657, 658, 659, 658, 224, 225, 653, 654, 653, 654, 653, 654, 45, 46, 47, 412, 413, 463, 464, 465, 463, 464, 465, 1126, 1127, 1127)], 'has_voids': 'True'}}
    assert fullResponse == fullAnswer

# @pytest.mark.skipif(egm96_file is None, reason="EGM 96 data does not exist")
def test_check_for_voids_by_file_false():
    # check_for_voids(   "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\"  )
    quickCheck = check_for_voids(   "c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n38_w078_3arc_v2.dt1"  )
    #print( quickCheck)
    quickAnswer = {"c:\\Users\\JohnO'Neill\\Downloads\\dem\\dted\\n38_w078_3arc_v2.dt1": 'False'}
    assert quickCheck == quickAnswer    
