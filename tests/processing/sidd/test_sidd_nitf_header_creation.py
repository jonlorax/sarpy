import json
import os

import pytest
import logging
import unittest
from tests import parse_file_entry # fails unless run using pytest
from datetime  import datetime, timezone

from sarpy.io.complex.converter import conversion_utility, open_complex
from sarpy.processing.ortho_rectify import NearestNeighborMethod
from sarpy.processing.sidd.sidd_product_creation import \
    create_detected_image_sidd, create_dynamic_image_sidd
import sarpy.visualization.remap as remap

from sarpy.utils import create_product

from sarpy.io.general.nitf import NITFDetails

complex_file_types = {}
this_loc           = os.path.abspath(__file__)

# JSON file that specifies test file locations
file_reference     = os.path.join(os.path.split(this_loc)[0], \
                                  'complex_file_types.json')  
if os.path.isfile(file_reference):
    with open(file_reference, 'r') as local_file:
        test_files_list = json.load(local_file)
        for test_files_type in test_files_list:
            valid_entries = []
            for entry in test_files_list[test_files_type]:
                the_file = parse_file_entry(entry)
                if the_file is not None:
                    valid_entries.append(the_file)
            complex_file_types[test_files_type] = valid_entries

sicd_files = complex_file_types.get('SICD', [])

def get_test_reader(idx):
    if idx >= len(sicd_files):
        return None
    input_file       = sicd_files[idx]
    reader           = open_complex(input_file)
    return reader

def test_nitf_fdt_updated_for_detected_image_sidd(tmp_path):
    local_reader = get_test_reader(0)
    ortho_helper = NearestNeighborMethod(local_reader, index=0)
    output_directory = tmp_path
    output_file = 'output.sidd'
    test_sidd = create_detected_image_sidd(ortho_helper, output_directory, output_file)
    sidd_file = os.path.join(*output_directory.parts,output_file)
    details = NITFDetails(sidd_file)
    fdt_datetime = datetime.strptime(details.nitf_header.FDT,"%Y%m%d%H%M%S%f")
    collection_datetime = datetime.strptime(details.img_headers[0].IDATIM,"%Y%m%d%H%M%S%f")
    current_time_zulu = datetime.now(timezone.utc).replace(tzinfo=None)
    time_delta = fdt_datetime - collection_datetime
    fdt_gt_cdt = time_delta.total_seconds() > 0
    recent_time_delta = current_time_zulu - fdt_datetime
    fdt_is_recent = recent_time_delta.total_seconds() < 120
    assert (fdt_gt_cdt and fdt_is_recent), 'NITF FileDateTime should be greater than IDATIM: {} > {}?'.format(details.nitf_header.FDT,details.img_headers[0].IDATIM)

def test_nitf_fdt_updated_for_dynamic_image_sidd(tmp_path):
    local_reader = get_test_reader(0)
    ortho_helper = NearestNeighborMethod(local_reader, index=0)
    output_directory = tmp_path
    output_file = 'output.sidd'
    test_sidd = create_dynamic_image_sidd(ortho_helper, output_directory, output_file)
    sidd_file = os.path.join(*output_directory.parts,output_file)
    details = NITFDetails(sidd_file)
    fdt_datetime = datetime.strptime(details.nitf_header.FDT,"%Y%m%d%H%M%S%f")
    collection_datetime = datetime.strptime(details.img_headers[0].IDATIM,"%Y%m%d%H%M%S%f")
    current_time_zulu = datetime.now(timezone.utc).replace(tzinfo=None)
    time_delta = fdt_datetime - collection_datetime
    fdt_gt_cdt = time_delta.total_seconds() > 0
    recent_time_delta = current_time_zulu - fdt_datetime
    fdt_is_recent = recent_time_delta.total_seconds() < 120
    assert (fdt_gt_cdt and fdt_is_recent), 'NITF FileDateTime should be greater than IDATIM: {} > {}?'.format(details.nitf_header.FDT,details.img_headers[0].IDATIM)

if __name__ == '__main__':
    unittest.main()





