# SIOWriter is a class for writing SICD files using an SIO format.
# The SICD metadata is written in a user data field called "SICDMETA" in the 
# standard SIO file format.
# 
# Written by: Tex Peterson, 
# Written on: 2025-10
#
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////

from xml.etree import ElementTree
import numpy
import os
import struct

from sarpy.io.complex.sicd_elements.SICD import SICDType
from sarpy.io.general.base import SarpyIOError
from sarpy.io.complex.sicd_elements.SICD import _SICD_SPEC_DETAILS, \
    _SICD_VERSION_DEFAULT
from sarpy.io.complex.sicd_elements.ImageData import ImageDataType, FullImageType
from sarpy.io.complex.sicd_elements.blocks import RowColType

class SIOReader(object):
    
    def __init__(
        self,
        param_filename
    ):
        self._filename =  param_filename
        if not os.path.exists(os.path.dirname(self._filename)):
            raise SarpyIOError('Path {} is not a file'.format(self._filename))
        self._fid = open(self._filename, 'rb') # We always read big-endian
        self._magic_key      = int.from_bytes(self._fid.read(4))
        self._rows           = int.from_bytes(self._fid.read(4))
        self._columns        = int.from_bytes(self._fid.read(4))
        self._data_type_code = int.from_bytes(self._fid.read(4))
        self.sio_code_to_numpy_data_type()
        self._data_size      = int.from_bytes(self._fid.read(4))
        match self._magic_key: ## Problem with case matching. hex() returns a string, leave as hex
            case 0xFF017FFE:
                # SIO file written as big endian without user data
                print('SIO file written as big endian without user data')
                self._user_data   = None
                self._image_data  = numpy.frombuffer(self._fid.read(), 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)
            case 0xFE7F01FF:
                # SIO file written as little endian without user data
                print('SIO file written as big endian without user data')
                self._user_data   = None
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = numpy.frombuffer(temp_image_data[::-1], 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)
            case 0xFF027FFD: 
                # SIO file written as big endian with user data (sicd meta)
                print('SIO file written as big endian with user data')
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
                self._user_data_xml = ElementTree.fromstring(self._user_data)
                self.sio_user_data_to_sarpy_format()
                self._image_data  = numpy.frombuffer(self._fid.read(), 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)
            case 0xFD7F02FF:
                # SIO file written as little endian with user data (sicd meta)
                print('SIO file written as little endian with user data')
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
                self._user_data_xml = ElementTree.fromstring(self._user_data)
                self.sio_user_data_to_sarpy_format()
                temp_image_data   = self._fid.read()
                # Reverse the bytes ingested from little endian to big
                self._image_data  = numpy.frombuffer(temp_image_data[::-1], 
                                                     dtype=self._data_type_str).reshape(self._rows, self._columns,2)

    def sio_code_to_numpy_data_type(self):
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
            
    def sio_user_data_to_sarpy_format(self):
        if ((self._user_data_xml.tag[-4:] == 'SICD') or 
            (self._user_data_xml.tag[-8:] == 'SICDMETA') or 
            (self._user_data_xml.tag[-9:] == 'SICD_META')):
            self.sio_user_data_to_sicd_format_current_version()
        elif self._user_data_xml.tag[-4:] == 'CPHD':
            self.sio_user_data_to_cphd_format()

    def sio_user_data_to_sicd_format_generic_version(self):
        # Initialize variables that will be set later.
        meta_data_number = 0
        NumRows = 0
        NumCols=0
        PixelType=0
        FirstRow=0
        FirstCol=0
        NumRows=0
        NumCols=0
        FullImageNumRows = 0 
        FullImageNumCols = 0
        SCPPixelRow=0
        SCPPixelCol=0
        FullImage = False
        # Process each  
        for elem in self._user_data_xml.iter():
            if elem.tag[-4:] == 'SICD':
                print(_SICD_SPEC_DETAILS[_SICD_VERSION_DEFAULT]['namespace'] + '}SICD')
                if meta_data_number > 0: # We only process the first SICD meta data
                    break
                else:
                    meta_data_number += 1
            elif elem.tag[-9:] == 'ImageData':
                print(_SICD_SPEC_DETAILS[_SICD_VERSION_DEFAULT]['namespace'] + '}ImageData')
            elif elem.tag[-9:] == 'PixelType':
                PixelType = elem.text
            elif elem.tag[-7:] == 'NumRows':
                if FullImage:
                    FullImageNumRows = elem.text
                else:
                    NumRows = elem.text
            elif elem.tag[-7:] == 'NumCols':
                if FullImage:
                    FullImageNumCols = elem.text
                    FullImage = False
                else:
                    NumCols = elem.text
            elif elem.tag[-8:] == 'FirstRow':
                FirstRow = elem.text
            elif elem.tag[-8:] == 'FirstCol':
                FirstCol = elem.text
            elif elem.tag[-9:] == 'FullImage':
                FullImage = True
            elif elem.tag[-8:] == 'SCPPixel':
                SCPPixel = True
            elif elem.tag[-3:] == 'Row':
                if SCPPixel:
                    SCPPixelRow = elem.text
            elif elem.tag[-3:] == 'Col':
                if SCPPixel:
                    SCPPixelCol = int(elem.text)
            else:
                print('break: ' + elem.tag)
        localImageData=ImageDataType(
        	NumRows=NumRows,
            NumCols=NumCols,
            PixelType=PixelType,
            FirstRow=FirstRow,
            FirstCol=FirstCol,
            FullImage=FullImageType(
                NumRows=FullImageNumRows,
                NumCols=FullImageNumCols
            ),
            SCPPixel=RowColType(Row=SCPPixelRow , Col=SCPPixelCol)
        )
        self._sicdmeta = SICDType(ImageData=localImageData)
        
    def sio_user_data_to_sicd_format_current_version(self):
        print('current version')
        # Initialize variables that will be set later.
        meta_data_number = 0
        NumRows = 0
        NumCols=0
        PixelType=0
        FirstRow=0
        FirstCol=0
        NumRows=0
        NumCols=0
        FullImageNumRows = 0 
        FullImageNumCols = 0
        SCPPixelRow=0
        SCPPixelCol=0
        # Define the Uniform Resource Names (URN)
        urn = '{' + _SICD_SPEC_DETAILS[_SICD_VERSION_DEFAULT]['namespace'] + '}'
        for image_data in self._user_data_xml.findall(urn+'ImageData'):
            for xml_element in image_data:
                if xml_element.tag == urn+'PixelType':
                    PixelType = xml_element.text
                elif xml_element.tag == urn+'NumRows':
                    NumRows = xml_element.text                    
                elif xml_element.tag == urn+'NumCols':
                    NumCols = xml_element.text
                elif xml_element.tag == urn+'FirstRow':
                    FirstRow = xml_element.text
                elif xml_element.tag == urn+'FirstCol':
                    FirstCol = xml_element.text
                elif xml_element.tag == urn+'FullImage':
                    for sub_element in xml_element:
                        if sub_element == urn+'NumRows':
                            FullImageNumRows = sub_element.text
                        elif sub_element == urn+'NumCols':
                            FullImageNumCols = sub_element.text                
                elif xml_element.tag == 'SCPPixel':
                    for sub_element in xml_element:
                        if sub_element.tag == 'Row':
                            SCPPixelRow = sub_element.text
                        elif sub_element.tag == 'Col':
                            SCPPixelCol = sub_element.text
                else:
                    print('break: ' + xml_element.tag)
        localImageData=ImageDataType(
        	NumRows=NumRows,
            NumCols=NumCols,
            PixelType=PixelType,
            FirstRow=FirstRow,
            FirstCol=FirstCol,
            FullImage=FullImageType(
                NumRows=FullImageNumRows,
                NumCols=FullImageNumCols
            ),
            SCPPixel=RowColType(Row=SCPPixelRow , Col=SCPPixelCol)
        )
        self._sicdmeta = SICDType(ImageData=localImageData)
        
    def sio_user_data_to_cphd_format(self):
        raise NotImplementedError
                


# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////