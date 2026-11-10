import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.note_detector import frequency_to_note, is_in_tune, get_tuning_direction


# tests pour frequency_to_note

def test_a4_is_440hz():
    # La4 = 440 Hz exactement : reference internationale
    result = frequency_to_note(440.0)
    assert result["note"] == "A"
    assert result["octave"] == 4
    assert abs(result["cents_off"]) < 0.01


def test_a5_is_880hz():
    # La5 = 880 Hz (une octave au dessus de A4)
    result = frequency_to_note(880.0)
    assert result["note"] == "A"
    assert result["octave"] == 5


def test_e4_standard():
    # Mi4 (E4) = 329.63 Hz : corde de mi d'une guitare standard
    result = frequency_to_note(329.63)
    assert result["note"] == "E"
    assert result["octave"] == 4


def test_invalid_frequency_raises():
    with pytest.raises(ValueError):
        frequency_to_note(0.0)

    with pytest.raises(ValueError):
        frequency_to_note(-100.0)


def test_cents_off_sharp_note():
    # une frequence legerement au dessus de A4 doit avoir cents_off positif
    result = frequency_to_note(445.0)
    assert result["cents_off"] > 0.0


def test_cents_off_flat_note():
    # une frequence legerement en dessous de A4 doit avoir cents_off negatif
    result = frequency_to_note(435.0)
    assert result["cents_off"] < 0.0


# tests pour is_in_tune

def test_in_tune_at_zero_cents():
    assert is_in_tune(0.0) is True


def test_in_tune_within_tolerance():
    assert is_in_tune(4.9) is True
    assert is_in_tune(-4.9) is True


def test_out_of_tune_beyond_tolerance():
    assert is_in_tune(10.0) is False
    assert is_in_tune(-10.0) is False


# tests pour get_tuning_direction

def test_direction_too_high():
    assert get_tuning_direction(20.0) == "TROP HAUT"


def test_direction_too_low():
    assert get_tuning_direction(-20.0) == "TROP BAS"


def test_direction_in_tune():
    assert get_tuning_direction(0.0) == "ACCORDE"
    assert get_tuning_direction(3.0) == "ACCORDE"
