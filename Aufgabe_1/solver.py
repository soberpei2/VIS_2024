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
        """Führt einen Schritt der numerischen Integration mit dem expliziten Euler-Verfahren aus."""
        # Aktuellen Zustand und Ableitungen berechnen
        current_state = self.__model__.get_state()
        dydt = self.__model__.dydt(t)

        # Expliziter Euler-Schritt: z_k+1 = z_k + dt * f(t_k, z_k)
        new_state = current_state + dt * dydt
    
        # Den neuen Zustand im Modell speichern
        self.__model__.set_state(new_state)
        #----------------------------------------------------------------------------
        
