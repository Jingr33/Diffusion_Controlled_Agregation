from vispy import scene
from sim_state_type import SimStateType

class Visualizer():
    """
    Manages visualization.
    """
    def __init__(self, atoms : list[int]):
        """
        Initialize a visualizer object.
        
        Args:
            is_visualization (bool): Wether visualization is enabled.
        """
        self.atoms = atoms
        self.view_boxes = []
        self.sim_data = []

    def set_simulation_data(self, simulation_data : list) -> None:
        """
        Append simulation data into self.sim_data
        """
        self.sim_data.append(simulation_data)

    def visualize_simulation(self) -> None:
        """
        Visualize the start and end states of the simulation (if enabled).
        """
        self._init_scene()
        for i in range(len(self.view_boxes)):
            vb_group = self.view_boxes[i]
            self._display_sim_state(SimStateType.START, vb_group[0], i)
            self._display_sim_state(SimStateType.FINISH, vb_group[1], i)
        self.canvas.app.run()

    def _init_scene(self) -> None:
        """
        Initialize the scene (canvas and viewboxes) for visualization.
        """
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(1200, 750), show=True, fullscreen=True)
        grid = self.canvas.central_widget.add_grid()
        grid.padding = 10
        for i in range(len(self.sim_data)):
            vb_left = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
            vb_right = scene.widgets.ViewBox(border_color='gray', parent=self.canvas.scene)
            # grid layout
            grid.add_widget(vb_left, i, 0)
            grid.add_widget(vb_right, i, 1)
            # camera setup
            vb_left.camera = 'arcball'
            vb_left.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
            vb_right.camera = 'arcball'
            vb_right.camera.set_range(x=[-20, 20], y=[-20, 20], z=[-20, 20])
            self.view_boxes.append((vb_left, vb_right))

    def _display_sim_state (self, sim_time : str, viewbox, idx : int) -> None:
        """
        Display the selected state of the simulation in the given viewbox.

        Args:
            sim_time (str): Time state of the simulation (e.g. START or FINISH).
            viewbox: The viewbox in which to display the state.
            index (int): ...
        """
        atoms = self.sim_data[idx]
        for atom in atoms:
            atom.display(viewbox, sim_time)
