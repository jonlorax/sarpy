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
    geom = GeometryProperties(name = custom_name)
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
    geom = GeometryProperties(color = custom_color)
    assert geom.color == custom_color

def test_geometryproperties_invalid_color():
    custom_color = 1234
    with pytest.raises(TypeError, 
                        match = re.escape("Got unexpected type for color")):
        geom = GeometryProperties(color=custom_color)