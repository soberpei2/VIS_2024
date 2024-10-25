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
        
        position = xk[0]  # Aktuelle Position
        velocity = xk[1]  # Aktuelle Geschwindigkeit

        # Berechnung des nächsten Zustands
        next_state = np.array([
            position + dt * velocity,
            velocity + dt * self.__model__.dydt(t)[1]  # Hier ist es wichtig, dass dydt mit dem richtigen t aufgerufen wird
        ])
        
        return next_state
