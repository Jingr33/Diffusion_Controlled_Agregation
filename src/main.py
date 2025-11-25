"""
Application for simulating diffusion-controlled aggregation. It simulates the formation of a dendrimer during electrolysis.
"""

import argparse

from simulation import Simulation
from visualizer import Visualizer
from chart_creator import ChartCreator
from config import *
from database.db_runner import DbRunner

def main():
    parser = argparse.ArgumentParser(description = "Difuzně řízená agregace")
    parser.add_argument("--layout", type=str, choices = LAYOUTS, default = LAYOUT_DEFAULT, help = "Typ počátečního rozdělení molekul (cube, sphere, random)")
    parser.add_argument("--atoms", nargs='+', type=int, default = ATOMS_DEFAULT, help = "Počet atomů v simulaci")
    parser.add_argument("--visualize", action="store_true", default=VISUALIZATION_DEFAULT, help = "Zobrazí vizualizaci počátečního a koncového stavu")
    parser.add_argument("--plot", action="store_true", default=PLOT_DFAULT, help = "Zobrazí graf početu atomů proti gyračnímu poloměru")
    parser.add_argument("--sim", action="store_true", default=SIM_DEFAULT, help = "Spustí simulaci")
    args = parser.parse_args()
    DbRunner()
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
    visualizer = Visualizer(atom_numbers)
    for atom_number in atom_numbers:
        sim = Simulation(layout, atom_number)
        visualizer.set_simulation_data(sim.get_atoms())
    if visualize:
        visualizer.visualize_simulation()


def _plot_chart (plot : bool) -> None:
    """
    Plot the results chart.

    If enabled, plots the dependency of log N (number of particles) on log Rg
    (gyration radius) after the simulation has finished.

    Args:
        plot (bool): Whether plotting the chart is enabled.
    """
    if plot:
        ChartCreator()


if __name__ == '__main__':
    main()
