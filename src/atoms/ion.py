from typing import Any, Optional
import numpy as np

import config
from calculation import Calculation
from sim_state_type import SimStateType
from atoms.atom_base import AtomBase
from atoms.electrode import Electrode


class Ion(AtomBase):
    """
    Representation of a single ion particle.

    Attributes:
        position (np.array): 3D position of the atom in space.
        positions_list (list): List of all positions occupied during the simulation.
        electrode_dist (float): Distance to the nearest electrode position.
        parent_electrode (Atom): For ions: None. For electrodes: reference to the
            neighboring electrode with lower generation.
    """
    def __init__(self, position: np.ndarray) -> None:
        """
        Initialize an Ion instance.

        Args:
            position (np.ndarray): 3D position of the ion in space [x, y, z].
        """
        super().__init__(position)
        self.electrode_dist = Calculation.vec_magnitude(Calculation.opposite_direction(self.position))

    def display(self, view, sim_time: str) -> None:
        """
        Display the ion as a sphere in the visualization.

        Args:
            view (vispy.scene.visuals): View window for the simulation.
            sim_time (str): START or FINISH (initial or final state).
        """
        position = self.positions_list[0] if sim_time == SimStateType.START else self.positions_list[-1]
        self.color = self._set_fg_color()
        self._display_sphere(view, position)

    def transform_to_electrode(self, nearest_electrode) -> None:
        """
        Convert an ion into an electrode when it becomes bound to the dendrimer.

        Args:
            nearest_electrode (Electrode): Nearest (parent) electrode to this ion.
        """
        self.__class__ = Electrode
        self.parent_electrode = nearest_electrode
        self.generation = self.parent_electrode.generation + 1
        self.orig_generation = None
        new_pos = Calculation.final_pos_optimalization(self)
        self.update_position(new_pos)

    def _set_fg_color(self, generation: Optional[int] = None) -> Any:
        """
        Determine an ion color.

        Args:
            generation (Optional[int]): Generation index (always -1 for free ions).

        Returns:
            Any: Color specification for the ion from config.ATOM_COLORS[-1].
        """
        return config.ATOM_COLORS[-1]
