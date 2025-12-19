import pathlib
 
import pytest
 
import sarpy.io.DEM.DTED as sarpy_dted
from sarpy.io.DEM.geoid import GeoidHeight
 
import tests
# Note
# set this for your storage of dted and egm files
# export SARPY_TEST_PATH=<your dem stuff path>
 
# test_data = tests.find_test_data_files(pathlib.Path(__file__).parent / "geoid.json")
test_data = tests.find_test_data_files( "tests/io/DEM/geoid.json")
print( "test_data: {}".format( test_data ))
egm96_file = test_data["geoid_files"][0] if test_data["geoid_files"] else None
 
 
 
print( "above test_dted_reader")
if 1:
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][0])
 
    # From entity ID: SRTM3S04W061V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    known_values = {
        (1000, 800): -32767,  # null
        (1000, 799): 7,
        (3, 841): -5,
    }
    for index, expected_value in known_values.items():
        print( "index: {}  value: {}  expected Value: {}".format( index, dted_reader[ index ], expected_value ))
 
    #  
    # now with the ignore_voids variable set to true, run same test  show correct resutls for void, positive and negative values
    dted_reader = sarpy_dted.DTEDReader(test_data["dted_with_null"][0], True)
 
    # From entity ID: SRTM3S04W061V1, date updated: 2013-04-17T12:16:47-05
    # Acquired from https://earthexplorer.usgs.gov/ on 2024-08-21
    known_values = {
        (1000, 800): 0, # void value 0-ed out
        (1000, 799): 7,
        (3, 841): -5,
    }  
    for index, expected_value in known_values.items():
        print( "index: {}  value: {}  expected Value: {}".format( index, dted_reader[ index ], expected_value ))
 
 
    #  
    # showing change with DTEDInterpolator, where
 
    ll = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1] 
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll)
    print( "old : dem_interpolator.get_elevation_hae  {}  expected -32803.49".format(  dem_interpolator.get_elevation_hae(ll[0], ll[1] )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1] )                == pytest.approx( -32803.49, abs=0.01 )
 
    dem_interpolator = sarpy_dted.DTEDInterpolator(files=files, geoid_file=geoid, lat_lon_box=ll, ignore_voids=True)
    print( "NEW : dem_interpolator.get_elevation_hae  {}  expected -36.490".format(  dem_interpolator.get_elevation_hae(ll[0], ll[1] )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1])  == pytest.approx( -36.490,   abs=0.01 )
 
 
    #
    # DTEDInterpolator had another constructor that was a little different, from_coords_and_list
    #
    # lat long box
    # The bounding box of the form `[lat min, lat max, lon min, lon max]`
    lat_lon_box = [ 33.3174, 33.8174,  -118.36258, -118.000 ]  # catinlia island off California coast VOID cell
    ll          = [ 33.3174, -118.36258 ]  # catinlia island off California coast VOID cell
    geoid = GeoidHeight(egm96_file)
    files = test_data["dted_with_null"][1]
    dted_root_dir = '/sar/CuratedData_SomeDomestic/sarpy_test/dem/' # dir above dted
    tmplist          = sarpy_dted.DTEDList( dted_root_dir)
    dem_interpolator = sarpy_dted.DTEDInterpolator.from_coords_and_list( lat_lon_box, tmplist, geoid_file=geoid)
    print( "old : dem_interpolator.from_coords_and_list  {}  expected -32803.49".format(  dem_interpolator.get_elevation_hae(ll[0], ll[1] )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1]) == pytest.approx( -32803.4904, abs=0.01 )
 
    dem_interpolator = sarpy_dted.DTEDInterpolator.from_coords_and_list( lat_lon_box, tmplist, geoid_file=geoid, ignore_voids=True)
    print( "_NEW_ : dem_interpolator.from_coords_and_list  {}  expected -36.49".format(  dem_interpolator.get_elevation_hae(ll[0], ll[1] )))
    assert dem_interpolator.get_elevation_hae(ll[0], ll[1]) == pytest.approx( -36.49, abs=0.01 ) # ignore_voids value
