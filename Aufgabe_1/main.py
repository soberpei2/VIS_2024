# main.py

import numpy as np
import matplotlib.pyplot as plt
import model
import solver

def run_simulation():
    # Parameters
    m = 1.0          # mass (kg)
    k = 100000.0     # stiffness (N/m)
    d = 0.01         # damping coefficient
    F = 50           # force (N)

    # initial conditions
    iniStates = np.array([0.0, 0.0])

    # Time parameters
    t_final = 10.0
    dt = 0.001
    num_steps = int(t_final / dt)

    # Create a model (SingleMassOscillator)
    myModel = model.SingleMassOscillator(iniStates, m, k, d, F)

    # Create a solver
    mySolver = solver.SolverExplicit(myModel)

    # Arrays to store time, position and velocity for plotting
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

        # Take a time step
        newState = mySolver.step(t, dt, positions[step], velocity[step])

        # Set new state for model
        myModel.set_state(newState)

    # Plotting the result

if __name__ == "__main__":
    run_simulation()
