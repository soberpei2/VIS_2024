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

    def step(self, t, dt):
        """Perform one step of numerical integration."""
       
        #aktueller Zustand
        z = self.__model__.get_state()

        #Ableitung vom Modell berechnen
        f = self.__model__.dydt(t)

        #neuen Zustand berechnen
        z1 = z + dt * f

        #Zustand setzen
        self.__model__.set_state(z1)
        
