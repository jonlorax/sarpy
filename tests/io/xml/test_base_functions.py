__classification__ = "UNCLASSIFIED"
__author__ = "Tex Peterson"

import numpy as np
import unittest
import xml.etree.ElementTree as ET
from collections import OrderedDict

import sarpy.io.xml.base as base

# ********************
# get_node_value tests
# ********************
class TestGetNodeValue(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_get_node_value_success_with_text(self):
        branch = base.get_node_value(self.root[0][1])
        self.assertEqual(branch, '2008')

    def test_get_node_value_success_none(self):
        branch = base.get_node_value(self.root[0])
        self.assertIsNone(branch)

    def test_get_node_value_success_empty(self):
        branch = base.get_node_value(self.root[0][3])
        self.assertIsNone(branch)

# ********************
# create_new_node tests
# ********************
class TestCreateNewNode(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_create_new_node_no_parent_success(self):
        new_node_tag = "country"
        self.assertEqual(len(self.root), 3, 
                         "Root should have 3 children before adding new node")
        new_node = base.create_new_node(self.tree, new_node_tag)
        self.assertEqual(len(self.root), 4, 
                         "Root should have 4 children after adding new node")
        self.assertEqual(self.root[-1].tag, new_node_tag, 
                         "Last child should have the new node tag")
        self.assertIs(self.root[-1], new_node, 
                      "Returned node should be the last child of root")

    def test_create_new_node_with_parent_success(self):
        new_node_tag = "ocean"
        self.assertEqual(len(self.root[1]), 5, 
                         "Parent should have 5 children before adding new node")
        new_node = base.create_new_node(self.tree, new_node_tag, self.root[1])
        self.assertEqual(len(self.root[1]), 6, 
                         "Parent should have 6 children after adding new node")
        self.assertEqual(self.root[1][5].tag, new_node_tag, 
                         "Last child should have the new node tag")
        self.assertIs(self.root[1][5], new_node, 
                      "Returned node should be the last child of parent")

# ********************
# create_text_node tests
# ********************
class TestCreateTextNode(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_create_text_node_no_parent_success(self):
        new_node_tag = "country"
        new_node_value = "Costa Rica"
        self.assertEqual(len(self.root), 3, 
                         "Root should have 3 children before adding new " + \
                                    "text node")
        new_node = base.create_text_node(self.tree, new_node_tag, new_node_value)
        self.assertEqual(len(self.root), 4, 
                         "Root should have 4 children after adding new " + \
                                    "text node")
        self.assertEqual(self.root[3].tag, new_node_tag, 
                         "Last child should have the new node tag")
        self.assertEqual(self.root[3].text, new_node_value, 
                         "Last child's text should match the new node value")
        self.assertIs(self.root[3], new_node, 
                      "Returned node should be the last child of root")

    def test_create_text_node_with_parent_success(self):
        new_node_tag = "ocean"
        new_node_value = "Pacific"
        self.assertEqual(len(self.root[2]), 6, 
                         "Parent should have 6 children before adding new " + \
                                    "text node")
        new_node = base.create_text_node(self.tree, new_node_tag, 
                                         new_node_value, self.root[2])
        self.assertEqual(len(self.root[2]), 7, 
                         "Parent should have 7 children after adding new " + \
                                    "text node")
        self.assertEqual(self.root[2][6].tag, new_node_tag, 
                         "Last child should have the new node tag")
        self.assertEqual(self.root[2][6].text, new_node_value, 
                         "Last child's text should match the new node value")
        self.assertIs(self.root[2][6], new_node, 
                      "Returned node should be the last child of parent")

# ********************
# find_first_child tests
# ********************
class TestFindFirstChild(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_find_first_child_no_optional_params_success(self):
        found_node = base.find_first_child(self.root, "country")
        self.assertIsNotNone(found_node, "Should find a node with tag 'country'")
        self.assertEqual(found_node.attrib, self.root[0].attrib, 
                         "Found node's attributes should match the first " + \
                                    "'country' node")

    def test_find_first_child_namespace_params_success(self):
        found_node = base.find_first_child(self.actor_root, "actor", 
                                           self.actor_ns_dict)
        self.assertIsNotNone(found_node, 
                             "Should find a node with tag 'actor' using namespace")
        self.assertEqual(found_node.attrib, 
                         self.actor_root[0].attrib, 
                         "Found node's attributes should match the first " + \
                                    "'actor' node")

    def test_find_first_child_namespace_nskey_params_success(self):
        found_actor_node = base.find_first_child(self.actor_root, "actor", 
                                                 self.actor_ns_dict)
        found_node = base.find_first_child(found_actor_node, "character", 
                                           self.actor_ns_dict, "fictional")
        self.assertIsNotNone(
            found_node, 
            "Should find a node with tag 'character' using namespace and nskey")
        self.assertEqual(found_node.attrib, 
                         self.actor_root[0].attrib, 
                         "Found node's attributes should match the first " + \
                                    "'actor' node")

# ********************
# find_children tests
# ********************
class TestFindChildren(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_find_children_no_optional_params_success(self):
        found_nodes = base.find_children(self.root, "country")
        self.assertEqual(found_nodes, 
                         self.root.findall("country"), 
                         "Should find all 'country' nodes without namespace")

    def test_find_children_namespace_params_success(self):
        found_node = base.find_children(self.actor_root, "actor", 
                                        self.actor_ns_dict)
        self.assertEqual(found_node, 
                         self.actor_root.findall('actor',self.actor_ns_dict)
                         )

    def test_find_children_namespace_nskey_params_success(self):
        found_actor_node = base.find_first_child(self.actor_root, "actor", 
                                                 self.actor_ns_dict)
        found_nodes = base.find_children(found_actor_node, "character", 
                                         self.actor_ns_dict, "fictional")
        self.assertEqual(
            found_nodes,
            found_actor_node.findall('fictional:character', self.actor_ns_dict),
            "Should find all 'character' nodes with namespace and nskey"
        )

# ********************
# parse_xml_from_string tests
# ********************
class TestParseXmlFromString(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_xml_from_string_success(self):
        xml_string = ET.tostring(self.root, encoding='unicode', method='xml')
        root_node, ns_dict = base.parse_xml_from_string(xml_string)
        self.assertEqual(root_node.attrib, self.root.attrib, 
                            "Parsed root node's attributes should match the " + \
                            "original root")
    
# ********************
# parse_xml_from_file tests
# ********************
class TestParseXmlFromFile(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_xml_from_file_success(self):
        test_root, test_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/country_data.xml')
        self.assertEqual(test_root.attrib, self.root.attrib)
        
# ********************
# validate_xml_from_string tests
# ********************
class TestValidateXmlFromString(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_validate_xml_from_string_success(self):
        xml_string = ET.tostring(self.root, encoding='unicode', method='xml')
        xsd_path = 'tests/io/xml/country.xsd'
        self.assertTrue(base.validate_xml_from_string(xml_string, xsd_path), 
                        "XML string should validate against the provided XSD")
        
    def test_validate_xml_from_string_with_logger_success(self):
        xml_string = ET.tostring(self.root, encoding='unicode', method='xml')
        xsd_path = 'tests/io/xml/country.xsd'
        self.assertTrue(base.validate_xml_from_string(xml_string, xsd_path, 
                                                      base.logger), 
                        "XML string should validate against the provided " + \
                                    "XSD with logger")

# ********************
# validate_xml_from_file tests
# ********************
class TestValidateXmlFromFile(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_validate_xml_from_file_success(self):
        xml_path = 'tests/io/xml/country_data.xml'
        xsd_path = 'tests/io/xml/country.xsd'
        self.assertTrue(base.validate_xml_from_file(xml_path, xsd_path), 
                        "XML file should validate against the provided XSD")
        
    def test_validate_xml_from_file_with_logger_success(self):
        xml_path = 'tests/io/xml/country_data.xml'
        xsd_path = 'tests/io/xml/country.xsd'
        self.assertTrue(
            base.validate_xml_from_file(xml_path, xsd_path, base.logger),
            "XML file should validate against the provided XSD with logger"
        )
        
# ********************
# parse_str tests
# ********************
class TestParseStr(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_str_no_params_fail(self):
        with self.assertRaisesRegex(
            TypeError, 
            r"parse_str\(\) missing 3 required positional arguments: " + \
                                    "'value', 'name', and 'instance'$"
        ):
            base.parse_str()
        
    def test_parse_str_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_str\(\) missing 2 " + \
                                    "required positional arguments: 'name' " + \
                                    "and 'instance'$"):
            base.parse_str("Test")

    def test_parse_str_missing_instance_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_str\(\) missing 1 " + \
                                    "required positional argument: 'instance'$"):
            base.parse_str("Test", "Bob")

    def test_parse_str_value_param_is_string_success(self):
        self.assertEqual(base.parse_str("Test", "Bob", "base"), "Test")

    def test_parse_str_value_param_is_None_success(self):
        self.assertIsNone(base.parse_str(None, "Bob", "base"))

    def test_parse_str_value_param_is_xml_with_value_success(self):
        self.assertEqual(base.parse_str(self.root[0][2], "text", "base"), 
                         self.root[0][2].text)
        
    def test_parse_str_value_param_is_xml_empty_value_success(self):
        self.assertEqual(base.parse_str(self.root[0], "text", "base"), 
                         self.root[0].text.strip()
                         )
        
    def test_parse_str_bad_value_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"field Bob of class str " + \
                                    "requires a string value."):
            base.parse_str(1, "Bob", "base")

# ********************
# parse_bool tests
# ********************
class TestParseBool(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_bool_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_bool\(\) missing 3 " + \
                                    "required positional arguments: 'value', " + \
                                    "'name', and 'instance'$"):
            base.parse_bool()
        
    def test_parse_bool_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_bool\(\) missing 2 " + \
                                    "required positional arguments: 'name' " + \
                                    "and 'instance'$"):
            base.parse_bool("Test")

    def test_parse_bool_missing_instance_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_bool\(\) missing 1 " + \
                                    "required positional argument: 'instance'$"):
            base.parse_bool("Test", "Bob")

    def test_parse_bool_value_param_is_None_success(self):
        self.assertIsNone(base.parse_bool(None, "Bob", "base"))

    def test_parse_bool_value_param_is_bool_success(self):
        self.assertTrue(base.parse_bool(True, "Bob", "base"))

    def test_parse_bool_value_param_is_int_success(self):
        self.assertTrue(base.parse_bool(1, "Bob", "base"))

    def test_parse_bool_value_param_is_np_bool_success(self):
        arr_bool = np.array([True, False, True, False], dtype=bool)
        self.assertTrue(base.parse_bool(arr_bool[0], "Bob", "base"))
        
    def test_parse_bool_value_param_is_xml_success(self):
        self.assertTrue(base.parse_bool(self.root[0][0], "Bob", "base"))

    def test_parse_bool_value_param_is_string_true_success(self):
        self.assertTrue(base.parse_bool('trUe', "Bob", "base"))

    def test_parse_bool_value_param_is_string_1_success(self):
        self.assertTrue(base.parse_bool('1', "Bob", "base"))

    def test_parse_bool_value_param_is_string_false_success(self):
        self.assertFalse(base.parse_bool('FALSE', "Bob", "base"))

    def test_parse_bool_value_param_is_string_0_success(self):
        self.assertFalse(base.parse_bool('0', "Bob", "base"))

    def test_parse_bool_value_param_is_float_fail(self):
        with self.assertRaisesRegex(ValueError, r"Boolean field Bob of " + \
                                    "class str cannot assign from type " + \
                                    "<class 'float'>."):
            base.parse_bool(3.5, "Bob", "base")

# ********************
# parse_int tests
# ********************
class TestParseInt(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_int_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_int\(\) missing 3 " + \
                                    "required positional arguments: 'value', " + \
                                    "'name', and 'instance'$"):
            base.parse_int()
        
    def test_parse_int_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_int\(\) missing 2 " + \
                                    "required positional arguments: 'name' " + \
                                    "and 'instance'$"):
            base.parse_int("Test")

    def test_parse_int_missing_instance_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_int\(\) missing 1 " + \
                                    "required positional argument: 'instance'$"):
            base.parse_int("Test", "Bob")

    def test_parse_int_value_param_is_None_success(self):
        self.assertIsNone(base.parse_int(None, "Bob", "base"))

    def test_parse_int_value_param_is_int_success(self):
        self.assertEqual(base.parse_int(1, "Bob", "base"), 1)

    def test_parse_int_value_param_is_xml_success(self):
        self.assertEqual(base.parse_int(self.root[0][0], "Bob", "base"), 1)

    def test_parse_int_value_param_is_string_1_success(self):
        self.assertEqual(base.parse_int('1', "Bob", "base"), 1)

    def test_parse_int_value_param_is_string_non_int_success(self):
        with self.assertRaisesRegex(ValueError, r"invalid literal for " + \
                                    "int\(\) with base 10: 'Bob'"):
            assert(base.parse_int('Bob', "Bob", "base") == 1)

    def test_parse_int_value_param_is_list_non_int_success(self):
        with self.assertRaisesRegex(TypeError, r"int\(\) argument must be a " + \
                                    "string, a bytes-like object or a real " + \
                                    "number, not 'list'"):
            assert(base.parse_int([3.5], "Bob", "base") == 1)

# ********************
# parse_float tests
# ********************
class TestParseFloat(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_float_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_float\(\) missing 3 " + \
                                    "required positional arguments: 'value', " + \
                                    "'name', and 'instance'$"):
            base.parse_float()
        
    def test_parse_float_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_float\(\) missing 2 " + \
                                    "required positional arguments: 'name' " + \
                                    "and 'instance'$"):
            base.parse_float("Test")

    def test_parse_float_missing_instance_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_float\(\) missing 1 " + \
                                    "required positional argument: 'instance'$"):
            base.parse_float("Test", "Bob")

    def test_parse_float_value_param_is_None_success(self):
        self.assertIsNone(base.parse_float(None, "Bob", "base"))

    def test_parse_float_value_param_is_float_success(self):
        self.assertEqual(base.parse_float(1.5, "Bob", "base"), 1.5)

    def test_parse_float_value_param_is_xml_success(self):
        self.assertEqual(base.parse_float(self.root[0][0], "Bob", "base"), 1.0)

    def test_parse_float_value_param_is_string_1dot5_success(self):
        self.assertEqual(base.parse_float('1.5', "Bob", "base"), 1.5)

    def test_parse_float_value_param_is_string_non_int_success(self):
        with self.assertRaisesRegex(ValueError, r"could not convert string " + \
                                    "to float: 'Bob'"):
            base.parse_float('Bob', "Bob", "base")

    def test_parse_float_value_param_is_list_non_int_success(self):
        with self.assertRaisesRegex(TypeError, r"float\(\) argument must be " + \
                                    "a string or a real number, not 'list'"):
            base.parse_float([3.5], "Bob", "base")

# ********************
# parse_complex tests
# ********************
class TestParseComplex(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_parse_complex_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_complex\(\) missing " + \
                                    "3 required positional arguments: 'value'," + \
                                    " 'name', and 'instance'$"):
            base.parse_complex()
        
    def test_parse_complex_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_complex\(\) missing 2 " + \
                                    "required positional arguments: 'name' " + \
                                    "and 'instance'$"):
            base.parse_complex("Test")

    def test_parse_complex_missing_instance_param_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_complex\(\) missing 1 " + \
                                    "required positional argument: 'instance'$"):
            base.parse_complex("Test", "Bob")

    def test_parse_complex_value_param_is_None_success(self):
        self.assertIsNone(base.parse_complex(None, "Bob", "base"))

    def test_parse_complex_value_param_is_complex_success(self):
        test_complex = 3 + 2j
        self.assertEqual(base.parse_complex(test_complex, "Bob", "base"), 
                         test_complex)

    def test_parse_complex_value_param_is_xml_success(self):
        test_complex = 3 + 2j
        self.assertEqual(base.parse_complex(self.root[0][4], "Bob", "base"), 
                         test_complex)

    def test_parse_complex_value_param_is_xml_2_real_fail(self):
        test_complex = 3 + 2j
        with self.assertRaisesRegex(ValueError, r"There must be exactly one " + \
                                    "Real component of a complex type node " + \
                                    "defined for field Bob of class str."):
            base.parse_complex(self.root[1][3], "Bob", "base")

    def test_parse_complex_value_param_is_xml_2_imag_fail(self):
        test_complex = 3 + 2j
        with self.assertRaisesRegex(ValueError, r"There must be exactly one " + \
                                    "Imag component of a complex type node " + \
                                    "defined for field Bob of class str."):
            base.parse_complex(self.root[2][3], "Bob", "base")

    def test_parse_complex_value_param_is_complex_dict_1_success(self):
        test_complex = 3 + 2j
        self.assertEqual(base.parse_complex({"real":3, "imag":2}, "Bob", "base"), 
                         test_complex)

    def test_parse_complex_value_param_is_complex_dict_2_success(self):
        test_complex = 3 + 2j
        self.assertEqual(base.parse_complex({"Real":3, "Imag":2}, "Bob", "base"), 
                         test_complex)

    def test_parse_complex_value_param_is_complex_dict_3_success(self):
        test_complex = 3 + 2j
        self.assertEqual(base.parse_complex({"re":3, "im":2}, "Bob", "base"), 
                         test_complex)

    def test_parse_complex_value_param_is_complex_dict_4_fail(self):
        test_complex = 3 + 2j
        with self.assertRaisesRegex(ValueError, r"Cannot convert dict {'not': 3, 'valid': 2} to a complex number for field Bob of class str."):
            base.parse_complex({"not":3, "valid":2}, "Bob", "base")

    def test_parse_complex_value_param_is_complex_dict_5_fail(self):
        test_complex = 3 + 2j
        with self.assertRaisesRegex(ValueError, r"Cannot convert dict {'real': None, 'imag': 2} to a complex number for field Bob of class str."):
            base.parse_complex({"real":None, "imag":2}, "Bob", "base")

    def test_parse_complex_value_param_is_complex_dict_6_fail(self):
        test_complex = 3 + 2j
        with self.assertRaisesRegex(ValueError, r"Cannot convert dict {'real': 4, 'imag': None} to a complex number for field Bob of class str."):
            base.parse_complex({"real":4, "imag":None}, "Bob", "base")

    def test_parse_complex_value_param_is_string_non_int_fail(self):
        with self.assertRaisesRegex(ValueError, r"complex\(\) arg is a malformed string"):
            base.parse_complex('Bob', "Bob", "base")

    def test_parse_complex_value_param_is_list_non_int_fail(self):
        with self.assertRaisesRegex(TypeError, r"complex\(\) first argument must be a string or a number, not 'list'"):
            base.parse_complex([3.5], "Bob", "base")


# ********************
# parse_serializable tests
# ********************

class ParseSerializableDummyType:
    @classmethod
    def from_dict(cls, d):
        return cls(**d)
    @classmethod
    def from_node(cls, node, xml_ns, ns_key=None):
        return cls(node=node, xml_ns=xml_ns, ns_key=ns_key)
    @classmethod
    def from_array(cls, arr):
        return cls(arr=arr)
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class ParseSerializableDummyArrayable(base.Arrayable):
    @classmethod
    def from_array(cls, arr):
        return cls(arr)
    def __init__(self, arr):
        self.arr = arr

class ParseSerializableDummyInstance:
    _xml_ns = {'default': 'urn:test'}
    _xml_ns_key = 'default'
    _child_xml_ns_key = {'foo': 'default'}

class TestParseSerializable(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse('tests/io/xml/country_data.xml')
        self.actor_tree = ET.parse('tests/io/xml/actor_test_data.xml')
        self.root = self.tree.getroot()
        # For xml ns is an abbreviation for name space
        self.actor_root, self.actor_ns_dict = \
            base.parse_xml_from_file('tests/io/xml/actor_test_data.xml') 

    def test_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable\(\) missing " + \
                                    "4 required positional arguments: 'value'," + \
                                    " 'name', 'instance', and 'the_type'$"):
            base.parse_serializable()
            
    def test_value_param_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable\(\) missing 3 " + \
                                    "required positional arguments: 'name', " + \
                                    "'instance', and 'the_type'$"):
            base.parse_serializable("Test")

    def test_value_name_params_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable\(\) missing 2 " + \
                                    "required positional arguments: " + \
                                    "'instance' and 'the_type'$"):
            base.parse_serializable("Test", "foo")

    def test_value_name_instance_params_only_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable\(\) missing 1 " + \
                                    "required positional argument: 'the_type'$"):
            base.parse_serializable("Test", "foo", ParseSerializableDummyInstance())

    def test_none(self):
        self.assertIsNone(base.parse_serializable(None, 'foo', 
                                                  ParseSerializableDummyInstance(), 
                                                  ParseSerializableDummyType))

    def test_instance(self):
        obj = ParseSerializableDummyType(a=1)
        self.assertIs(base.parse_serializable(obj, 'foo', 
                                              ParseSerializableDummyInstance(), 
                                              ParseSerializableDummyType), obj)

    def test_dict(self):
        result = base.parse_serializable({'a': 1}, 'foo', 
                                         ParseSerializableDummyInstance(), 
                                         ParseSerializableDummyType)
        self.assertIsInstance(result, ParseSerializableDummyType)
        self.assertEqual(result.a, 1)

    def test_element(self):
        elem = ET.Element('Dummy')
        result = base.parse_serializable(elem, 'foo', 
                                         ParseSerializableDummyInstance(), 
                                         ParseSerializableDummyType)
        self.assertIsInstance(result, ParseSerializableDummyType)
        self.assertEqual(result.node, elem)
        self.assertEqual(result.xml_ns, ParseSerializableDummyInstance._xml_ns)
        self.assertEqual(result.ns_key, 
                         ParseSerializableDummyInstance._child_xml_ns_key['foo'])

    def test_arrayable_ndarray(self):
        arr = np.array([1, 2, 3])
        result = base.parse_serializable(arr, 'foo', 
                                         ParseSerializableDummyInstance(), 
                                         ParseSerializableDummyArrayable)
        self.assertIsInstance(result, ParseSerializableDummyArrayable)
        np.testing.assert_array_equal(result.arr, arr)

    def test_arrayable_ndarray_bad_type_fail(self):
        arr = np.array([1, 2, 3])
        with self.assertRaisesRegex(TypeError, r"Field foo of class " + \
                                    "ParseSerializableDummyInstance is of type " + \
                                    "<class 'int'> \(not a subclass of " + \
                                    "Arrayable\) and got an argument of type " + \
                                    "<class 'numpy.ndarray'>.$"):
            result = base.parse_serializable(arr, 'foo', 
                                             ParseSerializableDummyInstance(), 
                                             int)

    def test_arrayable_list(self):
        arr = [1, 2, 3]
        result = base.parse_serializable(arr, 'foo', 
                                         ParseSerializableDummyInstance(), 
                                         ParseSerializableDummyArrayable)
        self.assertIsInstance(result, ParseSerializableDummyArrayable)
        self.assertEqual(result.arr, arr)

    def test_arrayable_tuple(self):
        arr = (1, 2, 3)
        result = base.parse_serializable(arr, 'foo', 
                                         ParseSerializableDummyInstance(), 
                                         ParseSerializableDummyArrayable)
        self.assertIsInstance(result, ParseSerializableDummyArrayable)
        self.assertEqual(result.arr, arr)

    def test_non_arrayable_array(self):
        arr = [1, 2, 3]
        with self.assertRaises(TypeError):
            base.parse_serializable(arr, 'foo', 
                                    ParseSerializableDummyInstance(), 
                                    ParseSerializableDummyType)

    def test_invalid_type(self):
        with self.assertRaisesRegex(TypeError, r"Field foo of class " + \
                                    "ParseSerializableDummyInstance is " + \
                                    "expecting type <class " + \
                                    "'test_base_functions." + \
                                    "ParseSerializableDummyType'>, but got an " + \
                                    "instance of incompatible type " + \
                                    "<class 'float'>.$"):
            base.parse_serializable(123.456, 'foo', 
                                    ParseSerializableDummyInstance(), 
                                    ParseSerializableDummyType)

class ParseSerializableArrayDummyArrayable(base.Arrayable):
    def __init__(self, arr):
        self.arr = np.array(arr)
    @classmethod
    def from_array(cls, arr):
        return cls(arr)
    def get_array(self, dtype=None):
        return self.arr

class ParseSerializableArrayDummySerializable:
    @classmethod
    def from_node(cls, node, xml_ns, ns_key=None):
        return cls(node.tag)
    @classmethod
    def from_dict(cls, d):
        return cls(d['tag'])
    def __init__(self, tag):
        self.tag = tag

class ParseSerializableArrayDummyInstance:
    _xml_ns = None
    _xml_ns_key = None
    _child_xml_ns_key = {}

class TestParseSerializableArray(unittest.TestCase):
    def test_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable_array\(\) " + \
                                    "missing 5 required positional arguments: " + \
                                    "'value', 'name', 'instance', " + \
                                    "'child_type', and 'child_tag'$"):
            base.parse_serializable_array()
            
    def test_value_param_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_array\(\) " + \
                                    "missing 4 required positional arguments: " + \
                                    "'name', 'instance', 'child_type', " + \
                                    "and 'child_tag'$"):
            base.parse_serializable_array('foo')

    def test_value_name_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_array\(\) " + \
                                    "missing 3 required positional arguments: " + \
                                    "'instance', 'child_type', and 'child_tag'$"):
            base.parse_serializable_array('foo', 'bar')

    def test_value_name_instance_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_array\(\) " + \
                                    "missing 2 required positional arguments: " + \
                                    "'child_type' and 'child_tag'$"):
            base.parse_serializable_array('foo', 'bar', 
                                          ParseSerializableArrayDummyInstance())

    def test_value_name_instance_child_type_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_array\(\) " + \
                                    "missing 1 required positional argument: " + \
                                    "'child_tag'$"):
            base.parse_serializable_array('foo', 'bar', 
                                          ParseSerializableArrayDummyInstance(),
                                          ParseSerializableArrayDummySerializable)
            
    def test_none_returns_none(self):
        self.assertIsNone(base.\
                          parse_serializable_array(None, 'test',
                                                   ParseSerializableArrayDummyInstance(),
                                                   ParseSerializableArrayDummySerializable,
                                                   'child'))

    def test_single_child_type(self):
        obj = ParseSerializableArrayDummySerializable('child')
        arr = base.parse_serializable_array(obj, 'test', 
                                            ParseSerializableArrayDummyInstance(), 
                                            ParseSerializableArrayDummySerializable, 
                                            'child')
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.size, 1)
        self.assertIs(arr[0], obj)

    def test_ndarray_of_arrayable(self):
        arr = np.array([[1, 2], [3, 4]])
        result = base.parse_serializable_array(arr, 'test', 
                                               ParseSerializableArrayDummyInstance(), 
                                               ParseSerializableArrayDummyArrayable, 
                                               'child')
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.size, 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableArrayDummyArrayable) for x in result)
        )

    def test_ndarray_wrong_dtype(self):
        arr = np.array([1, 2, 3], dtype=int)
        with self.assertRaisesRegex(ValueError, r"Attribute test of array " + \
                                    "type functionality belonging to class " + \
                                    "ParseSerializableArrayDummyInstance got " + \
                                    "an ndarray of dtype int64,and child " + \
                                    "type is not a subclass of Arrayable.$"):
            base.parse_serializable_array(arr, 'test', 
                                          ParseSerializableArrayDummyInstance(), 
                                          ParseSerializableArrayDummySerializable, 
                                          'child')

    def test_ndarray_wrong_shape(self):
        arr = np.empty((2,2), dtype=object)
        arr[0,0] = ParseSerializableArrayDummySerializable('child')
        arr[0,1] = ParseSerializableArrayDummySerializable('child')
        arr[1,0] = ParseSerializableArrayDummySerializable('child')
        arr[1,1] = ParseSerializableArrayDummySerializable('child')
        with self.assertRaisesRegex(ValueError, r"Attribute test of array " + \
                                    "type functionality belonging to class " + \
                                    "ParseSerializableArrayDummyInstance got " + \
                                    "an ndarray of shape \(2, 2\),but requires " + \
                                    "a one dimensional array.$"):
            base.parse_serializable_array(arr, 'test', 
                                          ParseSerializableArrayDummyInstance(), 
                                          ParseSerializableArrayDummySerializable, 
                                          'child')

    def test_ndarray_wrong_type(self):
        arr = np.array([1, 2, 3], dtype=object)
        with self.assertRaisesRegex(TypeError, r"Attribute test of array type " + \
                                    "functionality belonging to class " + \
                                    "ParseSerializableArrayDummyInstance got " + \
                                    "an ndarray containing first element of " + \
                                    "incompatible type <class 'int'>.$"):
            base.parse_serializable_array(arr, 'test', 
                                          ParseSerializableArrayDummyInstance(), 
                                          ParseSerializableArrayDummySerializable, 
                                          'child')

    def test_xml_element(self):
        xml = "<parent size='2'><child/><child/></parent>"
        elem = ET.fromstring(xml)
        result = base.parse_serializable_array(elem, 'test', 
                                               ParseSerializableArrayDummyInstance(), 
                                               ParseSerializableArrayDummySerializable, 
                                               'child')
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.size, 2)
        self.assertTrue(
            all(isinstance(x, ParseSerializableArrayDummySerializable) 
                for x in result))

    def test_xml_element_wrong_size(self):
        xml = "<parent size='3'><child/><child/></parent>"
        elem = ET.fromstring(xml)
        with self.assertRaisesRegex(ValueError, r"Attribute test of array " + \
                                    "type functionality belonging to class " + \
                                    "ParseSerializableArrayDummyInstance got " + \
                                    "a ElementTree element with size " + \
                                    "attribute 3, but has 2 child nodes " + \
                                    "with tag child.$"):
            base.parse_serializable_array(elem, 'test', 
                                          ParseSerializableArrayDummyInstance(), 
                                          ParseSerializableArrayDummySerializable, 
                                          'child')

    def test_list_of_child_type(self):
        objs = [ParseSerializableArrayDummySerializable('child'), 
                ParseSerializableArrayDummySerializable('child')]
        arr = base.parse_serializable_array(objs, 'test', 
                                            ParseSerializableArrayDummyInstance(), 
                                            ParseSerializableArrayDummySerializable, 
                                            'child')
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.size, 2)
        self.assertTrue(all(isinstance(x, ParseSerializableArrayDummySerializable) 
                            for x in arr))

    def test_list_of_dict(self):
        dicts = [{'tag': 'child'}, {'tag': 'child2'}]
        arr = base.parse_serializable_array(dicts, 'test', 
                                            ParseSerializableArrayDummyInstance(), 
                                            ParseSerializableArrayDummySerializable, 
                                            'child')
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.size, 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableArrayDummySerializable) for x in arr)
            )

    def test_list_of_arrayable(self):
        arrs = [[1,2], [3,4]]
        arr = base.parse_serializable_array(arrs, 'test', 
                                            ParseSerializableArrayDummyInstance(), 
                                            ParseSerializableArrayDummyArrayable, 
                                            'child')
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.size, 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableArrayDummyArrayable) for x in arr))

    def test_list_of_incompatible_type(self):
        arrs = [1, 2]
        with self.assertRaisesRegex(TypeError, r"Attribute test of array type " + \
                                    "functionality belonging to class " + \
                                    "ParseSerializableArrayDummyInstance got " + \
                                    "a list containing first element of " + \
                                    "incompatible type <class 'int'>.$"):
            base.parse_serializable_array(arrs, 'test', 
                                          ParseSerializableArrayDummyInstance(), 
                                          ParseSerializableArrayDummySerializable, 
                                          'child')

    def test_empty_list(self):
        arr = base.parse_serializable_array([], 'test', 
                                            ParseSerializableArrayDummyInstance(), 
                                            ParseSerializableArrayDummySerializable, 
                                            'child')
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.size, 0)

class ParseSerializableListDummySerializable:
    @classmethod
    def from_node(cls, node, xml_ns, ns_key=None):
        return cls(node.tag)
    @classmethod
    def from_dict(cls, d):
        return cls(d['tag'])
    def __init__(self, tag):
        self.tag = tag

class ParseSerializableListDummyInstance:
    _xml_ns = None
    _xml_ns_key = None
    _child_xml_ns_key = {}

class TestParseSerializableList(unittest.TestCase):
    def test_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_serializable_list\(\) " + \
                                    "missing 4 required positional arguments: " + \
                                    "'value', 'name', 'instance', and 'child_type'$"):
            base.parse_serializable_list()
            
    def test_value_param_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_list\(\) " + \
                                    "missing 3 required positional arguments: " + \
                                    "'name', 'instance', and 'child_type'$"):
            base.parse_serializable_list('foo')

    def test_value_name_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_list\(\) " + \
                                    "missing 2 required positional arguments: " + \
                                    "'instance' and 'child_type'$"):
            base.parse_serializable_list('foo', 'bar')

    def test_value_name_instance_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_serializable_list\(\) " + \
                                    "missing 1 required positional argument: " + \
                                    "'child_type'$"):
            base.parse_serializable_list('foo', 'bar', 
                                          ParseSerializableListDummyInstance())

    def test_none_returns_none(self):
        self.assertIsNone(base.parse_serializable_list(None, 'test', 
                                                       ParseSerializableListDummyInstance(), 
                                                       ParseSerializableListDummySerializable))

    def test_single_child_type(self):
        obj = ParseSerializableListDummySerializable('child')
        result = base.parse_serializable_list(obj, 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIs(result[0], obj)

    def test_xml_element(self):
        xml = "<child/>"
        elem = ET.fromstring(xml)
        result = base.parse_serializable_list(elem, 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ParseSerializableListDummySerializable)
        self.assertEqual(result[0].tag, "child")

    def test_list_of_child_type(self):
        objs = [ParseSerializableListDummySerializable('child'), 
                ParseSerializableListDummySerializable('child')]
        result = base.parse_serializable_list(objs, 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableListDummySerializable) for x in result)
            )

    def test_list_of_dict(self):
        dicts = [{'tag': 'child'}, {'tag': 'child2'}]
        result = base.parse_serializable_list(dicts, 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableListDummySerializable) for x in result)
            )
        self.assertEqual(result[0].tag, 'child')
        self.assertEqual(result[1].tag, 'child2')

    def test_list_of_xml_elements(self):
        xml = "<root><child/><child/></root>"
        elem = ET.fromstring(xml)
        children = list(elem)
        result = base.parse_serializable_list(children, 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            isinstance(x, ParseSerializableListDummySerializable) for x in result)
            )

    def test_list_of_incompatible_type(self):
        arrs = [1, 2]
        with self.assertRaisesRegex(TypeError, r"Field test of list type " + \
                                    "functionality belonging to class " + \
                                    "ParseSerializableListDummyInstance got a " + \
                                    "list containing first element of " + \
                                    "incompatible type <class 'int'>.$"):
            base.parse_serializable_list(arrs, 'test', 
                                         ParseSerializableListDummyInstance(), 
                                         ParseSerializableListDummySerializable)

    def test_empty_list(self):
        result = base.parse_serializable_list([], 'test', 
                                              ParseSerializableListDummyInstance(), 
                                              ParseSerializableListDummySerializable)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class ParseParametersCollectionDummyInstance:
    pass

class TestParseParametersCollection(unittest.TestCase):
    def test_no_params_fail(self):
        with self.assertRaisesRegex(TypeError, r"parse_parameters_collection\(\) " + \
                                    "missing 3 required positional arguments: " + \
                                    "'value', 'name', and 'instance'$"):
            base.parse_parameters_collection()
            
    def test_value_param_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_parameters_collection\(\) " + \
                                    "missing 2 required positional arguments: " + \
                                    "'name' and 'instance'$"):
            base.parse_parameters_collection('foo')

    def test_value_name_params_only_fail(self):
         with self.assertRaisesRegex(TypeError, r"parse_parameters_collection\(\) " + \
                                    "missing 1 required positional argument: " + \
                                    "'instance'$"):
            base.parse_parameters_collection('foo', 'bar')

    def test_none_returns_none(self):
        self.assertIsNone(base.parse_parameters_collection(None, 'params', 
                                                           ParseParametersCollectionDummyInstance()))

    def test_dict_returns_dict(self):
        d = {'a': '1', 'b': '2'}
        result = base.parse_parameters_collection(d, 'params', 
                                                  ParseParametersCollectionDummyInstance())
        self.assertIsInstance(result, dict)
        self.assertEqual(result, d)

    def test_empty_list_returns_empty_ordereddict(self):
        result = base.parse_parameters_collection([], 'params', 
                                                  ParseParametersCollectionDummyInstance())
        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(len(result), 0)

    def test_list_of_xml_elements(self):
        xml = """
        <root>
            <Parameter name="alpha">A</Parameter>
            <Parameter name="beta">B</Parameter>
        </root>
        """
        elem = ET.fromstring(xml)
        params = list(elem)
        result = base.parse_parameters_collection(params, 'params', 
                                                  ParseParametersCollectionDummyInstance())
        self.assertIsInstance(result, OrderedDict)
        self.assertEqual(result['alpha'], 'A')
        self.assertEqual(result['beta'], 'B')

    def test_list_of_xml_elements_empty_text(self):
        xml = """
        <root>
            <Parameter name="alpha"></Parameter>
            <Parameter name="beta"> </Parameter>
        </root>
        """
        elem = ET.fromstring(xml)
        params = list(elem)
        result = base.parse_parameters_collection(params, 'params', 
                                                  ParseParametersCollectionDummyInstance())
        self.assertIsInstance(result, OrderedDict)
        self.assertIsNone(result['alpha'])
        self.assertIsNone(result['beta'])

    def test_list_of_incompatible_type_raises(self):
        with self.assertRaisesRegex(TypeError, r"Field params of list type " + \
                                    "functionality belonging to class " + \
                                    "ParseParametersCollectionDummyInstance " + \
                                    "got a list containing first element of " + \
                                    "incompatible type <class 'int'>.$"):
            base.parse_parameters_collection([1, 2], 'params', 
                                             ParseParametersCollectionDummyInstance())

    def test_incompatible_type_raises(self):
        with self.assertRaisesRegex(TypeError, r"Field params of class " + \
                                    "ParseParametersCollectionDummyInstance " + \
                                    "got incompatible type <class 'str'>.$"):
            base.parse_parameters_collection("not_a_list_or_dict", 'params', 
                                             ParseParametersCollectionDummyInstance())

