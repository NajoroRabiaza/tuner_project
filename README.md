# Accordeur Chromatique - TFD

Systeme de detection de notes et accordeur chromatique en temps reel.
Basé sur la Transformee de Fourier Discrete (TFD).

## Principe

Le signal audio capte par le microphone est analyse via la TFD :

```
X[k] = SUM(n=0 -> N-1) x[n] * e^(-i * 2*pi*k*n / N)
```

La frequence fondamentale est identifiee comme le pic d'amplitude maximale
dans le spectre. Elle est ensuite convertie en note musicale via :

```
n = 12 * log2(f / 440)
```

## Structure

```
tuner/
|-- src/
|   |-- core/
|   |   |-- dft.py           # Transformee de Fourier Discrete
|   |   |-- note_detector.py # Conversion frequence -> note musicale
|   |-- utils/
|   |   |-- audio_capture.py # Capture microphone
|   |   |-- plot_spectrum.py # Generation du diagramme spectre
|   |-- main.py              # Point d'entree principal
|-- tests/
|   |-- test_dft.py
|   |-- test_note_detector.py
|-- requirements.txt
|-- README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
# Lancer l'accordeur en temps reel
cd src
python main.py

# Generer le diagramme spectre (sans microphone)
cd src
python utils/plot_spectrum.py

# Lancer les tests
pytest tests/
```

## Reference

- A4 = 440 Hz (reference internationale)
- Tolerance d'accord : +/- 5 cents
- Plage de detection : 50 Hz - 5000 Hz
