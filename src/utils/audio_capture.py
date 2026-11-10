import numpy as np
import sounddevice as sd

# parametres audio standard pour la detection de notes musicales
SAMPLE_RATE = 44100   # 44100 echantillons par seconde (CD quality)
BUFFER_SIZE = 4096    # nombre d'echantillons par bloc capture
CHANNELS = 1          # mono (un seul canal suffit pour la detection)


def capture_audio_block() -> np.ndarray:
    """
    Capture un bloc d'audio depuis le microphone.
    Bloquant : attend que le buffer soit rempli avant de retourner.

    sortie : tableau numpy de forme (BUFFER_SIZE,) contenant les echantillons
    """
    # sd.rec capture BUFFER_SIZE echantillons depuis le micro
    # dtype='float32' : chaque echantillon est un flottant entre -1.0 et 1.0
    audio_block = sd.rec(
        frames=BUFFER_SIZE,
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )
    # attendre la fin de la capture
    sd.wait()

    # aplatir le tableau 2D (BUFFER_SIZE, 1) en 1D (BUFFER_SIZE,)
    return audio_block.flatten()


def compute_rms(signal: np.ndarray) -> float:
    """
    Calcule le niveau RMS (Root Mean Square) du signal.
    C'est une mesure du volume sonore moyen du signal.
    RMS = sqrt( (1/N) * SUM(x[n]^2) )

    entree  : signal -> tableau numpy des echantillons
    sortie  : valeur RMS (float)
    """
    if len(signal) == 0:
        raise ValueError("Signal cannot be empty")

    return float(np.sqrt(np.mean(signal ** 2)))
