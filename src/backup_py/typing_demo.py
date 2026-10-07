"""类型注解演示。"""


def greet(name: str) -> str:
    """返回问候语。"""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """两数相加。"""
    return a + b


def divide(a: float, b: float) -> float | None:
    """除法，除数为0返回None。"""
    if b == 0:
        return None
    return a / b


def process_names(names: list[str]) -> dict[str, int]:
    """统计每个名字的长度。"""
    return {name: len(name) for name in names}


def find_user(user_id: int) -> dict[str, str] | None:
    """查找用户，找不到返回None。"""
    users = {
        1: {"name": "kylehelps", "age": "25"},
        2: {"name": "alice", "age": "30"},
    }
    return users.get(user_id)
