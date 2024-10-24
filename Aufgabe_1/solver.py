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

    def step(self, t, dt, xk, vk):
        
        """Perform one step of numerical integration."""
        #----------------------------------------------------------------------------

        # Setting derivatives
        dydt = self.__model__.dydt(t)

        # Euler algorithm
        xk1 = xk + dt * dydt[0]
        vk1 = vk + dt * dydt[1]

        # Return updated state
        return np.array([xk1, vk1])

        #----------------------------------------------------------------------------
        
