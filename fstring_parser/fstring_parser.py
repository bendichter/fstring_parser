from datetime import datetime
import re
from copy import copy

dt_format_to_regex = {symbol: "[0-9]{2}" for symbol in "ymdIMS"}
dt_format_to_regex.update({"-" + symbol: "[0-9]{1,2}" for symbol in "ymdIMS"})
dt_format_to_regex.update(
    Y="[0-9]{4}",
    H="[0-9]{1,2}",
    B="[January|February|March|April|May|June|July|August|September|October|November|December]",
    b="[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]",
    f="[0-9]{6}",
    p="[AM|PM]",
    z="[+|-][0-9]{4}",
)


def get_regex_for_datetime_format(_format):
    regex = copy(_format)
    for k, v in dt_format_to_regex.items():
        regex = regex.replace(f"%{k}", v)
    return regex


def get_entry_regex_pattern_and_parser(_format):
    if re.match(r"^[<^>]?(?P<n>\d+)$", _format):  # x:5, x:<5, x:^5, x:>5,
        p = re.match(r"[<^>]?(?P<n>\d+)$", _format).groupdict()
        return fr".{{{p['n']}}}", lambda x: x.strip()
    if re.match(",", _format):  # x:,
        return "-?[0-9|,]+", lambda x: int(x.replace(",", ""))
    if re.match(".[<^>][0-9]+", _format):  # x:=5
        return f".{{{_format[2:]}}}", lambda x: x.replace(_format[0], "")
    if re.match("^[d|n]$", _format):  # x:n
        return r"-?[0-9|\.]+", lambda x: int(x.replace(",", "").replace(".", ""))
    if re.match("^[0-9]+[d|n]$", _format):  #5n
        return fr"(?=[\d\s]{{{_format[:-1]}}})\s*\d*", lambda x: int(x.strip())
    if _format == "f":  # x:f
        return r"-?[0-9|\.]+", lambda x: float(x)
    if re.match("[0-9]+f", _format):  # x:5f
        return r"-?[0-9|\.]+", lambda x: float(x.strip())
    if re.match(r"\.\d+f", _format):  # x:.5f
        return rf"-?[0-9]*\.[0-9]{{{_format[1:-1]}}}", lambda x: float(x)
    if re.match(r",\.[0-9]+f", _format):  # x:,.5f
        return rf"-?[0-9|,]*\.[0-9]{{{_format[1:-1]}}}", lambda x: float(x.replace(",", ""))
    if "%Y" in _format:  # x:%Y-%m-%dT%H-%M-%S
        return get_regex_for_datetime_format(_format), lambda x: datetime.strptime(x, _format)
    raise NotImplementedError(f"format '{format}' does not match any of the implemented patterns.")


def generate_regex_and_parsers_from_fstring(fstring: str):
    # Find all group names in the filename pattern
    entries = re.findall(r"{(.*)}", fstring)

    # Replace each group name in the pattern with a named capture group pattern
    regex_pattern = f"^{re.escape(fstring)}$"

    parser_dict = dict()

    for entry in set(entries):

        if ":" in entry:
            label, _format = entry.split(":")
            entry_regex, entry_parser = get_entry_regex_pattern_and_parser(_format)
            parser_dict[label] = entry_parser
        else:
            label = entry
            entry_regex = ".+"
        regex_pattern = regex_pattern.replace(re.escape(f"{{{entry}}}"), rf"(?P<{label}>{entry_regex})", 1)

    # Replace subsequent occurrences with reference to appropriate capture group pattern
    for entry in set(entries):
        label, _format = entry.split(":")
        regex_pattern = regex_pattern.replace(re.escape(f"{{{entry}}}"), rf"(?P={label})")

    return regex_pattern, parser_dict


class FstringParser:
    def __init__(self, fstring: str):
        self.pattern, self.parser_dict = generate_regex_and_parsers_from_fstring(fstring)

    def __call__(self, string: str):
        self.match = re.match(self.pattern, string)

        if self.match is None:
            return None
        return {
            k: self.parser_dict[k](v) for k, v in self.match.groupdict().items()
        }


def parse_fstring(fstring: str, string: str):
    return FstringParser(fstring)(string)
