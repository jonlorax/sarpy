# FlatfileImageWriter is a class describing a family of format-specific
# image writers.  It describes data that can be written to a "flat" file
# (continuous pixels stored in raster order on disk), possibly with some
# header and footer, where data is written with the MATLAB fwrite function.
#
# The FID property of this class assumes an fread/fwrite functionality.  If
# memory-mapped writing, or another library for writing is used, FID (and
# possibly a number of the other properties) would not be appropriate.
# In this case a more generic superclass (SARImageWriter) should be used.
#
# Derived classes should have a constructor that calls superclass
# constructor with appropriate values, opens file, writes header, etc. and
# a destructor that writes any footer info, closes file, etc.
# 
# Written by: Tom Krauss, NGA/IDT
# Converted to Python by: Tex Peterson, 2025-09
#
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////

import numpy
import os
import struct

from sarpy.io.complex.sicd_elements.SICD import SICDType
from sarpy.io.general.base import SarpyIOError

_unsupported_pix_size = 'Got unsupported sio data type/pixel size = `{}`'

class FlatfileImageReader(object):
    
    def __init__(
        # Input parameters that are required to define the structure of the
        # "flat" file to read.
        self,
        param_filename
    ):
        self._filename =  param_filename
        if not os.path.exists(os.path.dirname(self._filename)):
            raise SarpyIOError('Path {} is not a file'.format(self._filename))
        self._fid = open(self._filename, 'rb') # We always read big-endian
        self._magic_key      = self._fid.read(4)  #.hex()
        self._rows           = self._fid.read(4).from_bytes()
        self._columns        = self._fid.read(4).from_bytes()
        self._data_type_code = self._fid.read(4).from_bytes()
        self._data_size      = self._fid.read(4).from_bytes()
        match self._magic_key: ## Problem with case matching. hex() returns a string, leave as hex
            case 0xFF017FFE:
                # SIO file written as big endian without user data
                print('SIO file written as big endian without user data')
                self._user_data   = None
                self._image_data  = self._fid.read()
            case 0xFE7F01FF:
                # SIO file written as little endian without user data
                print('SIO file written as big endian without user data')
                self._user_data   = None
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = temp_image_data[::-1]
            case 0xFF027FFD: 
                # SIO file written as big endian with user data (sicd meta)
                print('SIO file written as big endian with user data')
                # Num pairs   (4 byte uint, # pairs of user data, fixed at 1)
                # Name bytes  (4 byte uint, # bytes in name of user element,
                #             fixed at 8 for name "SICDMETA")
                # Name        (8 bytes containing "SICDMETA")
                # Value bytes (4 byte uint, value is length of XML string)
                # Value       (XML string holding SICD metadata)
                num_pairs = self._fid.read(4)
                user_data_name_bytes = self._fid.read(4)
                self._user_data_name = self._fid.read(user_data_name_bytes)
                self._user_data_size  = self._fid.read(4)
                self._user_data    = self._fid.read(self._user_data_size)
                self._image_data  = self._fid.read()
            case 0xFD7F02FF:
                # SIO file written as little endian with user data (sicd meta)
                print('SIO file written as little endian with user data')
                # Num pairs   (4 byte uint, # pairs of user data, fixed at 1)
                # Name bytes  (4 byte uint, # bytes in name of user element,
                #             fixed at 8 for name "SICDMETA")
                # Name        (8 bytes containing "SICDMETA")
                # Value bytes (4 byte uint, value is length of XML string)
                # Value       (XML string holding SICD metadata)
                num_pairs = self._fid.read(4)
                user_data_name_bytes = self._fid.read(4)
                self._user_data_name = self._fid.read(user_data_name_bytes)
                self._user_data_size  = self._fid.read(4)
                self._user_data    = self._fid.read(self._user_data_size)
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = temp_image_data[::-1]


# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////