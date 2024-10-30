import numpy as np

class Model:
    def __init__(self, iniState):
        self.state = iniState

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state

    def dydt(self, t, y):
        """Defines the system's dynamics: computes the derivative of the state vector."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SingleMassOscillator(Model):
    def __init__(self, iniState, m, k, d, F):
        super().__init__(iniState)
        #your implementation here
        self.__m__ = m
        self.__k__ = k
        self.__d__ =  2*d*np.sqrt(self.__m__*self.__k__) 
        self.__f__= F

    def dydt(self, t):
        """Berechnet die Ableitungen von Position und Geschwindigkeit."""
        position = self.state[0]
        velocity = self.state[1]
        
        # Beschleunigung aus der Bewegungsgleichung
        acceleration =self.__f__/self.__m__ - (self.__k__ / self.__m__) * position - (self.__d__ / self.__m__) * velocity
        
        # Rückgabe von Geschwindigkeit und Beschleunigung als Array
        return np.array([velocity, acceleration])
        
        # Rückgabe von Geschwindigkeit und Beschleunigung als Array
        return np.array([velocity, acceleration])

        return np.array([velocity, acceleration]) 
        #----------------------------------------------------------------------------

