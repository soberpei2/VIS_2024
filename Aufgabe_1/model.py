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
        self.__d__ = 2 * d * np.sqrt(m * k)

    
    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
        position = self.get_state[0]
        velocity = self.get_state[1]

        acceleration = -(self.__k__ * position - self.__d__ * velocity) / self.__m__

        return np.array([velocity, acceleration]) 
        #----------------------------------------------------------------------------

