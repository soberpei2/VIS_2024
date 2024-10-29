import numpy as np

class Model:
    def __init__(self, iniState):
        self.state = iniState

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state # new_state wird am Ende vom Solverschritt gesetzt 
        
    def dydt(self, t, y):
        """Defines the system's dynamics: computes the derivative of the state vector."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SingleMassOscillator(Model):
    def __init__(self, iniState, m, k, d):
        super().__init__(iniState)
        self.__m__ = m #Masse
        self.__k__ = k #Steifigkeit
        self.__d__ = 2*d*np.sqrt(self.__m__*self.__k__) #Umrechnen von D auf d

    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        position = self.state[0]
        velocity = self.state[1]

        # aus Bewegungsgleichung
        acceleration = (-self.__k__ * position - self.__d__ * velocity)/self.__m__
        
        return np.array([velocity, acceleration])