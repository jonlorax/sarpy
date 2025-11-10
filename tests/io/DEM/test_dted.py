import pathlib

import pytest

import sarpy.io.DEM.DTED as sarpy_dted
from sarpy.io.DEM.geoid import GeoidHeight

import tests


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
def test_dted_reader_south_west_no_voids():
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][0]) # belive wants the s file
    print( "Testing Reader test using: {}".format( test_data["dted_with_null"][0] ))

    # From entity ID: SRTM3S04W061V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    # to follow along in qgis
    # qgis row = 1200 - known_value[ 1 ]   # dted1 data in 1200 blocks
    # qgis col =  known_value[ 0 ]

    # now with no_voids set
    # same as above but now with new expected values
    known_values = {
        (1000, 800):  0,  # no_voids -ed 
        (1000, 799):  7,     
        (3, 841):    -5,     
        (1004, 797):  7,     # a value among the voids displayed in qgis
    }
    for index, expected_value in known_values.items():
        assert dted_reader[(index, True)] == expected_value

@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_reader_north_west_no_voids():
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][1]) # belive wants the northern  file
    print( "Testing Reader test using: {}".format( test_data["dted_with_null"][1] ))

    # From entity ID: SRTM3N33W119V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    # to follow along in qgis
    # know_value is one of known_values index
    # qgis row = 1200 - known_value[ 1 ]   # dted1 data in 1200 blocks
    # qgis col =  known_value[ 0 ]
    known_values = {
        (812, 927):  0,  # null   zeroed by no_voids
        (813, 927):  0,  # null   zeroed by no_voids
        (811, 927):  79,     # a value among the voids displayed in qgi
        (813, 926):  110     # a value among the voids displayed in qgi
    }
    for index, expected_value in known_values.items():
        assert dted_reader[(index, True)] == expected_value

@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_interpolator_get_elevation_hae_north_west_no_voids():
    ll = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1]  #  '/sar/CuratedData_SomeDomestic/sarpy_test/dem/dted/n33_w119_3arc_v1.dt1
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll)
    print("_no_voids_ dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1], no_voids=True )))
    print("dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae(ll[0], ll[1])))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1], no_voids=True)  == pytest.approx( -36.490,   abs=0.01 )
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1] )                == pytest.approx( -32803.49, abs=0.01 )


@pytest.mark.skipif(not test_data["dted_with_null"], reason="DTED with null data does not exist")
def test_dted_interpolator_get_elevation_hae_north_west_no_voids_default_on_void_data():
    ll = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1]  #  '/sar/CuratedData_SomeDomestic/sarpy_test/dem/dted/n33_w119_3arc_v1.dt1
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll)
    print("_no_voids_DEFAULT on a void  dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1] )))
    print("_no_voids         on a void  dted interpolator northen test  ll: {}  elevation HAE : {}".format( ll,  dem_interpolator.get_elevation_hae( ll[0], ll[1], no_voids=True )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1]) == pytest.approx( -32803.4904, abs=0.01 )
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1], no_voids=True) == pytest.approx( -36.49, abs=0.01 )

