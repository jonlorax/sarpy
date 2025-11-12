from collections import OrderedDict
import pytest
import re
import unittest
from uuid import UUID, uuid4

from sarpy.annotation.base import GeometryProperties, AnnotationProperties, AnnotationFeature, AnnotationCollection, FileAnnotationCollection
from sarpy.geometry.geometry_elements import Jsonable

class test_geometryproperties(unittest.TestCase):
    def test_geometryproperties_default_uid(self):
        # confirms that a uuid is generated if one isn't provided
        geom = GeometryProperties()
        self.assertIsInstance(geom.uid, str)

        try:
            UUID(geom.uid)
        except:
            pytest.fail("The generated uid is not a valid UUID string")

    def test_geometryproperties_custom_uid(self):
        # confirms that that the uid setter works as expected
        custom_uid = "abcd"
        geom = GeometryProperties(uid=custom_uid)
        self.assertEquals(geom.uid, custom_uid)

    def test_geometryproperties_invalid_uid(self):
        custom_uid = 1234
        with pytest.raises(TypeError, 
                            match = re.escape("uid must be a string")):
            geom = GeometryProperties(uid=custom_uid)

    def test_geometryproperties_default_name(self):
        geom = GeometryProperties()
        self.assertIsNone(geom.name)

    def test_geometryproperties_custom_name(self):
        custom_name = "abcd"
        geom = GeometryProperties(name=custom_name)
        self.assertEquals(geom.name, custom_name)

    def test_geometryproperties_invalid_name(self):
        custom_name = 1234
        with pytest.raises(TypeError, 
                            match = re.escape("Got unexpected type for name")):
            geom = GeometryProperties(name=custom_name)

    def test_geometryproperties_default_color(self):
        geom = GeometryProperties()
        self.assertIsNone(geom.color)

    def test_geometryproperties_custom_color(self):
        custom_color = "abcd"
        geom = GeometryProperties(color=custom_color)
        self.assertEquals(geom.color, custom_color)

    def test_geometryproperties_invalid_color(self):
        custom_color = 1234
        with pytest.raises(TypeError, 
                            match = re.escape("Got unexpected type for color")):
            geom = GeometryProperties(color=custom_color)

    def test_geometryproperties_all_fields(self):
        # makes sure that GeomeryProperties is able to be initialized properly with all three parameters passed
        geom = GeometryProperties(uid="abcd", name="efgh", color="blue")

        self.assertEquals(geom.uid, "abcd")
        self.assertEquals(geom.name, "efgh")
        self.assertEquals(geom.color, "blue")

    def test_from_dict_valid_data(self):
        data = {
            "type": GeometryProperties._type,
            "uid": "abcd",
            "name": "efgh",
            "color": "red"
        }

        geom = GeometryProperties.from_dict(data)

        self.assertIsInstance(geom, GeometryProperties)
        self.assertEquals(geom.uid, "abcd")
        self.assertEquals(geom.name, "efgh")
        self.assertEquals(geom.color, "red")

    def test_from_dict_missing_type(self):
        # confirms that an error is raised if the dict is missing type
        bad_data = {
            "uid": "abcd",
            "name": "efgh",
            "color": "red"
        }

        with pytest.raises(KeyError,
                            match = re.escape("the json requires the field 'type'")):
            geom = GeometryProperties.from_dict(bad_data)
    
    def test_from_dict_missing_type(self):
        # confirms that an error is raised if the dict is missing type
        bad_data = {
            "type": "string",
            "uid": "abcd",
            "name": "efgh",
            "color": "red"
        }

        with pytest.raises(ValueError, 
                            match = re.escape("GeometryProperties cannot be constructed from {'type': 'string', 'uid': 'abcd', 'name': 'efgh', 'color': 'red'}")):
            geom = GeometryProperties.from_dict(bad_data)

    def test_to_dict_geometryproperties_w_values(self):
        # confirms that the to_dict() function works as expected and includes all of the attributes in a dictionary 
        geom_dict = GeometryProperties(uid="abcd", name="efgh", color="blue").to_dict()

        self.assertIsInstance(geom_dict, dict)
        self.assertEquals(geom_dict["uid"], "abcd")
        self.assertEquals(geom_dict["name"], "efgh")
        self.assertEquals(geom_dict["color"], "blue")

    def test_to_dict_geometryproperties_exclude_none_fields(self):
        # confirms that None fields are excluded
        geom_dict = GeometryProperties(uid="abcd", name=None, color=None).to_dict()
        
        self.assertIsInstance(geom_dict, dict)
        self.assertEquals(geom_dict["uid"], "abcd")
        self.assertNotIn("name", geom_dict)
        self.assertNotIn("color", geom_dict)

    def test_to_dict_w_parent_dict(self):
        # confirms that the to_dict() function works with a parent_dict passed
        parent_dict = OrderedDict([("key", "value")])

        geom_dict = GeometryProperties(uid="abcd", name="efgh", color="blue").to_dict(parent_dict)

        self.assertEquals(geom_dict["key"], "value")
        self.assertEquals(geom_dict["uid"], "abcd")
        self.assertEquals(geom_dict["name"], "efgh")
        self.assertEquals(geom_dict["color"], "blue")

@pytest.fixture
def geometry_data():
    # return {"type": "GeometryProperties",
    #         "uid": str(uuid4()),
    #         "name": "apple",
    #         "color": "red"}
    return {
            "type": GeometryProperties._type,
            "uid": "abcd",
            "name": "efgh",
            "color": "red"
        }
    
@pytest.fixture
def geometryproperties_obj():
    return GeometryProperties.from_dict(geometry_data)

class test_annotationproperties(unittest.TestCase):
    def test_annotationproperties_default_initialization(self):
        obj = AnnotationProperties()

        self.assertIsNone(obj.name)
        self.assertIsNone(obj.description)
        self.assertIsNone(obj.directory)
        self.assertEquals(obj.geometry_properties, [])
        self.assertIsNone(obj.parameters)

    def test_annotationproperties_initialization_w_values(self):
        obj = AnnotationProperties(
            name = "annotation1",
            description = "abcd",
            directory = "path/folder",
            geometry_properties = [geometryproperties_obj],
            parameters = Jsonable()
        )

        self.assertEquals(obj.name, "annotation1")
        self.assertEquals(obj.description, "abcd")
        self.assertEquals(obj.directory, "path/folder")
        self.assertIsInstance(obj.geometry_properties, GeometryProperties)
        self.assertIsInstance(obj.parameters, Jsonable)

    def test_from_dict_valid_input(self):
        data = {
            "type": "AnnotationProperties",
            "name": "annotation1",
            "description": "abcd",
            "directory": "path/folder",
            "geometry_properties": [geometry_data],
            "parameters": None
        }
        
        obj = AnnotationProperties.from_dict(data)

        self.assertIsInstance(obj, AnnotationProperties)
        self.assertEquals(obj.name, "annotation1")
        self.assertEquals(obj.description, "abcd")
        self.assertEquals(obj.directory, "path/folder")
        self.assertEquals(len(obj.geometry_properties), 1)
