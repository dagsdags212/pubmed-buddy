import re


class FormatError(Exception):
    """Custom exception for invalid PMID/PMCID formats."""

    pass


def validate_pmid(pmid: str) -> str:
    """Validates the format of a given PMID.

    Returns the same PMID as a string if it is valid.
    Otherwise, a ValueError is raised.
    """
    pmid_re = r"\d{8}"
    match = re.search(pmid_re, pmid)
    if match:
        return match.group(0)
    raise FormatError("Invalid PMID: format should follow XXXXXXXX")


def validate_pmcid(pmcid: str) -> str:
    """Validates the format of a given PMCID.

    Returns the same PMCID as a string if it is valid.
    Otherwise, a ValueError is raised.
    """
    pmcid_re = r"^PMC\d{7}"
    match = re.search(pmcid_re, pmcid)
    if match:
        return match.group(0)
    raise FormatError("Invalid PMCID: format should follow PMCXXXXXXX")
