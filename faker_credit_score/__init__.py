# coding=utf-8
from __future__ import unicode_literals
from collections import OrderedDict, namedtuple

from faker.providers import BaseProvider

class CreditScoreResult(namedtuple("CreditScoreResult", ["name", "provider", "score"])):
    """ A credit score result with name, provider, and score fields. """

    def __str__(self):
        return f"{self.name}\n{self.provider}\n{self.score}"


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
        ("fico9", "FICO Score 9", ("Equifax", "Experian", "TransUnion"), (300, 850)),
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

    credit_score_tiers = OrderedDict([
        ("poor", (300, 579)),
        ("fair", (580, 669)),
        ("good", (670, 739)),
        ("very_good", (740, 799)),
        ("exceptional", (800, 850)),
    ])

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

    def credit_score(self, score_type=None, tier=None):
        """ Returns a valid credit score, optionally constrained to a tier. """
        credit_score_summary = self._credit_score_type(score_type)
        if tier is not None:
            if tier not in self.credit_score_tiers:
                raise ValueError(
                    f"Unknown tier '{tier}'. "
                    f"Valid tiers: {', '.join(self.credit_score_tiers)}"
                )
            tier_low, tier_high = self.credit_score_tiers[tier]
            model_low, model_high = credit_score_summary.score_range
            effective_low = max(tier_low, model_low)
            effective_high = min(tier_high, model_high)
            if effective_low > effective_high:
                raise ValueError(
                    f"Tier '{tier}' has no valid scores for "
                    f"score type '{credit_score_summary.name}'"
                )
            return self._generate_credit_score((effective_low, effective_high))
        return self._generate_credit_score(credit_score_summary.score_range)

    def credit_score_full(self, score_type=None, tier=None):
        """ Returns a CreditScoreResult namedtuple with name, provider, and score fields. """
        credit_score_summary = self._credit_score_type(score_type)
        return CreditScoreResult(
            name=self.credit_score_name(credit_score_summary),
            provider=self.credit_score_provider(credit_score_summary),
            score=self.credit_score(credit_score_summary, tier=tier),
        )

    def credit_score_tier(self, score=None):
        """Returns a credit score tier.

        Random (uniform across tier names) if no score provided,
        otherwise classifies the given score.
        """
        if score is None:
            return self.random_element(list(self.credit_score_tiers.keys()))
        for tier_name, (low, high) in self.credit_score_tiers.items():
            if low <= score <= high:
                return tier_name
        raise ValueError(
            f"Score {score} is outside the valid range "
            f"({next(iter(self.credit_score_tiers.values()))[0]}-"
            f"{list(self.credit_score_tiers.values())[-1][1]})"
        )

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
