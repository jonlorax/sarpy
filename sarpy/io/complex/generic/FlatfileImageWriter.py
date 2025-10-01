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
# Written by: Tex Peterson, 2025-09
# Derived from MATLAB_SAR, Tom Krauss, NGA/IDT
# 
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

class FlatfileImageWriter(object):
    
    def __init__(
        # Input parameters that are required to define the structure of the
        # "flat" file to write.
        self,
        param_filename, 
        param_sicdmeta, 
        # Number of bytes to skip before writing data
        param_header_skip:       int = 20,        
        # numpy data types. "uint8", "float32", etc.
        param_data_type_str:     str = 'complex64', 
        param_data_type_code:    int = 13,
        param_is_complex:        bool = True,         # Boolean
        # Derived parameters computed for ease of use
        # Size of image in columns, rows (2-vector), derived from sicdmeta NumCols, NumRows
        param_image_size:        list = [],        
        param_data_size:         int = 100,            # Size of image data in bytes
        # Data class of DATA_TYPE (so 'float32' becomes 'single'...)
        param_buffer_type:       str = 'complex64',
    ):
        self._filename       =  param_filename
        self._sicdmeta       = param_sicdmeta
        self._header_skip    = param_header_skip
        self._data_type_str  = param_data_type_str
        self._data_type_code = param_data_type_code
        self._is_complex     = param_is_complex
        self._image_size     = [x + self._header_skip for x in param_image_size]
        self._data_size      = param_data_size
        self._buffer_type    = param_buffer_type
        
        if not os.path.exists(os.path.dirname(self._filename)):
            raise SarpyIOError('Path {} is not a file'.format(self._filename))
        self._fid = open(self._filename, 'wb') # We always write big-endian
        # Derived properties
        # SICDMETA must have, at a minimum, the number of rows and columns
        if isinstance(self._sicdmeta, SICDType):
            self._image_size = [self._header_skip + 
                                self._sicdmeta.ImageData.NumCols, 
                                self._header_skip + 
                                self._sicdmeta.ImageData.NumRows]
            if self._sicdmeta.ImageData is not None:
                if self._sicdmeta.ImageData.PixelType == 'RE16I_IM16I':
                    self._data_type_str = 'int16'
                elif self._sicdmeta.ImageData.PixelType == 'RE32F_IM32F':
                    self._data_type_str = 'float32'
                elif self._sicdmeta.ImageData.PixelType == 'AMP8I_PHS8I':
                    self._data_type_str = 'uint8'
                else :
                    raise ValueError(_unsupported_pix_size.format(self._sicdmeta.ImageData.PixelType))
        
    # Generic data chip writing routine.  Use this to write chips to an
    # already-opened file.  Note that the file is opened with a call to
    # the (abstract) open function.  The file handle is then stored with
    # the object so it doesn't get passed around with this routine.
    def write_chip(self, param_data, param_start_indices = [0, 0]):
        # WRITE_CHIP Writes the given data into the already-opened file.
        #
        # Note this is a member function of FlatfileImageWriter class and hence
        # must be called in the context of an FlatfileImageWriter object.
        #
        # Inputs:
        #       self:              This is the 'hidden' object-specific handle.  
        #       data:              The matrix of data to be written
        #       start_indices:     1x2 vector ([start_column_index, start_row_index])
        #                          giving starting (upper-left-hand) position of
        #                          the chip to write in the entire file. (Note:
        #                          Definition of "column" and "row" assumes file
        #                          is written row-major order.)
        #
        # Outputs:
        #       num_bytes_written: The number of bytes written to the file
        #                          associated with the object.
        #
        #
        # Written by: Tom Krauss and Wade Schwartzkopf, NGA/IDT
        # # Converted to Python by: Tex Peterson, 2025-09

        ## Error checking
        if (any(x < 0 for x in param_start_indices) or 
            any(
                (param_start_indices[y] + len(param_data) - 1) > self._image_size[y] for y in [0, 1])
                ) :
            raise ValueError('FLATFILEIMAGEWRITER_WRITE_CHIP:InvalidSizePosition Chip cannot be written outside predefined size of image in file.')

        ## Python doesn't write complex numbers directly, so we have to use struct
        if not isinstance(param_data, numpy.ndarray):
            raise TypeError('param_data must be a numpy array')
        data_interleaved = param_data.tobytes()
        
        ## Need to seek to the correct location in the file before writing. 
        # Number of bytes for each pixel
        element_size = self._data_size * (self._is_complex + 1) 
        # Number of bytes to skip between each row
        row_skip = element_size * (self._image_size[0] - len(param_data)); 
        offset = (
            self._header_skip +  # Start of data in file
            ((element_size * param_start_indices[1]) * 
             self._image_size[0]) +  # First row
            (element_size * param_start_indices[0])
            ) # First column

        ## We might need to write the first line in the file separately.  MATLAB's
        # fwrite skips first and THEN writes, so we might not be able to set the
        # file pointer to a position where it can skip and then write without
        # having a negative position with respect to the beginning of the file.
        if (offset - row_skip) < 0 :
            # move offset bytes from the beginning of the file.
            print('offset: ' + str(offset))
            self._fid.seek(offset) 
            num_bytes_written = self._data_size * self._fid.write(param_data)
        else:
            num_bytes_written = 0
        self._fid.flush
        return num_bytes_written
    
    def close(self):
        self._fid.close()

# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////