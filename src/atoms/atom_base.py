from abc import ABC, abstractmethod
from typing import Any, Optional
from vispy import scene  # visualization of the simulation
from vispy.visuals.transforms import STTransform
import numpy as np

import config


class AtomBase(ABC):
    """
    Representation of a single atom.

    Attributes:
        position (np.array): 3D position of the atom in space.
        positions_list (list): List of all positions occupied during the simulation.
        sphere: Visual representation of the atom as a sphere.
        color: Color of the atom for visualization.
    """
    def __init__(self, position : np.array) -> None:
        """
        Initialize an Atom instance.

        Args:
            position (np.array): 3D position of the atom in space.
        """
        self.position = position
        self.positions_list = [self.position]
        self.sphere = None
        self.color = None

    def update_position(self, new_position : np.array) -> None:
        """
        Update the atom's current position.

        Args:
            new_position (np.array): New 3D position of the atom.
        """
        self.position = new_position
        self.positions_list.append(new_position)

    @abstractmethod
    def display(self, view, sim_time : str) -> None:
        """
        Display this atom in the given view for a specified simulation time.

        Args:
            view: The vispy view/window to render into.
            sim_time (str): Either START or FINISH to indicate which
                state to display.
        """

    def _display_sphere(self, view, position : np.array) -> None:
        """
        Create and place the sphere visual for this atom.

        Args:
            view: The vispy view/window to render into.
            position (np.array): 3D position where the sphere should be placed.
        """
        self.sphere = scene.visuals.Sphere(
            radius=config.ATOM_RADIUS,
            method='ico',
            parent=view.scene,
            color = self.color,
            edge_color = config.ATOM_EDGE_COLOR
            )
        self._translate_sphere(position)

    def _translate_sphere (self, pos : np.array) -> None:
        """
        Place or move the atom's visual sphere to the given position.

        Args:
            pos (np.array): 3D position of the atom in space.
        """
        self.sphere.transform = STTransform(translate=[pos[0], pos[1], pos[2]])

    @abstractmethod
    def _set_fg_color (self, generation : Optional[int] = None) -> Any:
        """
        Determine the atom color based on its generation in the dendrimer.

        Args:
            generation (Optional[int]): Generation index (use -1 for a free ion, or
                None if generation is not available).

        Returns:
            Any: Color specification for the atom (format taken from config).
        """
