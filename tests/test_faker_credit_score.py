#  -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import re

from faker import Faker
from faker_credit_score import CreditScore


class TestEnUS(unittest.TestCase):
    def setUp(self):
        self.fake = Faker("en_US")
        self.fake.add_provider(CreditScore)
        Faker.seed(0)

    def test_failure_scenario_credit_score_nonexistent_provider(self):
        with self.assertRaises(KeyError):
            credit_score = self.fake.credit_score("nonexistent")

    def test_failure_scenario_credit_score_provider_nonexistent_provider(self):
        with self.assertRaises(KeyError):
            credit_score_provider = self.fake.credit_score_provider("nonexistent")

    def test_failure_scenario_credit_score_name_nonexistent_provider(self):
        with self.assertRaises(KeyError):
            credit_score_name = self.fake.credit_score_name("nonexistent")

    def test_failure_scenario_credit_score_full_nonexistent_provider(self):
        with self.assertRaises(KeyError):
            credit_score_full = self.fake.credit_score_full("nonexistent")

    def test_random_credit_score(self):
        for _ in range(100):
            credit_score = self.fake.credit_score()
            assert 300 <= credit_score <= 850

    def test_credit_score_of_a_specific_type(self):
        for _ in range(100):
            credit_score = self.fake.credit_score("fico8")
            assert 300 <= credit_score <= 850

    def test_random_credit_score_provider(self):
        for _ in range(100):
            provider = self.fake.credit_score_provider()
            assert provider in ("FICO", "Experian", "Equifax", "TransUnion")

    def test_credit_score_provider_of_a_specific_type(self):
        for _ in range(100):
            provider = self.fake.credit_score_provider("fico5")
            assert provider == "Equifax"

    def test_random_credit_score_name(self):
        for _ in range(100):
            name = self.fake.credit_score_name()
            assert name in (
                "FICO Score 8",
                "Equifax Beacon 5.0",
                "Experian/Fair Isaac Risk Model V2SM",
                "TransUnion FICO Risk Score, Classic 04",
                "VantageScore 3.0",
                "FICO Score 10",
                "FICO Score 10 T",
            )

    def test_credit_score_name_of_a_specific_type_fico5(self):
        for _ in range(100):
            name = self.fake.credit_score_name("fico5")
            assert name == "Equifax Beacon 5.0"

    def test_credit_score_name_of_a_specific_type_fico2(self):
        for _ in range(100):
            name = self.fake.credit_score_name("fico2")
            assert name == "Experian/Fair Isaac Risk Model V2SM"

    def test_credit_score_name_of_a_specific_type_fico4(self):
        for _ in range(100):
            name = self.fake.credit_score_name("fico4")
            assert name == "TransUnion FICO Risk Score, Classic 04"

    def test_random_credit_score_full(self):
        """ Output looks like this (provider, model, and credit score are random):
        Equifax Beacon 5.0
        Equifax
        660
        """
        for _ in range(100):
            output = self.fake.credit_score_full()
            assert re.match(r".+\n.+\n\d{3}\n", output)

    def test_credit_score_full_of_a_specific_type(self):
        """ Output looks like this (credit score is random):
        Equifax Beacon 5.0
        Equifax
        660
        """
        for _ in range(100):
            output = self.fake.credit_score_full("fico5")
            assert re.match(r"Equifax Beacon 5\.0\nEquifax\n\d{3}\n", output)
