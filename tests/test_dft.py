import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.dft import compute_dft, find_fundamental_frequency


# tests pour compute_dft

def test_compute_dft_sinusoid_440hz():
    # signal de test : sinusoide pure a 440 Hz (La4)
    # la TFD doit detecter un pic a 440 Hz
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 440 * t).astype(np.float32)

    frequencies, amplitudes = compute_dft(signal, sample_rate)

    peak_index = np.argmax(amplitudes)
    detected_freq = frequencies[peak_index]

    # on accepte une marge de 2 Hz
    assert abs(detected_freq - 440.0) < 2.0


def test_compute_dft_returns_positive_frequencies_only():
    # la fonction doit retourner seulement les frequences positives
    sample_rate = 44100
    signal = np.random.rand(1024).astype(np.float32)
    frequencies, amplitudes = compute_dft(signal, sample_rate)

    assert np.all(frequencies > 0)


def test_compute_dft_empty_signal_raises():
    with pytest.raises(ValueError):
        compute_dft(np.array([]), 44100)


def test_compute_dft_amplitudes_non_negative():
    # les amplitudes (modules) sont toujours positifs ou nuls
    sample_rate = 44100
    signal = np.random.rand(2048).astype(np.float32)
    frequencies, amplitudes = compute_dft(signal, sample_rate)

    assert np.all(amplitudes >= 0)


# tests pour find_fundamental_frequency

def test_find_fundamental_frequency_basic():
    # frequences connues avec un pic clair a 500 Hz
    frequencies = np.array([100.0, 300.0, 500.0, 700.0])
    amplitudes = np.array([10.0, 20.0, 150.0, 5.0])

    result = find_fundamental_frequency(frequencies, amplitudes)
    assert result == 500.0


def test_find_fundamental_frequency_empty_raises():
    with pytest.raises(ValueError):
        find_fundamental_frequency(np.array([440.0]), np.array([]))
