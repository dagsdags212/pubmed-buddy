from pytest import raises
from pmbuddy.util.validation import (
    FormatError,
    validate_pmid,
    validate_pmcid,
)


class TestValidation:
    valid_pmid = "12345678"
    invalid_pmid = "3891GH12"
    valid_pmcid = "PMC1234567"
    invalid_pmcid = "PM1029384"

    def test_pmid_validation(self):
        assert validate_pmid(self.valid_pmid) == self.valid_pmid
        with raises(FormatError):
            validate_pmid(self.invalid_pmid)

    def test_pmcid_validation(self):
        assert validate_pmcid(self.valid_pmcid) == self.valid_pmcid
        with raises(FormatError):
            validate_pmcid(self.invalid_pmcid)
