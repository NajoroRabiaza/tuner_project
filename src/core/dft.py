import numpy as np

# calcul de la Transformee de Fourier Discrete sur un signal audio
# on utilise numpy.fft.fft qui est une implementation optimisee de la TFD
# la formule de base :
# X[k] = SUM(n=0 -> N-1) x[n] * e^(-i * 2*pi*k*n / N)

def compute_dft(signal: np.ndarray, sample_rate: int):
    """
    Applique la TFD sur un signal audio et retourne
    les frequences et leurs amplitudes correspondantes.

    entree  : signal      -> tableau numpy des echantillons audio
    entree  : sample_rate -> taux d'echantillonnage (ex: 44100 Hz)
    sortie  : (frequencies, amplitudes) -> deux tableaux de meme taille
    """
    if len(signal) == 0:
        raise ValueError("Signal cannot be empty")

    N = len(signal)

    # etape 1 : appliquer la TFD
    # numpy.fft.fft retourne N nombres complexes X[0], X[1], ..., X[N-1]
    # X[k] represente la composante a la frequence k * sample_rate / N
    spectrum = np.fft.fft(signal)

    # etape 2 : calculer les amplitudes (module des complexes)
    # |X[k]| = sqrt(Re(X[k])^2 + Im(X[k])^2)
    amplitudes = np.abs(spectrum)

    # etape 3 : calculer le vecteur des frequences correspondantes
    # numpy.fft.fftfreq retourne les frequences associees a chaque indice k
    # on garde seulement la moitie positive (le spectre est symetrique)
    frequencies = np.fft.fftfreq(N, d=1.0 / sample_rate)

    # etape 4 : ne garder que la partie positive du spectre
    # la TFD sur signal reel est symetrique : X[k] = conjugue de X[N-k]
    # la partie negative n'apporte pas d'information supplementaire
    positive_mask = frequencies > 0
    frequencies = frequencies[positive_mask]
    amplitudes = amplitudes[positive_mask]

    return frequencies, amplitudes


def find_fundamental_frequency(frequencies: np.ndarray, amplitudes: np.ndarray) -> float:
    """
    Identifie la frequence fondamentale du signal.
    C'est simplement la frequence qui a l'amplitude maximale
    dans le spectre calcule par la TFD.

    entree  : frequencies -> vecteur des frequences (Hz)
    entree  : amplitudes  -> vecteur des amplitudes correspondantes
    sortie  : frequence fondamentale en Hz (float)
    """
    if len(amplitudes) == 0:
        raise ValueError("Amplitudes array cannot be empty")

    # l'indice de l'amplitude maximale correspond a la frequence dominante
    peak_index = np.argmax(amplitudes)
    return float(frequencies[peak_index])
