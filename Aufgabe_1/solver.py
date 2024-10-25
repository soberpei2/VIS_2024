import model

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
        # your implementation here

        
    def step(self, t, dt, xk):
        
        """Perform one step of numerical integration."""
        #----------------------------------------------------------------------------
        # Euler Explizit 

        # z(k+1) = z(k) + h * f(t(k),z(k))

        xk1 = xk + dt * self.__model__.dydt(t)[0]
        vk1 = self.__model__.dydt(t)[0] + dt * self.__model__.dydt(t)[1]
    

       #  vk1 = (xk1 - xk) / dt