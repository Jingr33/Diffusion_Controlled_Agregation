from vispy import scene  # visualization of the simulation
from vispy.visuals.transforms import STTransform
from typing import Any

from calculation import Calculation
import config
import numpy as np


class Atom ():
    """
    Representation of a single atom (particle) in the simulation.

    Attributes:
        type (str): "electrode" or "ion".
        position (np.array): 3D position of the atom in space.
        generation (int): Generation index of the particle within the dendrimer.
        positions_list (list): List of all positions occupied during the simulation.
        electrode_dist (float): Distance to the nearest electrode position.
        parent_electrode (Atom): For ions: None. For electrodes: reference to the
            neighboring electrode with lower generation.
    """
    def __init__(self, type : str, position : np.array) -> None:
        """
        Initialize an Atom instance.

        Args:
            type (str): "electrode" or "ion".
            position (np.array): 3D position of the atom in space.
        """
        self.type = type
        self.position = position
        self.generation = 0 if self.type == "electrode" else -1
        self.orig_generation = self.generation
        self.positions_list = [self.position]
        self.electrode_dist = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))
        self.parent_electrode = None
            
    def display(self, view, sim_time : str) -> None:
        """
        Display the atom as a sphere in the visualization.

        Args:
            view (vispy.scene.visuals): View window for the simulation.
            sim_time (str): "start" or "finish" (initial or final state).
        """
        generation = self.generation if sim_time != "start" else self.orig_generation
        position = self.positions_list[0] if sim_time == "start" else self.positions_list[-1]
        self.color = self._set_fg_color(generation)
        self.sphere = scene.visuals.Sphere(radius=config.atom_radius, method='ico', parent=view.scene, color = self.color, edge_color = config.atom_edge_color)
        self._translate_sphere(position)

    def update_position(self, new_position : np.array) -> None:
        """
        Update the atom's current position.

        Args:
            new_position (np.array): New 3D position of the atom.
        """
        self.position = new_position
        self.positions_list.append(new_position)

    def transform_to_electrode (self, nearest_electrode) -> None:
        """
        Convert an ion into an electrode when it becomes bound to the dendrimer.

        Args:
            nearest_electrode (Atom): Nearest (connected) electrode to this atom.
        """
        self.type = "electrode"
        self.parent_electrode = nearest_electrode
        self.generation = self.parent_electrode.generation + 1
        new_pos = Calculation.final_pos_optimalization(self)
        self.update_position(new_pos)

    def _set_fg_color (self, generation : int) -> Any:
        """
        Determine the atom color based on its generation in the dendrimer.

        Args:
            generation (int): Generation index of the particle (use -1 for a free ion).

        Returns:
            Any: Color specification for the atom, in the format used by the config.
        """
        if (generation == -1):
            return config.atom_color[-1]
        return config.atom_color[generation % 10]

    def _translate_sphere (self, pos : np.array) -> None:
        """
        Place or move the atom's visual sphere to the given position.

        Args:
            pos (np.array): 3D position of the atom in space.
        """
        self.sphere.transform = STTransform(translate=[pos[0], pos[1], pos[2]])
