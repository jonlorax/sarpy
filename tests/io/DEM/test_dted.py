import pathlib

import pytest

import sarpy.io.DEM.DTED as sarpy_dted
from sarpy.io.DEM.geoid import GeoidHeight

import tests
# Note
# set this for your storage of dted and egm files
# export SARPY_TEST_PATH=<your dem stuff path>

test_data = tests.find_test_data_files(pathlib.Path(__file__).parent / "geoid.json")
egm96_file = test_data["geoid_files"][0] if test_data["geoid_files"] else None


@pytest.mark.skipif(egm96_file is None, reason="EGM 96 data does not exist")
def test_interpolator_no_readers():
    llb = [10.0, 20.0, 10.5, 20.5]
    geoid = GeoidHeight(egm96_file)
    dtedinterp = sarpy_dted.DTEDInterpolator([], geoid_file=geoid, lat_lon_box=llb)
    
    assert dtedinterp.get_max_geoid(llb) == 0
    assert dtedinterp.get_max_hae(llb) == geoid(10, 10.5)


@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_reader():
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][0])

    # From entity ID: SRTM3S04W061V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    known_values = {
        (1000, 800): -32767,  # null
        (1000, 799): 7,
        (3, 841): -5,
    }
    for index, expected_value in known_values.items():
        assert dted_reader[index] == expected_value

# no void tests
@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_reader_south_west_ignore_voids():
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][0]) # belive wants the s file
    print( "Testing Reader test using: {}".format( test_data["dted_with_null"][0] ))

    # From entity ID: SRTM3S04W061V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    # to follow along in qgis
    # qgis row = 1200 - known_value[ 1 ]   # dted1 data in 1200 blocks
    # qgis col =  known_value[ 0 ]

    # now with ignore_voids set
    # same as above but now with new expected values 
    # and notice  True in the dted_reader subscript call
    known_values = {
        (1000, 800):  0,  # ignore_voids -ed 
        (1000, 799):  7,     
        (3, 841):    -5,     
        (1004, 797):  7,     # a value among the voids displayed in qgis
    }
    for index, expected_value in known_values.items():
        assert dted_reader[(index, True)] == expected_value

@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_reader_north_west_ignore_voids():
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][1]) # belive wants the northern  file
    print( "Testing Reader test using: {}".format( test_data["dted_with_null"][1] ))

    # From entity ID: SRTM3N33W119V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    # to follow along in qgis
    # know_value is one of known_values index
    # qgis row = 1200 - known_value[ 1 ]   # dted1 data in 1200 blocks
    # qgis col =  known_value[ 0 ]
    known_values = {
        (812, 927):  0,  # null   zeroed by ignore_voids
        (813, 927):  0,  # null   zeroed by ignore_voids
        (811, 927):  79,     # a value among the voids displayed in qgi
        (813, 926):  110     # a value among the voids displayed in qgi
    }
    for index, expected_value in known_values.items():
        assert dted_reader[(index, True)] == expected_value

@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_interpolator_get_elevation_hae_north_west_ignore_voids():
    ll = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1]  #  '/sar/CuratedData_SomeDomestic/sarpy_test/dem/dted/n33_w119_3arc_v1.dt1
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll)
    print("_ignore_voids_ dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1], ignore_voids=True )))
    print("dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae(ll[0], ll[1])))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1], ignore_voids=True)  == pytest.approx( -36.490,   abs=0.01 )
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1] )                == pytest.approx( -32803.49, abs=0.01 )


@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_interpolator_get_elevation_hae_north_west_ignore_voids_default_on_void_data():
    ll = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1]  #  '/sar/CuratedData_SomeDomestic/sarpy_test/dem/dted/n33_w119_3arc_v1.dt1
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll)
    print("_ignore_voids_DEFAULT on a void  dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1] )))
    print("_ignore_voids         on a void  dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1], ignore_voids=True )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1]) == pytest.approx( -32803.4904, abs=0.01 )
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1], ignore_voids=True) == pytest.approx( -36.49, abs=0.01 )

def test_repair_values():
    import numpy as np
    
    # numpy math that repair_values with ignore_voids work is based on
    array1         = np.array([1, 4, 2, 6, 3, 65535])
    arrayCorrected = np.array([1, 4, 2, 6, 3, 0])
    # replaces value in place
    array1[ array1 == 65535] = 0
    assert np.array_equal( array1, arrayCorrected)

    array1      = np.array([1, 4, 2, 6, 3, 65535])
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][2])
    repaired    = dted_reader._repair_values( array1 )
    oldRepair   = np.array([1, 4, 2, 6, 3, -32767] ) # this is what repair_values does when not ignoring_voids, the user's concern
    assert np.array_equal( repaired , oldRepair  )
    
    repaired = dted_reader._repair_values( array1, True)
    assert np.array_equal( repaired , arrayCorrected )

    special_int = np.uint16( 100 )
    repaired    = dted_reader._repair_values( special_int, True)
    assert repaired, special_int
 
    special_int = np.uint16( 65535 )
    repaired = dted_reader._repair_values( special_int, True)
    assert np.equal(repaired, np.uint64( 0 ))  # to show values are the same, was getting np.uint64(0)

