from vispy import scene
import numpy as np

from layout_generator import LayoutGenerator
from calculation import Calculation
from atom import Atom


class Simulation ():
    """
    Class that manages the simulation of dendrimer formation and its
    visualization.

    Attributes:
        layout (str): Starting layout of free ions in space.
        atoms_num (int): Number of atoms in the simulation.
        ions (list): List of ion objects in the simulation.
        electrodes (list): List of electrode objects in the simulation.
        _radius_of_gyration (float): Gyration radius of the resulting dendrimer.
        canvas (scene): Visualization canvas.
        vb1: First viewbox for visualization.
        vb2: Second viewbox for visualization.
    """
    def __init__(self, layout : str, atoms_num : int, visualize : bool) -> None:
        """
        Initialize the Simulation object.

        Args:
            layout (str): Starting layout of the simulation.
            atoms_num (int): Number of atoms in the simulation.
            visualize (bool): Whether visualization is enabled.
        """
        self.layout = layout
        self.atoms_num = atoms_num
        self.ions = []
        self.electrodes = []
        self.atoms = []
        self._generate_ion_layout()
        self.electrode = self._generate_elecrode()
        self._calculate_simulation()
        if (visualize):
            self._visualize()
        self._radius_of_gyration = self._calc_gyration()
        self._gyration_to_db()

    def run(self) -> None:
        """
        Start the visualization.
        """
        self.canvas.app.run()

    def _generate_ion_layout (self) -> None:
        """
        Generate the initial layout of atoms using the layout generator.
        """
        layout_gen = LayoutGenerator(self.layout, self.atoms_num)
        coords = layout_gen.get_start_pos()
        for i in range(self.atoms_num):
            atom = Atom("ion", coords[i])
            self.ions.append(atom)

    def _generate_elecrode(self) -> Atom:
        """
        Create the first electrode before the simulation starts.

        Returns:
            Atom: Electrode placed at position (0, 0, 0).
        """
        electrode = Atom("electrode", np.array([0, 0, 0]))
        electrode.parent_electrode = electrode
        self.ions.append(electrode)
        return electrode

    def _calculate_simulation (self) -> None:
        """
        Run the simulation calculation using the Calculation class.
        """
        calc = Calculation(self)
        calc.calculate_sim()
    
    def _visualize(self) -> None:
        """
        Visualize the start and end states of the simulation (if enabled).
        """
        self._init_scene()
        self._display_sim_state("start", self.vb1)
        self._display_sim_state("finish", self.vb2)

    def _init_scene(self) -> None:
        """
        Initialize the scene (canvas and viewboxes) for visualization.
        """
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(1200, 750), show=True, fullscreen=True)
        self.vb1 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        self.vb2 = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
        # grid layout
        grid = self.canvas.central_widget.add_grid()
        grid.padding = 10
        grid.add_widget(self.vb1, 0, 0)
        grid.add_widget(self.vb2, 0, 1)
        # camera setup
        self.vb1.camera = 'arcball'
        self.vb1.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
        self.vb2.camera = 'arcball'
        self.vb2.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])

    def _display_sim_state (self, sim_time : str, viewbox) -> None:
        """
        Display the selected state of the simulation in the given viewbox.

        Args:
            sim_time (str): Time state of the simulation (e.g. "start" or "finish").
            viewbox: The viewbox in which to display the state.
        """
        self.atoms = self.ions + self.electrodes
        for atom in self.atoms:
            atom.display(viewbox, sim_time)        

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
            r_pow2_sum += np.pow(r_atom, 2)
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
        with open ("database.txt", "a+") as f:
            line = f"{self._radius_of_gyration} {self.atoms_num}\n"
            f.write(line)