import numpy as np

import config

class LayoutGenerator ():
    """
    Generate a list of 3D vectors representing starting positions for atoms.
    """

    def __init__(self, layout : str, atoms_num : int):
        """
        Initialize LayoutGenerator.

        Args:
            layout (str): type of starting layout ("cube", "sphere", or "random").
            atoms_num (int): number of atoms in the system.
        """
        self.atoms_num = atoms_num
        if layout == config.LAYOUTS[0]:
            self.start_postions = self._gen_cube_layout()
        elif layout == config.LAYOUTS[1]:
            self.start_postions = self._gen_sphere_layout()
        elif layout == config.LAYOUTS[2]:
            self.start_postions = self._gen_random_layout()

    def get_start_pos (self) -> list:
        """
        Return the list of starting positions for free ions.
        """
        return self.start_postions

    def _gen_cube_layout(self) -> list:
        """
        Generate a random layout of atoms on the surface of a cube.

        Returns:
            list[np.array]: List of positions for each free ion at the start of the simulation.
        """
        coord_list = [None] * self.atoms_num
        half_edge = np.power(self.atoms_num, 0.56)
        for i in range(self.atoms_num):
            rnd_coord = np.random.randint(0, 3)
            rnd_side = np.random.choice([-1, 1])
            position = np.array([0.0, 0.0, 0.0])
            position[rnd_coord] = half_edge * rnd_side
            for j in range(len(position)):
                if position[j] != 0:
                    continue
                position[j] = np.random.uniform(-half_edge, half_edge)
            coord_list[i] = position
        return coord_list

    def _gen_sphere_layout(self) -> list:
        """
        Generate a random layout of atoms on the surface of a sphere.

        Returns:
            list[np.array]: List of positions for each free ion at the start of the simulation.
        """
        coord_list = [None] * self.atoms_num
        r = np.power(self.atoms_num, 0.5) * 2
        for i in range(self.atoms_num):
            phi = np.random.uniform(0, np.pi)
            theta = np.random.uniform(0, 2 * np.pi)
            x = r * np.cos(phi) * np.sin(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(theta)
            coord_list[i] = np.array([x, y, z])
        return coord_list

    def _gen_random_layout(self) -> list:
        """
        Generate a random layout of atoms in space.

        Returns:
            list[np.array]: List of positions for each free ion at the start of the simulation.
        """
        max_radius = int(np.ceil(np.power(self.atoms_num, 0.5)))
        coord_list = [None] * self.atoms_num
        for i in range(self.atoms_num):
            x = np.random.randint(-max_radius, max_radius + 1)
            y = np.random.randint(-max_radius, max_radius + 1)
            z = np.random.randint(-max_radius, max_radius + 1)
            coord_list[i] = np.array([x, y, z])
        return coord_list
    