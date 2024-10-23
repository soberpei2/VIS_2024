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

    def step(self, t, dt):
        
        """Perform one step of numerical integration using forward Euler"""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
        #----------------------------------------------------------------------------
        current_state = self.__model__.get_state()
        new_state = current_state + dt * self.__model__.dydt(t)
        self.__model__.set_state(new_state)

class SolverImplicit(Solver):
    def __init__(self, model2Solve, tolerance=1e-6, max_iterations=100):
        super().__init__(model2Solve)
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def step(self, t, dt):
        """Perform one step of implicit numerical integration using backward Euler."""
        current_state = self.__model__.get_state()
        new_state = current_state

        for _ in range(self.max_iterations):
            new_state_next = current_state + dt * self.__model__.dydt(t + dt)
            
            # Check for convergence
            if np.linalg.norm(new_state_next - new_state) < self.tolerance:
                new_state = new_state_next
                break
            
            new_state = new_state_next
        
        self.__model__.set_state(new_state)
