__classification__ = "UNCLASSIFIED"
__author__ = "Tex Peterson"
# Written on: 2025-10
#

import numpy, os, pytest, re
from unittest import TestCase

from sarpy.io.complex.sicd_elements.blocks     import RowColType
from sarpy.io.complex.sicd_elements.ImageData  import ImageDataType, FullImageType
from sarpy.io.complex.sicd_elements.SICD       import SICDType
from sarpy.io.complex.sio_processor.sio_writer import SIOWriter as SIOWriter

class test_sio_writer(TestCase):
    def setUp(self):
        print('no repeateable setup')

    def test_create_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, 
                                    re.escape(
                                        "SIOWriter.__init__() missing 2 required positional arguments")):
            sio_writer = SIOWriter()