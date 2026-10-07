"""演示参数化测试的多种写法。"""

import pytest


def add(a: int, b: int) -> int:
    """两数相加。"""
    return a + b


# ========== 写法1：字符串参数名（最常用） ==========
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_add_string_params(a, b, expected):
    """写法1：字符串参数名。"""
    assert add(a, b) == expected


# ========== 写法2：列表参数名 ==========
@pytest.mark.parametrize(
    ["a", "b", "expected"],
    [
        (1, 2, 3),
        (10, 20, 30),
    ],
)
def test_add_list_params(a, b, expected):
    """写法2：列表参数名。"""
    assert add(a, b) == expected


# ========== 写法3：单参数 ==========
@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_is_positive(value):
    """写法3：单参数。"""
    assert value > 0


# ========== 写法4：带ID的参数 ==========
@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(1, 2, 3, id="small"),
        pytest.param(0, 0, 0, id="zero"),
        pytest.param(100, 200, 300, id="large"),
        pytest.param(-5, -3, -8, id="negative"),
    ],
)
def test_add_with_id(a, b, expected):
    """写法4：带ID的参数。"""
    assert add(a, b) == expected
