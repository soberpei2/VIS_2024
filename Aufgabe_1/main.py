# main.py

#importieren von Bibliotheken
import numpy as np
import matplotlib.pyplot as plt

#Verbindung herstellen zu model und solver durch importieren
import model
import solver

# Funktion für durchlauf der Funktion
def run_simulation():
    #definieren von Parametern
    m = 1.0     #Masse (kg)
    k = 1000    # Steifigkeit (N/m) 10000 lt Angabe
    d = 0.001   # Dämpfungskoeff.

    #Initialisierungs-Vektor
    iniStates = np.array([0.0,3.0])

    #Zeit Parameter
    t_final = 10.0          #10 sec bis ende Rechnung
    dt = 0.001              #Rechenschritt
    num_steps = int(t_final/dt)  # Anzahl der rechenschritte

    # erstellen eines Modells (in diesem Fall 1 Massenschwinger)

    myModel = model.SingleMassOscillator(iniStates,m,k,d) #instanziert Objekt myModel von der Klasse SingleMassOscillator welches sich unter model befindet

    # erstellen/Wahl eines Solvers mit Eingang des zu lösenden Models
    mySolver = solver.SolverExplicit(myModel)

    # Array für das speichern von Zeit und Position für das Plotten
    times = np.linspace(0,t_final,num_steps)
    positions = np.zeros_like(times)            #gleich viele Stellen wie array times

    #Simulations Schleife

    for step in range(num_steps):       #erhöhen von stepum 1
        t = step*dt                     #aktuelle Sim-Zeit
        #speichern der Position
        positions[step]=myModel.get_state()[0] #nimmt erstes Element (Weg) von Model

        #gehen eines Zeitschrittes
        mySolver.step(t,myModel,dt)

    # Plotting the result
    plt.plot(times, positions)
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Single Mass Oscillator')
    plt.show()

if __name__ == "__main__":
    run_simulation()
