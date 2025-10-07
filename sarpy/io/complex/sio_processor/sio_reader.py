# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////
# 
# Written by: Tex Peterson, 
# Written on: 2025-10
#

import numpy
import os

from sarpy.io.complex.sicd_elements.SICD import SICDType
from sarpy.io.general.base import SarpyIOError

class SIOReader(object):
    """
    A class for reading SICD data from the Stream-oriented Input Output (SIO) format.

    SIO files have a 20 byte header, possibly followed by the SICD meta data in 
    the user data section, followed by the image data.

    Example:
    # Given an SIO file.
    # Within an interactive Python shell

    from sarpy.io.complex.sio_processor.sio_reader import SIOReader as SIOReader

    input_sio_file = "SIOReaderExampleOutput.sio"

    my_sio_reader = SIOReader(str(input_sio_file))

    """

    def __init__(
        self,
        param_filename
    ):
        """
        Parameters:

        param_filename:
            The path and filename to read the data from.

        Returns:
        An SIOReader object.

        """
        self._filename =  param_filename
        if not os.path.exists(os.path.dirname(self._filename)):
            raise SarpyIOError('Path {} is not a file'.format(self._filename))
        # We always open the file as big-endian because the header is always 
        # big-endian
        self._fid = open(self._filename, 'rb') 
        self._magic_key      = int.from_bytes(self._fid.read(4))
        self._rows           = int.from_bytes(self._fid.read(4))
        self._columns        = int.from_bytes(self._fid.read(4))
        self._data_type_code = int.from_bytes(self._fid.read(4))
        # Set the data type and size from the code in the header.
        self._sio_code_to_numpy_data_type()
        self._data_size      = int.from_bytes(self._fid.read(4))
        match self._magic_key: 
            case 0xFF017FFE:
                # SIO file written as big endian without user data
                print('Reading an SIO file written as big endian without user data')
                self._user_data   = None
                self._image_data  = numpy.frombuffer(self._fid.read(), 
                                                     dtype=self._data_type_str
                                                     ).reshape(self._rows, 
                                                                 self._columns,
                                                                 2)
            case 0xFE7F01FF:
                # SIO file written as little endian without user data
                print('Reading an SIO file written as little endian without user data')
                self._user_data   = None
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = numpy.frombuffer(temp_image_data[::-1], 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)
            case 0xFF027FFD: 
                # SIO file written as big endian with user data (sicd meta)
                print('Reading an SIO file written as big endian with user data')
                # SICD meta data header format:
                # Num pairs   (4 byte uint, # pairs of user data, fixed at 1)
                # Name bytes  (4 byte uint, # bytes in name of user element,
                #             fixed at 8 for name "SICDMETA")
                # Name        (8 bytes containing "SICDMETA")
                # Value bytes (4 byte uint, value is length of XML string)
                # Value       (XML string holding SICD metadata)
                self._num_pairs = int.from_bytes(self._fid.read(4))
                user_data_name_bytes = int.from_bytes(self._fid.read(4))
                self._user_data_name = self._fid.read(user_data_name_bytes).decode("utf-8")
                self._user_data_size  = int.from_bytes(self._fid.read(4))
                self._user_data    = self._fid.read(self._user_data_size).decode("utf-8")
                self._sicdmeta = SICDType.from_xml_string(self._user_data)
                self._image_data  = numpy.frombuffer(self._fid.read(), 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)
            case 0xFD7F02FF:
                # SIO file written as little endian with user data (sicd meta)
                print('Reading an SIO file written as little endian with user data')
                # SICD meta data header format:
                # Num pairs   (4 byte uint, # pairs of user data, fixed at 1)
                # Name bytes  (4 byte uint, # bytes in name of user element,
                #             fixed at 8 for name "SICDMETA")
                # Name        (8 bytes containing "SICDMETA")
                # Value bytes (4 byte uint, value is length of XML string)
                # Value       (XML string holding SICD metadata)
                self._num_pairs = int.from_bytes(self._fid.read(4))
                user_data_name_bytes = int.from_bytes(self._fid.read(4))
                self._user_data_name = self._fid.read(user_data_name_bytes).decode("utf-8")
                self._user_data_size  = int.from_bytes(self._fid.read(4))
                self._user_data    = self._fid.read(self._user_data_size).decode("utf-8")
                self._sicdmeta = SICDType.from_xml_string(self._user_data)
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = numpy.frombuffer(temp_image_data[::-1], 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)

    def _sio_code_to_numpy_data_type(self):
        """
        Private function: Given the data type code from the header, set the numpy data type and size.
        """
        match self._data_type_code:
            case 1:
                self._data_type_str = 'int16'
                self._data_size = 2
            case 3:
                self._data_type_str = 'float32'
                self._data_size = 8
            case 13:
                self._data_type_str = 'complex64'
                self._data_size = 16
            case _ : #Default if other cases don't match
                raise TypeError('Writer only recognizes floats, complex and signed or unsigned integers')        
    
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////