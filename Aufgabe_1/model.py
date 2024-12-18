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
<<<<<<< HEAD
        self.__m__ = m  # Mass
        self.__k__ = k  # Stiffness
        self.__d__ = 2*d*np.sqrt(self.__m__*self.__k__)  # Damping

    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        position = self.state[0]
        velocity = self.state[1]
        
        # Equation of motion: 
        acceleration = (-self.__k__ / self.__m__) * position - (self.__d__ / self.__m__) * velocity
        
=======
        self.m = m
        self.k = k
        self.d = 2*d*np.sqrt(self.m*self.k)

    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
>>>>>>> 556f251205053badc0fd836e57cb1a2d74bb833a
        
        position = self.state[0]
        velocity = self.state[1]
        acceleration = (-self.k * position - self.d * velocity) / self.m
        return np.array([velocity, acceleration]) 

