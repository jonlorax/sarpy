# SIOReader is a class implementing a specific FlatfileImageReader for SICD
# files using an SIO "carrier".  The SICD metadata is written in a user
# data field called "SICDMETA" in the standard SIO file format.  
#
# Written by: Tex Peterson
#
# //////////////////////////////////////////
# /// CLASSIFICATION: UNCLASSIFIED       ///
# //////////////////////////////////////////

# from sarpy.io.complex.generic.FlatfileImageReader import FlatfileImageReader
# from sarpy.io.complex.sicd_elements.SICD import SICDType

# class SIOReader(FlatfileImageReader):

#     def __init__(
#         self,
#         param_filename:              str, 
#     ):
#         super().__init__(param_filename=param_filename)
