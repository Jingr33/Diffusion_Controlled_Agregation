"""
Application for simulating diffusion-controlled aggregation. It simulates the formation of a dendrimer during electrolysis.
"""


import argparse
from Simulation import Simulation
from chart_creator import ChartCreator
from config import *

def main():
    parser = argparse.ArgumentParser(description = "Difuzně řízená agregace")
    parser.add_argument("--layout", type=str, choices = layout_choices, default = layout_default, help = "Typ počátečního rozdělení molekul")
    parser.add_argument("--atoms", nargs='+', type=int, default = atoms_default, help = "Počet atomů v simulaci")
    parser.add_argument("--visualize", action="store_true", help = "Zobrazí vizualizaci počátečního a koncového stavu")
    parser.add_argument("--plot", action="store_true", help = "Zobrazí graf početu atomů proti gyračnímu poloměru")
    parser.add_argument("--sim", action="store_true", help = "Spustí simulaci")
    args = parser.parse_args()
    _start_sim(args.layout, args.atoms, args.visualize, args.sim)
    _plot_chart(args.plot)

def _start_sim (layout : str, atom_numbers : list, visualize : bool, simulation : bool) -> None:
    """
    Start simulation and visualization.

    Runs the simulation for each requested atom count. Optionally visualizes the
    initial and final states and the system's gyration radius.

    Args:
        layout (str): Start positions of the ions ("cube", "sphere" or "random").
        atom_numbers (list[int]): List of atom counts for the simulation.
        visualize (bool): Whether to visualize the initial and final state.
        simulation (bool): Whether to run the simulation process.
    """
    if not simulation: 
        return
    for atom_number in atom_numbers:
        sim = Simulation(layout, atom_number, visualize)
        if (visualize):
            sim.run()

def _plot_chart (plot : bool) -> None:
    """
    Plot the results chart.

    If enabled, plots the dependency of log N (number of particles) on log Rg
    (gyration radius) after the simulation has finished.

    Args:
        plot (bool): Whether plotting the chart is enabled.
    """
    if (plot):
        ChartCreator()


if __name__ == '__main__':
    main()