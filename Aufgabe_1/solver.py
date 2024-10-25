import model
import numpy as np

# Parentclass
#============
class Solver:
    def __init__(self, model2Solve):
        if not isinstance(model2Solve, model.Model):
            raise TypeError("Expected an instance of model or its subclass.")
        self.__model__ = model2Solve

    def step(self, t, dt):
        """Should be implemented in derived classes."""
        raise NotImplementedError("This method should be implemented by subclasses.")
#=====================================================================================

# Children class - Explicit Solver
#=================================
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
#=====================================================================================
        
# Children class - Implicit Solver
#=================================
class SolverImplicit(Solver):
    # Constructor
    #------------
    def __init__(self, model2Solve):
        super().__init__(model2Solve)

    # Calculation step
    #-----------------
    def step(self, t, dt, xk, vk):

        """"Perform one step of numerical integration with implicit Euler."""

        #----------------------------------------------------------------------------

        # Setting derivatives
        dydt = self.__model__.dydt(t)

        # Calculating current velocity v(k + 1)
        vk1 = (dt / self.__model__.m * (self.__model__.F - self.__model__.k * xk)) / (1 + dt * self.__model__.d / self.__model__.m + dt**2 * self.__model__.k / self.__model__.m)

        # Calculating current position x(k + 1)
        xk1 = xk + dt * vk1

        # Return updated state
        return np.array([xk1, vk1])
