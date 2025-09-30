# SIOWriter is a class implementing a specific FlatfileImageWriter for SICD
# files using an SIO "carrier".  The SICD metadata is written in a user
# data field called "SICDMETA" in the standard SIO file format.  The caller
# can also turn off the user data, since not all SIO readers handle this.
#
# Written by: Tom Krauss, NGA/IDT
#
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////

from sarpy.io.complex.generic.FlatfileImageWriter import FlatfileImageWriter
from sarpy.io.complex.sicd_elements.SICD import SICDType

class SIOWriter(FlatfileImageWriter):
    
    def __init__(
            # Parse inputs
            # These inputs are really parsed later in the superclass
            # constructor.  Here just need to 1) extract
            # include_sicd_metadata, which is specific to SIOWriter class
            # and 2) make sure that no additional arguments are passed--
            # like header_skip, which could break things, if passed on to
            # the superclass constructor.
            self,
            param_filename:              str, 
            param_sicdmeta:              SICDType,
            # numpy data types. "uint8", "float32", etc.
            param_data_type_str:         str = 'complex64', 
            param_data_type_code:        int = 13,
            param_is_complex:            bool = True,       # Boolean
            param_include_sicd_metadata: bool = True,       # Boolean
    ):
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
        self._include_sicd_metadata = param_include_sicd_metadata
        header_skip = 5*4 # SIO header with no user data is 5 uint32 words
        if self._include_sicd_metadata:
            XML_meta_string = param_sicdmeta.to_xml_string()
            header_skip = header_skip + 4 + 4 + 8 + 4 + len(XML_meta_string); # Add user data length
        
        # Call the init function of the parent class
        super().__init__(param_filename=param_filename, 
                         param_sicdmeta=param_sicdmeta,
                         param_data_type_str=param_data_type_str,
                         param_data_type_code=param_data_type_code,
                         param_is_complex=param_is_complex,
                         param_header_skip=header_skip)
        
        # Magic key
        # We always write big-endian
        if param_include_sicd_metadata:
            magic_key = 0xFF027FFD # Indicates big endian, with user-data
        else:
            magic_key = 0xFF017FFE # Indicates big endian, with no user-data
        self._fid.seek(0)
        self._fid.write(magic_key.to_bytes(4))
        # Rows and columns
        self._fid.write(self._image_size[1].to_bytes(4))
        self._fid.write(self._image_size[0].to_bytes(4))
        # Data type and size
        self.numpy_data_type_to_sio()
        self._fid.write(self._data_type_code.to_bytes(4))
        self._fid.write(self._data_size.to_bytes(4))
        # User data
        if self._include_sicd_metadata:
            self._fid.write((1).to_bytes(4))                    # Num pairs of user data
            self._fid.write((8).to_bytes(4))                    # Pair 1 name length
            self._fid.write('SICDMETA'.encode('utf-8'))           # Pair 1 name
            self._fid.write(len(XML_meta_string).to_bytes(4)) # Pair 1 value length
            self._fid.write(XML_meta_string.encode('utf-8'))      # Pair 1 value
    
    def numpy_data_type_to_sio(self):
        match self._data_type_str:
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
                
    

# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////