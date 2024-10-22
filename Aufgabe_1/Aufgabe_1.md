# Zeitintegrator

## Ziel
Kennenlernen von Python

## Aufgabe

Implementieren Sie mindestens zwei Zeitintegrationsverfahren:
- Klasse `solver`
- Abgeleitete Klasse `solver_xy`

### Zeitintegrationsverfahren
- **Euler explizit**
- **Euler implizit**

### Modellierung eines Einmassenschwingers
- **Masse \( m = 1 \, \text{kg} \)**
- **Steifigkeit \( c = 100 \, \text{N/mm} = 100000 \, \text{N/m} \)**
- **Dämpfungsrate \( D = 0.01 \)**

### Anforderungen
1. Implementierung der Zeitintegrationsmethoden.
2. Modellierung des Einmassenschwingers.
3. Durchführung einer Konvergenzanalyse.
4. Export der Daten in eine Datei (CSV oder XLSX).
5. Plotten der Ergebnisse mit Python (Matplotlib).

## Implementierung

### 1. `solver` Klasse

```python
class Solver:
    def __init__(self, mass, stiffness, damping, time_step):
        self.m = mass
        self.c = damping
        self.k = stiffness
        self.dt = time_step
        self.time = 0

    def step(self, force):
        raise NotImplementedError("This method should be implemented by subclasses.")
