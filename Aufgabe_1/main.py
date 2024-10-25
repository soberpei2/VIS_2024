# main.py

import numpy as np
import matplotlib.pyplot as plt
import os
import model
import solver

def run_simulation():
    # Parameters
    m = 1.0          # mass (kg)
    k = 100.0     # stiffness (N/m)
    D = 0.01         # Lehrsches Dämpfungsmaß
    F = 1000.0          # force (N)

    # initial conditions
    iniStates = np.array([0.0, 0.0])

    # Time parameters
    t_final = 10.0
    dt = 0.001
    num_steps = int(t_final / dt)

    # Create a model (SingleMassOscillator)
    myModel = model.SingleMassOscillator(iniStates, m, k, D, F)

    # Create a solver
    #mySolver = solver.SolverExplicit(myModel)
    mySolver = solver.SolverImplicit(myModel)

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
    plt.plot(times, positions, "g-")
    plt.grid(True)
    plt.xlabel(r"Zeit $t$ in [s]")
    plt.ylabel(r"Weg $x$ in [m]")
    plt.title("Konvergenzanalyse")

    plt.savefig(os.getcwd() + "fig.png")

    # Define array with position over time
    posOverTime = np.zeros((len(times), 2))
    posOverTime[:,0] = times
    posOverTime[:,1] = positions

    # Get path to current script directory
    workPath = os.getcwd()
    fileName = workPath + "PosOverTime.csv"
    
    # Writing results in a .csv-File
    np.savetxt(fileName, posOverTime, delimiter = ' ')

if __name__ == "__main__":
    run_simulation()
