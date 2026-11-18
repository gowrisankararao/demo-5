import pytest

from priority_score import calculate_priority_score


@pytest.mark.parametrize(
    ("severity", "expected_score"),
    [
        ("critical", 80),
        ("warning", 50),
        ("info", 30),
    ],
)
def test_calculate_priority_score_above_threshold_returns_int(
    severity: str,
    expected_score: int,
) -> None:
    score = calculate_priority_score(severity, metric_value=15.0, threshold=10.0)

    assert isinstance(score, int)
    assert score == expected_score

# --- Edge cases added manually ---
def test_unknown_severity_raises_value_error():
    with pytest.raises(ValueError, match="Unsupported severity"):
        calculate_priority_score("emergency", 100, 90)


def test_zero_threshold_raises_value_error():
    with pytest.raises(ValueError, match="threshold must not be zero"):
        calculate_priority_score("critical", 50, 0)


def test_metric_below_threshold_gets_no_bonus():
    assert calculate_priority_score("warning", -20, 10) == 30


def test_metric_at_threshold_gets_no_bonus():
    assert calculate_priority_score("critical", 10, 10) == 60


def test_priority_score_bonus_is_capped_at_100():
    score = calculate_priority_score("critical", 100, 10)

    assert isinstance(score, int)
    assert score == 100