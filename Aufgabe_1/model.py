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
    def __init__(self, iniState, m, k, d):
        super().__init__(iniState)
        #your implementation here
        self.__m__ = m
        self.__k__ = k
        self.__d__ = d
        #leersche Dämpfung
        # self.__d__ = 2*d*np.sqrt(self.__m__*self.__k__)

    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""


        position = self.state[0]
        velocity = self.state[1] 
        
                # Equation of motion for a damped harmonic oscillator: m*a + d*v + k*x = 0
        acceleration = -(self.d/self.m)*velocity - (self.k/self.m)*position

        return np.array([velocity, acceleration]) 
        #----------------------------------------------------------------------------

