import collections
import unittest

import numpy as np
import os

from sarpy.io.complex.converter import open_complex
from sarpy.processing.ortho_rectify import NearestNeighborMethod
from sarpy.processing.sidd.sidd_structure_creation import create_sidd_structure
from sarpy.processing.ortho_rectify.base import FullResolutionFetcher, OrthorectificationIterator
from sarpy.visualization import remap as remap

import sys 

# not ready for primetime
reader = open_complex('/sar/CuratedData_SomeDomestic/Domestic/Peregrine/Peregrine2020/Imagery/Peregrine2020_FARAD/Peregrine2020_FARAD_SICDF_SV/2020-07-30_f05/pass0004/20200730f02p0004faradx0500_709_11114HH.nitf' )
# create an orthorectification helper for specified sicd index
ortho_helper = NearestNeighborMethod(reader, index=0)

calculator = FullResolutionFetcher(
        ortho_helper.reader, dimension=0, index=ortho_helper.index, block_size=10)
ortho_iterator = OrthorectificationIterator(
        ortho_helper, calculator=calculator, bounds=None,
        remap_function=None, recalc_remap_globals=False)
# print( create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO8I', version=3, remap_function=None) )

class TestSiddProcessing(unittest.TestCase):
    def test_create_sidd_structure_v3_default_remap( self ):
        tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO8I', version=3 ) 
        assert tmpSidd.Display.PixelType ==  'MONO8I'
        assert tmpSidd.Display.NonInteractiveProcessing[0].ProductGenerationOptions.DataRemapping.LUTName == 'NRL'

    def test_create_sidd_structure_v3_density_remap( self ):
        tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO8I', version=3 , remap_function=remap.get_registered_remap( 'density' ) )
        # print( tmpSidd )
        assert tmpSidd.Display.PixelType ==  'MONO8I'
        assert tmpSidd.Display.NonInteractiveProcessing[0].ProductGenerationOptions.DataRemapping.LUTName == 'DENSITY'
    def test_create_sidd_structure_v3_default_remap_16( self ):
        tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO16I', version=3 ) 
        assert tmpSidd.Display.PixelType ==  'MONO16I'
        assert tmpSidd.Display.NonInteractiveProcessing[0].ProductGenerationOptions.DataRemapping.LUTName == 'NRL'

    def test_create_sidd_structure_v3_density_remap_16( self ):
        tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO16I', version=3 , remap_function=remap.get_registered_remap( 'density' ) )
        assert tmpSidd.Display.PixelType ==  'MONO16I'
        assert tmpSidd.Display.NonInteractiveProcessing[0].ProductGenerationOptions.DataRemapping.LUTName == 'DENSITY'

    def test_create_sidd_structure_v3_DEFAULT_remap_16( self ):
        tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO16I', version=3 , remap_function=remap.DEFAULT_REMAPPER )
        assert tmpSidd.Display.PixelType ==  'MONO16I'
        assert tmpSidd.Display.NonInteractiveProcessing[0].ProductGenerationOptions.DataRemapping.LUTName == 'NRL'

    def test_create_sidd_structure_v3_None_remap_16( self ):
        with self.assertRaises(AttributeError):  # remaper.name dont fly
            tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO16I', version=3 , remap_function=None )

    def test_create_sidd_structure_v3_string_remap_16( self ):
        with self.assertRaises(AttributeError):  # remaper.name dont fly when None
            tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image', pixel_type='MONO16I', version=3 , remap_function='bad robot' )
          
    def test_create_sidd_structure_v3_DEFAULT_remap_25( self ):
        with self.assertRaises(ValueError):  # mono 25  dont fly
            tmpSidd = create_sidd_structure(ortho_helper, bounds=ortho_iterator.ortho_bounds, product_class='Detected Image',  pixel_type='MONO25I', version=3 , remap_function=remap.DEFAULT_REMAPPER )

