import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.dft import compute_dft, find_fundamental_frequency
from core.note_detector import frequency_to_note

SAMPLE_RATE = 44100


def generate_demo_signal(frequency: float, duration: float = 0.1) -> np.ndarray:
    """
    Genere un signal sinusoidal de test a une frequence donnee.
    Utilise pour produire le diagramme du spectre sans microphone.

    entree  : frequency -> frequence de la sinusoide en Hz
    entree  : duration  -> duree du signal en secondes
    sortie  : tableau numpy des echantillons
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # signal compose : fondamentale + harmoniques pour ressembler a un vrai instrument
    signal = (
        np.sin(2 * np.pi * frequency * t) * 1.0 +
        np.sin(2 * np.pi * frequency * 2 * t) * 0.5 +
        np.sin(2 * np.pi * frequency * 3 * t) * 0.25
    )
    return signal.astype(np.float32)


def plot_spectrum(signal: np.ndarray, sample_rate: int, output_path: str):
    """
    Genere et sauvegarde le diagramme du spectre frequentiel.
    Ce diagramme montre le resultat de la TFD appliquee au signal.

    entree  : signal      -> tableau numpy des echantillons
    entree  : sample_rate -> taux d'echantillonnage en Hz
    entree  : output_path -> chemin de sauvegarde de l'image
    """
    # etape 1 : calculer la TFD
    frequencies, amplitudes = compute_dft(signal, sample_rate)

    # etape 2 : trouver la frequence fondamentale
    # on filtre entre 50 Hz et 5000 Hz
    mask = (frequencies >= 50) & (frequencies <= 5000)
    freq_filtered = frequencies[mask]
    amp_filtered = amplitudes[mask]

    fundamental = find_fundamental_frequency(freq_filtered, amp_filtered)
    note_info = frequency_to_note(fundamental)
    note_name = f"{note_info['note']}{note_info['octave']}"

    # etape 3 : construire le graphique
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle("Diagramme du Spectre Frequentiel - TFD", fontsize=14, fontweight="bold")

    # --- graphique 1 : signal temporel ---
    t = np.linspace(0, len(signal) / sample_rate, len(signal))
    # afficher seulement les 5 premiers millisecondes
    samples_to_show = int(0.005 * sample_rate)
    ax1.plot(t[:samples_to_show] * 1000, signal[:samples_to_show], color="steelblue", linewidth=0.8)
    ax1.set_title("Signal audio (domaine temporel)")
    ax1.set_xlabel("Temps (ms)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    # --- graphique 2 : spectre frequentiel (resultat TFD) ---
    ax2.plot(freq_filtered, amp_filtered, color="darkorange", linewidth=0.8)

    # marquer la frequence fondamentale
    peak_idx = np.argmax(amp_filtered)
    ax2.axvline(
        x=fundamental,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Fondamentale : {fundamental:.2f} Hz ({note_name})"
    )
    ax2.scatter([fundamental], [amp_filtered[peak_idx]], color="red", zorder=5, s=60)

    ax2.set_title("Spectre frequentiel (domaine frequentiel apres TFD)")
    ax2.set_xlabel("Frequence (Hz)")
    ax2.set_ylabel("Amplitude |X[k]|")
    ax2.set_xlim(0, 3000)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Spectre sauvegarde : {output_path}")


if __name__ == "__main__":
    # demo : generer le spectre d'un La4 (440 Hz)
    signal = generate_demo_signal(440.0)

    output_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "spectrum_demo.png"
    )
    plot_spectrum(signal, SAMPLE_RATE, os.path.abspath(output_path))
