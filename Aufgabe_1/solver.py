# solver.py

import model
import numpy as np

class Solver:
    def __init__(self, model2Solve):
        if not isinstance(model2Solve, model.Model):
            raise TypeError("Expected an instance of model or its subclass.")
        self.__model__ = model2Solve

    def step(self, t, dt):
        """Should be implemented in derived classes."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class SolverExplicit(Solver):
    def __init__(self, model2Solve):
        super().__init__(model2Solve)

    def step(self, t, dt, xk):
        """Perform one step of numerical integration."""
        # Euler Explizit 
        # z(k+1) = z(k) + h * f(t(k), z(k))
        
        # Berechnung des nächsten Zustands
        xk1 = xk[0] + dt * self.__model__.dydt(t)[0]  # Position wird aktualisiert
        yk1 = xk[1] + dt * self.__model__.dydt(t)[1]  # Geschwindigkeit wird aktualisiert

        return np.array([xk1, yk1])  # Rückgabe als NumPy-Array
