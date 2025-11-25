from typing import Any, Optional
import numpy as np

import config
from sim_state_type import SimStateType
from atoms.atom_base import AtomBase


class Electrode(AtomBase):
    """
    Representation of a electrode particle.

    Attributes:
        position (np.array): 3D position of the atom in space.
        generation (int): Generation index of the particle within the dendrimer.
        positions_list (list): List of all positions occupied during the simulation.
    """
    def __init__(self, position : np.array) -> None:
        """
        Initialize an Atom instance.

        Args:
            position (np.array): 3D position of the atom in space.
        """
        super().__init__(position)
        self.generation = 0
        self.orig_generation = self.generation
        self.parent_electrode = None

    def display(self, view, sim_time : str) -> None:
        """
        Display the atom as a sphere in the visualization.

        Args:
            view (vispy.scene.visuals): View window for the simulation.
            sim_time (str): START or FINISH (initial or final state).
        """
        generation = self.generation if sim_time != SimStateType.START else self.orig_generation
        position = self.positions_list[0] if sim_time == SimStateType.FINISH else self.positions_list[-1]
        self.color = self._set_fg_color(generation)
        self._display_sphere(view, position)

    def _set_fg_color (self, generation : Optional[int] = None) -> Any:
        """
        Determine the electrode color based on its generation in the dendrimer.

        Args:
            generation (int): Generation index of the particle .

        Returns:
            Any: Color specification for the atom, in the format used by the config.
        """
        if generation is None:
            return config.ATOM_COLORS[-1]
        return config.ATOM_COLORS[generation % (len(config.ATOM_COLORS) - 1)]
