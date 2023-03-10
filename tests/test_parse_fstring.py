from fstring_parser import parse_fstring
from datetime import datetime


def test_5():
    x = 55
    assert parse_fstring("abc{x:5}abc", f"abc{x:5}abc") == {'x': '55'}


def test_s():
    x = "55"
    assert parse_fstring("abc{x:s}abc", f"abc{x:s}abc") == {'x': '55'}


def test_5comma():
    x=5555555
    assert parse_fstring("abc{x:,}abc", f"abc{x:,}abc") == {'x': 5555555}


def test_5comma_underscore():
    x=5555555
    assert parse_fstring("abc{x:_}abc", f"abc{x:_}abc") == {'x': 5555555}


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


def test_05():
    x = 55
    assert parse_fstring("abc{x:05n}abc", f"abc{x:05n}abc") == dict(x=55)


def test_15():
    x = 55
    assert parse_fstring("abc{x:15n}abc", f"abc{x:15n}abc") == dict(x=55)


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


def test_pi():
    num5 = 3.141592653589793
    assert parse_fstring(
        "Pi is approximately equal to {num5:.2f}",
        f"Pi is approximately equal to {num5:.2f}"
    ) == dict(num5=3.14)


def test_exponential():
    num6 = 0.000000000003141592653589793
    assert parse_fstring(
        "Pi in scientific notation: {num6:e}",
        f"Pi in scientific notation: {num6:e}",
    ) == dict(num6=0.000000000003141593)


def test_exponential_with_precision():
    num6 = 0.000000000003141592653589793
    assert parse_fstring(
        "Pi in scientific notation: {num6:e}",
        f"Pi in scientific notation: {num6:.2e}",
    ) == dict(num6=0.00000000000314)


def test_binary():
    num2 = 42
    assert parse_fstring("Number in binary: {num2:b}", f"Number in binary: {num2:b}") == dict(num2=42)


def test_hexadecimal():
    num2 = 42
    assert parse_fstring("Number in hex: {num2:x}", f"Number in hex: {num2:x}") == dict(num2=42)


def test_hexadecimal_alt():
    num2 = 42
    assert parse_fstring("Number in hex: {num2:#x}", f"Number in hex: {num2:#x}") == dict(num2=42)



def test_hexadecimal_upper():
    num2 = 42
    assert parse_fstring("Number in hex: {num2:X}", f"Number in hex: {num2:X}") == dict(num2=42)


def test_octal():
    num2 = 42
    assert parse_fstring("Number in octal: {num2:o}", f"Number in octal: {num2:o}") == dict(num2=42)


def test_octal_alt():
    num2 = 42
    assert parse_fstring("Number in octal: {num2:#o}", f"Number in octal: {num2:#o}") == dict(num2=42)


def test_double_braces():
    num2 = 42
    assert parse_fstring(
        "Number in {{hello}}: {num2:n}",
        f"Number in {{hello}}: {num2:n}") == dict(num2=42)


def test_triple_braces():
    num2 = 42
    assert parse_fstring(
        "Number in: {{{num2:n}}}",
        f"Number in: {{{num2:n}}}") == dict(num2=42)


def test_fstring_parser():
    num2 = 42
    assert parse_fstring(
        "Number in octal: {num2:#o}",
        f"Number in octal: {num2:#o}",
        transform=False,
    ) == dict(num2="0o52")
