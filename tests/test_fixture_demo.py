"""演示自定义fixture。"""

import pytest


@pytest.fixture
def sample_data():
    """提供测试用的示例数据。"""
    return {"name": "kylehelps", "age": 25}


def test_use_fixture(sample_data):
    """使用fixture的测试。"""
    assert sample_data["name"] == "kylehelps"
    assert sample_data["age"] == 25


def test_modify_fixture(sample_data):
    """每个测试拿到的是独立的fixture副本。"""
    sample_data["name"] = "changed"
    assert sample_data["name"] == "changed"


def test_fixture_independent(sample_data):
    """另一个测试拿到的是原始数据。"""
    assert sample_data["name"] == "kylehelps"
