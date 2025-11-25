import numpy as np

from layout_generator import LayoutGenerator
from calculation import Calculation
from atoms.electrode import Electrode
from atoms.ion import Ion


class Simulation ():
    """
    Class that manages the simulation of dendrimer formation.

    Attributes:
        layout (str): Starting layout of free ions in space.
        atoms_num (int): Number of atoms in the simulation.
        ions (list): List of ion objects in the simulation.
        electrodes (list): List of electrode objects in the simulation.
        _radius_of_gyration (float): Gyration radius of the resulting dendrimer.
    """
    def __init__(self, layout : str, atoms_num : int) -> None:
        """
        Initialize the Simulation object.

        Args:
            layout (str): Starting layout of the simulation.
            atoms_num (int): Number of atoms in the simulation.
        """
        self.layout = layout
        self.atoms_num = atoms_num
        self.ions = []
        self.electrodes = []
        self._generate_ion_layout()
        self.electrode = self._generate_elecrode()
        self._calculate_simulation()
        self._radius_of_gyration = self._calc_gyration()
        self._gyration_to_db()

    def get_atoms(self) -> list:
        """
        Return list of all atoms.
        """
        return self.ions + self.electrodes

    def _generate_ion_layout (self) -> None:
        """
        Generate the initial layout of atoms using the layout generator.
        """
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            ion = Ion(coords[i])
            self.ions.append(ion)

    def _generate_elecrode(self) -> Electrode:
        """
        Create the first electrode before the simulation starts.

        Returns:
            Atom: Electrode placed at position (0, 0, 0).
        """
        electrode = Electrode(np.array([0, 0, 0]))
        electrode.parent_electrode = electrode
        self.electrodes.append(electrode)
        return electrode

    def _calculate_simulation (self) -> None:
        """
        Run the simulation calculation using the Calculation class.
        """
        calc = Calculation(self)
        calc.calculate_sim()

    def _calc_gyration (self) -> float:
        """
        Calculate the radius of gyration of the molecule.

        Returns:
            float: The radius of gyration.
        """
        atoms = self.electrodes + self.ions
        com = self._center_of_mass(atoms)
        r_pow2_sum = 0
        for atom in atoms:
            r_atom = np.linalg.norm(atom.position - com)
            r_pow2_sum += np.power(r_atom, 2)
        return np.sqrt(r_pow2_sum / self.atoms_num)

    def _center_of_mass (self, atoms : list) -> np.array:
        """
        Calculate the center of mass of the molecule.

        Args:
            atoms (list): List of all atoms in the simulation.

        Returns:
            np.array: The center of mass position.
        """
        pos_sum = np.array([0, 0, 0])
        for atom in atoms:
            pos_sum = pos_sum + atom.position
        return np.array(pos_sum / self.atoms_num)

    def _gyration_to_db (self) -> None:
        """
        Save N and Rg to the database.
        """
        with open ("database.txt", "a+", encoding="utf-8") as f:
            line = f"{self._radius_of_gyration} {self.atoms_num}\n"
            f.write(line)
