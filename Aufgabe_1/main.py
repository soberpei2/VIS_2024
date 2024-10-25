# main.py

import numpy as np
import matplotlib.pyplot as plt
import model
import solver

def run_simulation():
    # Parameters
    m = 1.0        # mass (kg)
    k = 100        # stiffness (N/m)
    d = 0.01       # damping coefficient
    F = 0          # Force 
    # initial conditions
    iniStates = np.array([1, 1])

    # Time parameters
    t_final = 10.0
    dt = 0.001
    num_steps = int(t_final / dt)

    # Create a model (SingleMassOscillator)
    myModel = model.SingleMassOscillator(iniStates, m, k, d,F)

    # Create/Select a solver
    mySolver = solver.SolverExplicit(myModel)

    # Arrays to store time and position for plotting
    times = np.linspace(0, t_final, num_steps)
    positions = np.zeros_like(times)
    velocity = np.zeros_like(times)


    # Simulation loop
    for step in range(num_steps):
        t = step * dt
        # Store the current position for plotting
        positions[step] = myModel.get_state()[0]
        
        # Store the current velocity 
        velocity[step] = myModel.get_state()[1]
        
        # create new States 
        newStates = mySolver.step(t, dt, positions[step])

        # save new States 
        myModel.set_state(newStates)

        # Take a time step
        mySolver.step(t,dt)

plt.plot(t, positions, label="Position")
plt.plot(t, velocity, label="Velocity")
plt.xlabel("Time (s)")
plt.ylabel("State")
plt.legend()
plt.show()



if __name__ == "__main__":
    run_simulation()
