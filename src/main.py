import sys
import numpy as np

from core.dft import compute_dft, find_fundamental_frequency
from core.note_detector import (
    frequency_to_note,
    get_tuning_direction,
    is_in_tune,
    SILENCE_THRESHOLD
)
from utils.audio_capture import capture_audio_block, compute_rms, SAMPLE_RATE

# frequences audibles pour une guitare / instrument standard
# on filtre les frequences hors de cette plage pour ignorer le bruit
MIN_FREQUENCY = 50.0    # Hz (en dessous : grondement, bruit de fond)
MAX_FREQUENCY = 5000.0  # Hz (au dessus : harmoniques non fondamentaux)


def print_header():
    print("=" * 50)
    print("   ACCORDEUR CHROMATIQUE - TFD")
    print("   Reference : A4 = 440 Hz")
    print("=" * 50)
    print("Jouez une note sur votre instrument...")
    print("Appuyez sur Ctrl+C pour quitter.\n")


def build_tuning_bar(cents_off: float) -> str:
    """
    Construit une barre visuelle d'accord dans le terminal.
    Le centre represente l'accord parfait.
    Les '<' indiquent trop bas, '>' indiquent trop haut.

    entree  : cents_off -> ecart en cents
    sortie  : chaine de caracteres representant la barre
    """
    bar_width = 20
    center = bar_width // 2

    # normaliser cents_off entre -50 et +50
    clamped = max(-50.0, min(50.0, cents_off))
    # convertir en position dans la barre
    position = int(center + (clamped / 50.0) * center)
    position = max(0, min(bar_width - 1, position))

    bar = ["-"] * bar_width
    bar[center] = "|"
    bar[position] = "O"

    return "[" + "".join(bar) + "]"


def process_audio_block(audio_block: np.ndarray):
    """
    Traite un bloc audio et affiche le resultat dans le terminal.
    Pipeline complet : signal -> TFD -> frequence -> note -> affichage

    entree : audio_block -> tableau numpy des echantillons captures
    """
    # etape 1 : verifier le niveau sonore
    rms = compute_rms(audio_block)
    if rms * 32768 < SILENCE_THRESHOLD:
        print("\r  [silence detecte]              ", end="", flush=True)
        return

    # etape 2 : appliquer la TFD
    frequencies, amplitudes = compute_dft(audio_block, SAMPLE_RATE)

    # etape 3 : filtrer les frequences hors plage audible utile
    mask = (frequencies >= MIN_FREQUENCY) & (frequencies <= MAX_FREQUENCY)
    if not np.any(mask):
        return

    frequencies_filtered = frequencies[mask]
    amplitudes_filtered = amplitudes[mask]

    # etape 4 : trouver la frequence fondamentale (pic dominant)
    fundamental = find_fundamental_frequency(frequencies_filtered, amplitudes_filtered)

    # etape 5 : convertir en note musicale
    note_info = frequency_to_note(fundamental)

    # etape 6 : construire et afficher le resultat
    note_name = f"{note_info['note']}{note_info['octave']}"
    cents = note_info["cents_off"]
    direction = get_tuning_direction(cents)
    tuning_bar = build_tuning_bar(cents)
    in_tune_marker = " [OK]" if is_in_tune(cents) else ""

    line = (
        f"\r  Note : {note_name:<4}  "
        f"| {fundamental:>7.2f} Hz  "
        f"| {cents:>+6.1f} cents  "
        f"| {tuning_bar}  "
        f"{direction:<10}"
        f"{in_tune_marker}"
    )
    print(line, end="", flush=True)


def main():
    print_header()

    try:
        while True:
            audio_block = capture_audio_block()
            process_audio_block(audio_block)

    except KeyboardInterrupt:
        print("\n\nAccordeur arrete.")
        sys.exit(0)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
