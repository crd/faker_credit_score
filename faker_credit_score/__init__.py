# coding=utf-8
from __future__ import unicode_literals
from collections import OrderedDict

from faker.providers import BaseProvider


class CreditScoreObject(object):
    """ Credit Score Object that uses fico8 as a sensible default. """

    def __init__(
        self,
        name="FICO Score 8",
        providers=("Equifax", "Experian", "TransUnion"),
        score_range=(300, 850),
    ):
        self.name = name
        self.providers = providers
        self.score_range = score_range


class Provider(BaseProvider):

    # FICO 8 Score is the most widely-used non-industry specific credit score model,
    # followed by 5, 2, and 4 as per https://www.myfico.com/credit-education/credit-scores/fico-score-versions
    #
    # Ranges obtained here and validated elsewhere:
    #
    # * https://blog.myfico.com/whats-a-good-credit-score-range/
    # * https://www.wrightrealtors.com/home/credit-score.htm

    # List of credit score types with names, providers, and ranges
    credit_score_data = [
        ("fico2", "Experian/Fair Isaac Risk Model V2SM", ("Experian",), (320, 844)),
        ("fico4", "TransUnion FICO Risk Score, Classic 04", ("TransUnion",), (309, 839)),
        ("fico5", "Equifax Beacon 5.0", ("Equifax",), (334, 818)),
        ("fico8", "FICO Score 8", ("Equifax", "Experian", "TransUnion"), (300, 850)),
        ("fico9", "FICO Score 8", ("Equifax", "Experian", "TransUnion"), (300, 850)),
        ("fico10", "FICO Score 10", ("Equifax", "Experian", "TransUnion"), (300, 850)),             # based on FICO 8
        ("fico10t", "FICO Score 10 T", ("Equifax", "Experian", "TransUnion"), (300, 850)),          # based on FICO 8
        ("ultrafico", "UltraFICO", ("Experian",), (300, 850)),                                      # based on FICO 8
        ("vantageScore3", "VantageScore 3.0", ("Equifax", "Experian", "TransUnion"), (300, 850)),   # based on FICO 8
        ("vantageScore4", "VantageScore 4.0", ("Equifax", "Experian", "TransUnion"), (300, 850))    # based on FICO 8
    ]

    # Construct the OrderedDict
    credit_score_types = OrderedDict(
        (key, CreditScoreObject(name, providers, score_range))
        for key, name, providers, score_range in credit_score_data
    )

    # Add alias for FICO to map to FICO 8
    credit_score_types["fico"] = credit_score_types["fico8"]

    def credit_score_name(self, score_type=None):
        """ Returns the name of the credit score. """
        if score_type is None:
            score_type = self.random_element(self.credit_score_types.keys())
        return self._credit_score_type(score_type).name

    def credit_score_provider(self, score_type=None):
        """ Returns the name of the credit score provider. """
        if score_type is None:
            score_type = self.random_element(self.credit_score_types.keys())
        return self.random_element(self._credit_score_type(score_type).providers)

    def credit_score(self, score_type=None):
        """ Returns a valid credit score. """
        credit_score_summary = self._credit_score_type(score_type)
        score = self._generate_credit_score(credit_score_summary.score_range)
        return score

    def credit_score_full(self, score_type=None):
        """ Returns a tuple representation of a valid credit score. """
        credit_score_summary = self._credit_score_type(score_type)

        tpl = "{name}\n" "{provider}\n" "{credit_score}\n"

        tpl = tpl.format(
            name=self.credit_score_name(credit_score_summary),
            provider=self.credit_score_provider(credit_score_summary),
            credit_score=self.credit_score(credit_score_summary),
        )
        return self.generator.parse(tpl)

    def _credit_score_type(self, score_type=None):
        """ Returns a credit score type instance of the specified type (random if none provided). """
        if score_type is None:
            score_type = self.random_element(self.credit_score_types.keys())
        elif isinstance(score_type, CreditScoreObject):
            return score_type
        return self.credit_score_types[score_type]

    def _generate_credit_score(self, credit_score_range):
        """ Returns an integer within the range specified by credit_score_range. """
        return self.random_int(*credit_score_range)


CreditScore = Provider
