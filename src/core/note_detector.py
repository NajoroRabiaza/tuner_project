import math

# table chromatique : 12 notes par octave
# reference internationale : La4 (A4) = 440 Hz
# formule : f(n) = 440 * 2^(n/12)
# ou n est le nombre de demi-tons par rapport a A4

CHROMATIC_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# seuil minimum pour considerer qu'un signal est assez fort
# en dessous de ce seuil on considere que c'est du silence
SILENCE_THRESHOLD = 50.0


def frequency_to_note(frequency: float) -> dict:
    """
    Convertit une frequence en Hz vers la note musicale la plus proche.

    La formule de conversion est :
    n = round(12 * log2(f / 440))
    note_index = n % 12
    octave = 4 + (n + 9) // 12

    entree  : frequency -> frequence en Hz (ex: 440.0)
    sortie  : dict avec 'note', 'octave', 'frequency', 'cents_off'
    """
    if frequency <= 0:
        raise ValueError("Frequency must be strictly positive")

    # etape 1 : calculer le nombre de demi-tons par rapport a A4 (440 Hz)
    # n = 12 * log2(f / 440)
    n = 12.0 * math.log2(frequency / 440.0)

    # etape 2 : arrondir au demi-ton le plus proche
    n_rounded = round(n)

    # etape 3 : identifier la note et l'octave
    # CHROMATIC_NOTES[0] = A, donc on decale de 9 pour commencer a C
    note_index = n_rounded % 12
    octave = 4 + (n_rounded + 9) // 12

    # etape 4 : calculer l'ecart en cents (100 cents = 1 demi-ton)
    # cents_off mesure a quel point on est desaccorde par rapport a la note juste
    cents_off = (n - n_rounded) * 100.0

    # etape 5 : calculer la frequence theorique exacte de la note detectee
    exact_frequency = 440.0 * (2.0 ** (n_rounded / 12.0))

    return {
        "note": CHROMATIC_NOTES[note_index],
        "octave": octave,
        "frequency": frequency,
        "exact_frequency": exact_frequency,
        "cents_off": cents_off,
        "n": n_rounded
    }


def is_in_tune(cents_off: float, tolerance: float = 5.0) -> bool:
    """
    Verifie si une note est suffisamment accordee.
    La tolerance standard pour un accordeur est +/- 5 cents.

    entree  : cents_off -> ecart en cents par rapport a la note juste
    entree  : tolerance -> seuil d'acceptation en cents (defaut 5)
    sortie  : True si la note est dans la tolerance
    """
    return abs(cents_off) <= tolerance


def get_tuning_direction(cents_off: float) -> str:
    """
    Indique dans quelle direction accorder l'instrument.

    entree  : cents_off -> ecart en cents
    sortie  : "TROP HAUT", "TROP BAS" ou "ACCORDE"
    """
    if cents_off > 5.0:
        return "TROP HAUT"
    elif cents_off < -5.0:
        return "TROP BAS"
    else:
        return "ACCORDE"
