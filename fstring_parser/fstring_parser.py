from datetime import datetime
import re
from copy import copy
from functools import partial
from typing import Optional


dt_format_to_regex = {symbol: "[0-9]{2}" for symbol in "ymdIMSUW"}
dt_format_to_regex.update({"-" + symbol: "[0-9]{1,2}" for symbol in "ymdIMS"})

dt_format_to_regex.update(
    {
        "Y": "[0-9]{4}",
        "H": "[0-9]{1,2}",
        "B": "[January|February|March|April|May|June|July|August|September|October|November|December]",
        "b": "[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]",
        "f": "[0-9]{6}",
        "p": "[AM|PM]",
        "z": "[+|-][0-9]{4}",
        "j": "[0-9]{3}",
        "-j": "[0-9]{1,3}",
    }
)


def get_regex_for_datetime_format(_format):
    regex = copy(_format)
    for k, v in dt_format_to_regex.items():
        regex = regex.replace(f"%{k}", v)
    return regex


def construct_parser(
    x,
    align: Optional[str] = None,
    plus_minus: Optional[str] = None,
    length: Optional[str] = None,
    comma: Optional[str] = None,
    precision: Optional[str] = None,
    dtype: Optional[str] = None,
):
    if align is not None and len(align) == 2:
        fill, align = align
    else:
        fill = None
    if length is not None:
        if align in (">", None):
            x = x.lstrip(fill)
        elif align == "<":
            x = x.rstrip(fill)
        else:  # align == "^"
            x = x.strip(fill)
    if comma:
        x = x.replace(",", "")
    if dtype in ("d", "n"):
        x = int(x)
    elif dtype in ("f", "e"):
        x = float(x)
    elif comma or plus_minus:
        if "." in x:
            x = float(x)
        else:
            x = int(x)
    return x


def construct_regex(
    align: Optional[str] = None,
    plus_minus: Optional[str] = None,
    length: Optional[str] = None,
    comma: str = "",
    precision: Optional[str] = None,
    dtype: Optional[str] = None,
):
    """

    Parameters
    ----------
    align : str, optional
        An alignment character ("<", "^", or ">") optionally preceded by a fill character.
    plus_minus : str, optional
        "+" or "-". Indicates styling and implicitly indicates that the string is numeric.
    length : str, optional
        Must be a numeric string. Indicates the length of the string.
    comma : {"", ","}
        "," indicates that numbers >= 1000 should use comma styling
    precision : str, optional
        A period followed by number, indicating the number of decimal places to use.
    dtype : {None, "d", "n", "f", "e"}
        The data type.

    Returns
    -------
    str

    """
    if not (dtype or comma or plus_minus):  # could be a string. Do not impose any form.
        return fr".{{{length or '+'}}}"

    if align is not None and len(align) == 2:
        fill, align = align
        fill = re.escape(fill)
    else:
        fill = r"\s"

    regex = ""
    if align is not None and align in "^>" or (length and align != "<"):
        regex += fill + "*"
    if plus_minus == "+":
        regex += r"[\+-]" + "?"
    else:
        regex += r"-?"
    if comma:
        regex += "[0-9,]+"
    else:
        regex += "[0-9]+"
    if precision:
        regex += rf"\.[0-9]{{,{precision[1:]}}}"
    elif dtype == "f":
        regex += rf"\.[0-9]{{,6}}"
    elif dtype not in ("d", "n", "e"):
        regex += rf"(\.[0-9]{{,6}})?"
    if dtype == "e":
        regex += rf"\.[0-9]+e[+-][0-9]{{{2}}}"
    if align is not None and align in "<^":
        regex += re.escape(fill) + "*"
    return regex


def get_entry_regex_pattern_and_parser(format_):
    # first try numeric or string
    match = re.match(
        r"^(?P<align>.?[<^>])?"
        r"(?P<plus_minus>[+-])?"
        r"(?P<length>\d+)?"
        r"(?P<comma>,)?"
        r"(?P<precision>\.\d+)?"
        r"(?P<dtype>[dnfe])?$",
        format_,
    )
    if match:
        p = match.groupdict()
        return construct_regex(**p), partial(construct_parser, **p)
    if "%Y" in format_:  # then try datetime
        return get_regex_for_datetime_format(format_), lambda x: datetime.strptime(x, format_)
    raise NotImplementedError(f"format '{format}' does not match any of the implemented patterns.")


def generate_regex_and_parsers_from_fstring(fstring: str):
    # Find all group names in the filename pattern. Exclude closing bracket as a possible character to get atomic
    # matches.
    entries = re.findall(r"{([^}]*)}", fstring)

    # Replace each group name in the pattern with a named capture group pattern.
    regex_pattern = f"^{re.escape(fstring)}$"

    parser_dict = dict()

    for entry in set(entries):
        if ":" in entry:
            label, format_ = entry.split(":")
            entry_regex, entry_parser = get_entry_regex_pattern_and_parser(format_)
            parser_dict[label] = entry_parser
        else:
            label = entry
            entry_regex = ".+"
            parser_dict[label] = lambda x: x
        regex_pattern = regex_pattern.replace(re.escape(f"{{{entry}}}"), rf"(?P<{label}>{entry_regex})", 1)
    # Replace subsequent occurrences with reference to appropriate capture group pattern
    for entry in set(entries):
        if ":" in entry:
            label, format_ = entry.split(":")
        else:
            label = entry
        regex_pattern = regex_pattern.replace(re.escape(f"{{{entry}}}"), rf"(?P={label})")
    return regex_pattern, parser_dict


class FstringParser:
    def __init__(self, fstring: str):
        self.pattern, self.parser_dict = generate_regex_and_parsers_from_fstring(fstring)
        print(self.pattern)

    def __call__(self, string: str):
        print(string)
        self.match = re.match(self.pattern, string)
        if self.match is None:
            return None
        return {
            k: self.parser_dict[k](v) for k, v in self.match.groupdict().items()
        }


def parse_fstring(fstring: str, string: str):
    return FstringParser(fstring)(string)
