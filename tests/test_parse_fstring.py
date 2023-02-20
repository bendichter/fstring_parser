from fstring_parser import parse_fstring, FstringParser
from datetime import datetime


def test_5():
    x = 55
    assert parse_fstring("abc{x:5}abc", f"abc{x:5}abc") == {'x': '55'}


def test_5comma():
    x=5555555
    assert parse_fstring("abc{x:,}abc", f"abc{x:,}abc") == {'x': 5555555}


def test_5n():
    x = 55
    assert parse_fstring("abc{x:5n}abc", f"abc{x:5n}abc") == dict(x=55)


def test_5d():
    x = 55
    assert parse_fstring("abc{x:5d}abc", f"abc{x:5d}abc") == dict(x=55)


def test_n():
    x = 55
    assert parse_fstring("abc{x:n}abc", f"abc{x:n}abc") == dict(x=55)


def test_gt5():
    x = 55
    assert parse_fstring("abc{x:>5}abc", f"abc{x:>5}abc") == dict(x="55")


def test_lt5():
    x = 55
    assert parse_fstring("abc{x:<5}abc", f"abc{x:<5}abc") == dict(x="55")


def test_caret5():
    x = 55
    assert parse_fstring("abc{x:^5}abc", f"abc{x:^5}abc") == dict(x="55")


def test_eqgt():
    x = 55
    assert parse_fstring("abc{x:=>5}abc", f"abc{x:=>5}abc") == dict(x="55")


def test_f():
    x = 55.0
    assert parse_fstring("abc{x:f}abc", f"abc{x:f}abc") == dict(x=55.0)


def test_5f():
    x = 55.0
    assert parse_fstring("abc{x:5f}abc", f"abc{x:5f}abc") == dict(x=55.0)


def test_dot5f():
    x = 55.0
    assert parse_fstring("abc{x:.5f}abc", f"abc{x:.5f}abc") == dict(x=55.0)


def test_datetime():
    x = datetime(2021, 3, 4, 4, 3, 2)
    assert parse_fstring("abc{x:%Y-%m-%dT%H-%M-%S}abc", f"abc{x:%Y-%m-%dT%H-%M-%S}abc") == dict(x=datetime(2021, 3, 4, 4, 3, 2))


def test_special_characters():
    x = 55
    assert parse_fstring(r".\{x:5n}abc", rf".\{x:5n}abc") == {'x': 55}


def test_special_characters2():
    x = r"\/*^"
    assert parse_fstring(r".\{x}abc", rf".\{x}abc") == {'x': r"\/*^"}


def test_multiple():
    x = 2
    y = 5
    assert parse_fstring("a{x:n}b{y:n}c{x:n}d", f"a{x:n}b{y:n}c{x:n}d") == {"x": 2, "y": 5}


def test_multiple_no_match():
    x = 2
    y = 5
    assert parse_fstring("a{x:n}b{y:n}c{x:n}d", f"a{x:n}b{y:n}c6d") is None


def test_plus_float():
    x = 2.3
    assert parse_fstring("abc{x:+}", f"abc{x:+}") == {"x": 2.3}








