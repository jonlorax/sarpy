# SIOWriter is a class for writing SICD files using an SIO format.
# The SICD metadata is written in a user data field called "SICDMETA" in the 
# standard SIO file format. The caller can also turn off the user data, since 
# not all SIO readers handle this.
#
# Written by: Tex Peterson
# Written on: 2025-10
#
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////

import numpy
import os

from sarpy.io.complex.sicd_elements.SICD import SICDType
from sarpy.io.general.base import SarpyIOError

class SIOWriter(object):
    
    def __init__(
            self,
            param_filename:              str, 
            param_image_data:            numpy.array, 
            param_sicdmeta:              SICDType|None = None,
            param_start_indices:         list = [0, 0],
            param_include_sicd_metadata: bool = True       # Boolean
    ):
        # Parse inputs
        self._filename       = param_filename
        self._image_data     = param_image_data
        if param_sicdmeta is not None:
            self._sicdmeta   = param_sicdmeta.to_xml_bytes()
        self._start_indices  = param_start_indices
        self._include_sicd_metadata = param_include_sicd_metadata
        
        self._header_skip = 5*4 # SIO header with no user data is 5 uint32 words

        # Magic key
        # We always write big-endian
        if self._sicdmeta is not None and self._include_sicd_metadata:
            self._header_skip = self._header_skip + 4 + 4 + 8 + 4 + \
                len(self._sicdmeta) # Add user data length
            self._magic_key = 0xFF027FFD # Indicates big endian, with user-data
        else:
            self._magic_key = 0xFF017FFE # Indicates big endian, with no user-data
        self._image_shape    = self._image_data.shape
        
        # Data type and size
        self.numpy_data_type_to_sio()
        
        if not os.path.exists(os.path.dirname(self._filename)):
            raise SarpyIOError('Path {} is not a file'.format(self._filename))
        self._fid = open(self._filename, 'wb')
        
    
    def numpy_data_type_to_sio(self):
        match self._image_data.dtype:
            case 'int16':
                self._data_type_code = 1
                self._data_size = 2
            case 'float32':
                self._data_type_code = 3
                self._data_size = 8
            case 'complex64':
                self._data_type_code = 13
                self._data_size = 16
            case _ : #Default if other cases don't match
                raise TypeError('Writer only recognizes floats, complex and signed or unsigned integers')
                
    def write(self):
        # We'll use a fixed definition SIO header with (possibly) one user-data segment.
        # The header will the look like this:
        #    Core SIO header:
        #       Magic key   (4 byte uint, fixed value of 'FF027FFD')
        #       Rows        (4 byte uint)
        #       Columns     (4 byte uint)
        #       Data type   (4 byte uint)
        #       Data size   (4 byte uint, # bytes per element)
        #    Optional "user data":
        #       Num pairs   (4 byte uint, # pairs of user data, fixed at 1)
        #       Name bytes  (4 byte uint, # bytes in name of user element,
        #                    fixed at 8 for name "SICDMETA")
        #       Name        (8 bytes containing "SICDMETA")
        #       Value bytes (4 byte uint, value is length of XML string)
        #       Value       (XML string holding SICD metadata)
        

        self._fid.write(self._magic_key.to_bytes(4))
        # Rows and columns
        self._fid.write(self._image_shape[0].to_bytes(4))
        self._fid.write(self._image_shape[1].to_bytes(4))
        self._fid.write(self._data_type_code.to_bytes(4))
        self._fid.write(self._data_size.to_bytes(4))
        # User data
        if self._sicdmeta is not None and self._include_sicd_metadata:
            # Num pairs of user data, always 1 because we only write 1 SICD at a time.
            self._fid.write((1).to_bytes(4))                  
            self._fid.write((8).to_bytes(4))                 # Name length
            self._fid.write('SICDMETA'.encode('utf-8'))      # Always SICDMEATA
            self._fid.write(len(self._sicdmeta).to_bytes(4)) 
            self._fid.write(self._sicdmeta.encode('utf-8'))  

        num_bytes_written = self._fid.write(self._image_data)
        return num_bytes_written
    
    def close(self):
        self._fid.close()

# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////