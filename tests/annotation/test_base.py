from collections import OrderedDict
import pytest
import re
from uuid import UUID

from sarpy.annotation.base import GeometryProperties

def test_geometryproperties_default_uid():
    # confirms that a uuid is generated if one isn't provided
    geom = GeometryProperties()
    assert isinstance(geom.uid, str)

    try:
        UUID(geom.uid)
    except:
        pytest.fail("The generated uid is not a valid UUID string")

def test_geometryproperties_custom_uid():
    # confirms that that the uid setter works as expected
    custom_uid = "abcd"
    geom = GeometryProperties(uid=custom_uid)
    assert geom.uid == custom_uid

def test_geometryproperties_invalid_uid():
    custom_uid = 1234
    with pytest.raises(TypeError, 
                        match = re.escape("uid must be a string")):
        geom = GeometryProperties(uid=custom_uid)

def test_geometryproperties_default_name():
    geom = GeometryProperties()
    assert geom.name == None

def test_geometryproperties_custom_name():
    custom_name = "abcd"
    geom = GeometryProperties(name=custom_name)
    assert geom.name == custom_name

def test_geometryproperties_invalid_name():
    custom_name = 1234
    with pytest.raises(TypeError, 
                        match = re.escape("Got unexpected type for name")):
        geom = GeometryProperties(name=custom_name)

def test_geometryproperties_default_color():
    geom = GeometryProperties()
    assert geom.color == None

def test_geometryproperties_custom_color():
    custom_color = "abcd"
    geom = GeometryProperties(color=custom_color)
    assert geom.color == custom_color

def test_geometryproperties_invalid_color():
    custom_color = 1234
    with pytest.raises(TypeError, 
                        match = re.escape("Got unexpected type for color")):
        geom = GeometryProperties(color=custom_color)

def test_geometryproperties_all_fields():
    # makes sure that GeomeryProperties is able to be initialized properly with all three parameters passed
    geom = GeometryProperties(uid="abcd", name="efgh", color="blue")

    assert geom.uid == "abcd"
    assert geom.name == "efgh"
    assert geom.color == "blue"

def test_from_dict_valid_data():
    data = {
        "type": GeometryProperties._type,
        "uid": "abcd",
        "name": "efgh",
        "color": "red"
    }

    geom = GeometryProperties.from_dict(data)

    assert isinstance(geom, GeometryProperties)
    assert geom.uid == "abcd"
    assert geom.name == "efgh"
    assert geom.color == "red"

def test_from_dict_missing_type():
    # confirms that an error is raised if the dict is missing type
    bad_data = {
        "uid": "abcd",
        "name": "efgh",
        "color": "red"
    }

    # with pytest.raises(ValueError, 
    #                     match = re.escape("Geometry Properties cannot be constructed from")):
    geom = GeometryProperties.from_dict(bad_data)
    # key error is currently being thrown? not sure if it should be the value error as stated in the from_dict function

def test_to_dict_geometryproperties_w_values():
    # confirms that the to_dict() function works as expected and includes all of the attributes in a dictionary 
    geom_dict = GeometryProperties(uid="abcd", name="efgh", color="blue").to_dict()

    assert isinstance(geom_dict, dict)
    assert geom_dict["uid"] == "abcd"
    assert geom_dict["name"] == "efgh"
    assert geom_dict["color"] == "blue"

def test_to_dict_geometryproperties_exclude_none_fields():
    # confirms that None fields are excluded
    geom_dict = GeometryProperties(uid="abcd", name=None, color=None).to_dict()
    
    assert isinstance(geom_dict, dict)
    assert geom_dict["uid"] == "abcd"
    assert "name" not in geom_dict
    assert "color" not in geom_dict

def test_to_dict_w_parent_dict():
    # confirms that the to_dict() function works with a parent_dict passed
    parent_dict = OrderedDict([("key", "value")])

    geom_dict = GeometryProperties(uid="abcd", name="efgh", color="blue").to_dict(parent_dict)

    assert geom_dict["key"] == "value"
    assert geom_dict["uid"] == "abcd"
    assert geom_dict["name"] == "efgh"
    assert geom_dict["color"] == "blue"