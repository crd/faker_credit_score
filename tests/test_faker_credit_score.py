#  -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def fake():
    from faker import Faker
    from faker_credit_score import CreditScore

    Faker.seed(0)
    fake = Faker("en_US")
    fake.add_provider(CreditScore)

    return fake


def test_failure_scenario_credit_score_nonexistent_provider(fake):
    with pytest.raises(KeyError):
        fake.credit_score("nonexistent")


def test_failure_scenario_credit_score_provider_nonexistent_provider(fake):
    with pytest.raises(KeyError):
        fake.credit_score_provider("nonexistent")


def test_failure_scenario_credit_score_name_nonexistent_provider(fake):
    with pytest.raises(KeyError):
        fake.credit_score_name("nonexistent")


def test_failure_scenario_credit_score_full_nonexistent_provider(fake):
    with pytest.raises(KeyError):
        fake.credit_score_full("nonexistent")


def test_random_credit_score(fake):
    for _ in range(100):
        credit_score = fake.credit_score()
        assert 300 <= credit_score <= 850


def test_credit_score_of_a_specific_type(fake):
    for _ in range(100):
        credit_score = fake.credit_score("fico8")
        assert 300 <= credit_score <= 850


def test_random_credit_score_provider(fake):
    for _ in range(100):
        provider = fake.credit_score_provider()
        assert provider in ("FICO", "Experian", "Equifax", "TransUnion")


def test_credit_score_provider_of_a_specific_type(fake):
    for _ in range(100):
        provider = fake.credit_score_provider("fico5")
        assert provider == "Equifax"


def test_random_credit_score_name(fake):
    for _ in range(100):
        name = fake.credit_score_name()
        assert name in (
            "FICO Score 8",
            "FICO Score 9",
            "Equifax Beacon 5.0",
            "Experian/Fair Isaac Risk Model V2SM",
            "TransUnion FICO Risk Score, Classic 04",
            "VantageScore 3.0",
            "VantageScore 4.0",
            "FICO Score 10",
            "FICO Score 10 T",
            "UltraFICO"
        )

def test_credit_score_name_of_a_specific_type_fico5(fake):
    for _ in range(100):
        name = fake.credit_score_name("fico5")
        assert name == "Equifax Beacon 5.0"


def test_credit_score_name_of_a_specific_type_fico2(fake):
    for _ in range(100):
        name = fake.credit_score_name("fico2")
        assert name == "Experian/Fair Isaac Risk Model V2SM"


def test_credit_score_name_of_a_specific_type_fico4(fake):
    for _ in range(100):
        name = fake.credit_score_name("fico4")
        assert name == "TransUnion FICO Risk Score, Classic 04"


def test_random_credit_score_full(fake):
    """Returns a CreditScoreResult namedtuple with name, provider, and score."""
    from faker_credit_score import CreditScoreResult
    for _ in range(100):
        result = fake.credit_score_full()
        assert isinstance(result, CreditScoreResult)
        assert isinstance(result.name, str)
        assert isinstance(result.provider, str)
        assert isinstance(result.score, int)
        # Destructuring works
        name, provider, score = result
        assert name == result.name
        # str() produces CLI-friendly multi-line format
        assert str(result) == f"{result.name}\n{result.provider}\n{result.score}"


def test_credit_score_full_of_a_specific_type(fake):
    for _ in range(100):
        result = fake.credit_score_full("fico5")
        assert result.name == "Equifax Beacon 5.0"
        assert result.provider == "Equifax"
        assert 334 <= result.score <= 818


def test_random_credit_score_tier(fake):
    valid_tiers = ("poor", "fair", "good", "very_good", "exceptional")
    for _ in range(100):
        tier = fake.credit_score_tier()
        assert tier in valid_tiers


def test_credit_score_tier_classifies_poor(fake):
    assert fake.credit_score_tier(score=300) == "poor"
    assert fake.credit_score_tier(score=579) == "poor"
    assert fake.credit_score_tier(score=450) == "poor"


def test_credit_score_tier_classifies_fair(fake):
    assert fake.credit_score_tier(score=580) == "fair"
    assert fake.credit_score_tier(score=669) == "fair"


def test_credit_score_tier_classifies_good(fake):
    assert fake.credit_score_tier(score=670) == "good"
    assert fake.credit_score_tier(score=739) == "good"


def test_credit_score_tier_classifies_very_good(fake):
    assert fake.credit_score_tier(score=740) == "very_good"
    assert fake.credit_score_tier(score=799) == "very_good"


def test_credit_score_tier_classifies_exceptional(fake):
    assert fake.credit_score_tier(score=800) == "exceptional"
    assert fake.credit_score_tier(score=850) == "exceptional"


def test_credit_score_tier_boundary_values(fake):
    """Verify each boundary falls into the correct tier (lower-bound inclusive)."""
    assert fake.credit_score_tier(score=579) == "poor"
    assert fake.credit_score_tier(score=580) == "fair"
    assert fake.credit_score_tier(score=669) == "fair"
    assert fake.credit_score_tier(score=670) == "good"
    assert fake.credit_score_tier(score=739) == "good"
    assert fake.credit_score_tier(score=740) == "very_good"
    assert fake.credit_score_tier(score=799) == "very_good"
    assert fake.credit_score_tier(score=800) == "exceptional"


def test_credit_score_tier_out_of_range(fake):
    with pytest.raises(ValueError):
        fake.credit_score_tier(score=299)
    with pytest.raises(ValueError):
        fake.credit_score_tier(score=851)


def test_credit_score_with_tier_poor(fake):
    for _ in range(100):
        score = fake.credit_score(tier="poor")
        assert 300 <= score <= 579


def test_credit_score_with_tier_exceptional(fake):
    for _ in range(100):
        score = fake.credit_score(tier="exceptional")
        assert 800 <= score <= 850


def test_credit_score_with_tier_and_score_type(fake):
    """When both tier and score_type given, clamp to intersection of ranges."""
    for _ in range(100):
        # fico5 range is 334-818, "poor" is 300-579 → effective 334-579
        score = fake.credit_score(score_type="fico5", tier="poor")
        assert 334 <= score <= 579


def test_credit_score_with_tier_and_score_type_exceptional_clamped(fake):
    """fico5 range is 334-818, "exceptional" is 800-850 → effective 800-818."""
    for _ in range(100):
        score = fake.credit_score(score_type="fico5", tier="exceptional")
        assert 800 <= score <= 818


def test_credit_score_with_tier_no_overlap(fake):
    """When tier range doesn't overlap model range, raise ValueError."""
    from faker_credit_score import CreditScore, CreditScoreObject
    # Create a score type with range 600-650, which has no overlap with "exceptional" (800-850)
    CreditScore.credit_score_types["narrow_test"] = CreditScoreObject(
        "Narrow Test", ("Test",), (600, 650)
    )
    try:
        with pytest.raises(ValueError):
            fake.credit_score(score_type="narrow_test", tier="exceptional")
    finally:
        del CreditScore.credit_score_types["narrow_test"]


def test_credit_score_with_invalid_tier(fake):
    with pytest.raises(ValueError, match="Unknown tier 'nonexistent'"):
        fake.credit_score(tier="nonexistent")


def test_credit_score_full_with_tier(fake):
    """Full output with tier constraint should produce score in tier range."""
    for _ in range(100):
        result = fake.credit_score_full(tier="exceptional")
        assert 800 <= result.score <= 850


def test_credit_score_full_with_tier_and_score_type(fake):
    """Full output with both tier and score_type."""
    for _ in range(100):
        result = fake.credit_score_full(score_type="fico5", tier="poor")
        assert result.name == "Equifax Beacon 5.0"
        assert result.provider == "Equifax"
        assert 334 <= result.score <= 579


# --- credit_score_profile tests ---


def test_credit_score_profile_default(fake):
    """Default profile returns a dict with CreditScoreResult per provider."""
    from faker_credit_score import CreditScoreResult
    for _ in range(100):
        profile = fake.credit_score_profile()
        assert isinstance(profile, dict)
        assert len(profile) >= 1
        for provider, result in profile.items():
            assert isinstance(result, CreditScoreResult)
            assert result.provider == provider


def test_credit_score_profile_specific_model(fake):
    """FICO 8 profile returns all three bureaus."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico8")
        assert set(profile.keys()) == {"Equifax", "Experian", "TransUnion"}
        for result in profile.values():
            assert result.name == "FICO Score 8"
            assert 300 <= result.score <= 850


def test_credit_score_profile_single_bureau_model(fake):
    """Single-bureau model returns a single-entry dict."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico5")
        assert set(profile.keys()) == {"Equifax"}
        assert profile["Equifax"].name == "Equifax Beacon 5.0"
        assert 334 <= profile["Equifax"].score <= 818


def test_credit_score_profile_filter_providers(fake):
    """Only requested providers are returned."""
    for _ in range(100):
        profile = fake.credit_score_profile(
            score_type="fico8", providers=["Equifax", "TransUnion"]
        )
        assert set(profile.keys()) == {"Equifax", "TransUnion"}


def test_credit_score_profile_case_insensitive_providers(fake):
    """Provider names are matched case-insensitively."""
    for _ in range(100):
        profile = fake.credit_score_profile(
            score_type="fico8", providers=["equifax", "EXPERIAN"]
        )
        assert set(profile.keys()) == {"Equifax", "Experian"}


def test_credit_score_profile_invalid_provider(fake):
    """Requesting a provider not available for the model raises ValueError."""
    with pytest.raises(ValueError, match="not available"):
        fake.credit_score_profile(score_type="fico5", providers=["TransUnion"])


def test_credit_score_profile_nonexistent_score_type(fake):
    with pytest.raises(KeyError):
        fake.credit_score_profile(score_type="nonexistent")


def test_credit_score_profile_with_tier(fake):
    """Tier constrains scores to the right ballpark."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico8", tier="poor")
        for result in profile.values():
            # Base score is in poor range; jitter may push slightly outside
            assert 275 <= result.score <= 604  # 300±25 to 579±25


def test_credit_score_profile_with_tier_and_model(fake):
    """Combined tier and model constraints work correctly."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico5", tier="exceptional")
        assert set(profile.keys()) == {"Equifax"}
        # fico5 range 334-818, exceptional 800-850 → base 800-818, jitter clamped to model
        assert 775 <= profile["Equifax"].score <= 818


def test_credit_score_profile_invalid_tier(fake):
    with pytest.raises(ValueError, match="Unknown tier"):
        fake.credit_score_profile(tier="nonexistent")


def test_credit_score_profile_tier_no_overlap(fake):
    """Tier with no overlap raises ValueError."""
    from faker_credit_score import CreditScore, CreditScoreObject
    CreditScore.credit_score_types["narrow_test"] = CreditScoreObject(
        "Narrow Test", ("Test",), (600, 650)
    )
    try:
        with pytest.raises(ValueError):
            fake.credit_score_profile(score_type="narrow_test", tier="exceptional")
    finally:
        del CreditScore.credit_score_types["narrow_test"]


def test_credit_score_profile_scores_correlated(fake):
    """All scores in a profile should be within 50 points of each other."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico8")
        scores = [r.score for r in profile.values()]
        assert max(scores) - min(scores) <= 50


def test_credit_score_profile_scores_within_model_range(fake):
    """Jitter should never push scores outside the model's valid range."""
    for _ in range(100):
        profile = fake.credit_score_profile(score_type="fico5")
        for result in profile.values():
            assert 334 <= result.score <= 818
