"""演示mock用法。"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time


def test_mock_basic():
    """基础mock。"""
    mock_obj = MagicMock()
    mock_obj.get_name.return_value = "kylehelps"

    result = mock_obj.get_name()

    assert result == "kylehelps"
    mock_obj.get_name.assert_called_once()


def fetch_data_from_api(url: str) -> dict:
    """假装从API获取数据。"""
    return {"data": "real"}


@patch("test_mock_demo.fetch_data_from_api")
def test_with_patch(mock_fetch):
    """用patch替换函数。"""
    mock_fetch.return_value = {"data": "mocked"}

    result = fetch_data_from_api("http://example.com")

    assert result == {"data": "mocked"}
    mock_fetch.assert_called_once_with("http://example.com")


def get_current_year() -> int:
    """获取当前年份。"""
    return datetime.now(timezone.utc).year


@freeze_time("2020-01-01")
def test_get_current_year():
    """用freezegun冻结时间。"""
    result = get_current_year()
    assert result == 2020


@patch("test_mock_demo.fetch_data_from_api")
def test_call_assertions(mock_fetch):
    """测试mock的调用断言。"""
    mock_fetch.return_value = {"data": "x"}

    fetch_data_from_api("http://a.com")
    fetch_data_from_api("http://b.com")

    assert mock_fetch.call_count == 2
    mock_fetch.assert_any_call("http://a.com")
    mock_fetch.assert_any_call("http://b.com")


@pytest.mark.parametrize(
    "user_id, expected",
    [
        (1, "User_1"),
        (2, "User_2"),
        (100, "User_100"),
    ],
)
@patch("test_mock_demo.fetch_data_from_api")
def test_param_with_mock(mock_fetch, user_id, expected):
    """参数化+mock组合。"""
    mock_fetch.return_value = {"name": expected}

    result = fetch_data_from_api(f"http://example.com/{user_id}")

    assert result["name"] == expected
    mock_fetch.assert_called_once_with(f"http://example.com/{user_id}")
