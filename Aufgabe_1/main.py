# main.py
#importieren von Bibliotheken
import numpy as np
import matplotlib.pyplot as plt

#Verbindung herstellen zu model und solver durch importieren#Verbindung herstellen zu model und solver durch importieren
import model
import solver

# Funktion für durchlauf der Funktion
def run_simulation():
    # Parameters
    m = 1.0      # mass (kg)
    k = 100000.0     # stiffness (N/m)
    d = 0.01      # damping coefficient

    # initial conditions
    iniStates = np.array([1.0, 0.0])

    # Time parameters
    t_final = 1.0
    dt = 0.0001
    num_steps = int(t_final / dt)

    # Create a model (SingleMassOscillator)
    myModel = model.SingleMassOscillator(iniStates, m, k, d)

    # Create a solver
    mySolver = solver.SolverExplicit(myModel)

    # Arrays to store time and position for plotting
    times = np.linspace(0, t_final, num_steps)
    positions = np.zeros_like(times)

    #Simulations Schleife
    for step in range(num_steps):
        t = step * dt
        # Store the current position for plotting
        positions[step] = myModel.get_state()[0]
        
        # Take a time step
        mySolver.step(t, dt)

    # Plotting the result
    plt.plot(times, positions)
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Single Mass Oscillator')
    plt.show()

   
if __name__ == "__main__":
    run_simulation()