import numpy as np

import config

class Calculation ():
    """
    This class manages all numerical calculations for the simulation.

    Attributes:
        simulation (Simulation): Parent simulation instance.
        ions (list): List of all ion objects in the simulation.
        electrodes (list): List of all electrode objects in the simulation.
    """
    def __init__(self, simulation) -> None:
        """
        Initialize the Calculation helper.

        Args:
            simulation (Simulation): Parent simulation instance.
        """
        self.master = simulation
        self.ions = simulation.ions
        self.electrodes = simulation.electrodes

    def calculate_sim(self) -> None:
        """
        Perform all simulation steps until all free ions become electrodes.

        The simulation advances while there is at least one free ion in space;
        otherwise the calculation (and the whole simulation) terminates.
        """
        while len(self.ions) != 0:
            for ion in self.ions:
                shortest_dist, nearest_elec = self._shortest_electrode_dist(ion)
                if self._is_electrode(ion, nearest_elec):
                    continue
                ion.electrode_dist = shortest_dist
                shift_vec = self._gen_biased_vector(ion, nearest_elec)
                ion.update_position(ion.position + shift_vec * config.STEP)

    @staticmethod
    def final_pos_optimalization(atom) -> np.ndarray:
        """
        Optimize a particle's final position when the ion is bound to the dendrimer.

        Args:
            atom (Atom): Atom of interest.

        Returns:
            np.ndarray: Adjusted position of the atom at exactly 2*ATOM_RADIUS distance from parent.
        """
        electrode_pos = atom.parent_electrode.position
        elec_to_ion = np.array(atom.position - electrode_pos)
        distance = np.linalg.norm(elec_to_ion)
        if distance == 0:
            return np.array(atom.position)
        norm_elec_to_ion = np.array(elec_to_ion / distance)
        return np.array(electrode_pos + norm_elec_to_ion * 2 * config.ATOM_RADIUS)


    @staticmethod
    def vec_magnitude(vector: np.ndarray) -> float:
        """
        Calculate the magnitude (Euclidean norm) of a vector.

        Args:
            vector (np.ndarray): Input vector.

        Returns:
            float: Magnitude of the vector.
        """
        return np.linalg.norm(vector)

    @staticmethod
    def opposite_direction(vector: np.ndarray) -> tuple:
        """
        Calculate the opposite direction of a 3D vector.

        Args:
            vector (np.ndarray): Input vector with three components [x, y, z].

        Returns:
            tuple: Vector pointing in the opposite direction [-x, -y, -z].
        """
        return (-vector[0], -vector[1], -vector[2])

    def _shortest_electrode_dist(self, ion):
        """
        Calculate the distance from an ion to the nearest electrode of the dendrimer.

        Args:
            ion (Ion): Free ion of interest.

        Returns:
            tuple: (float, Electrode) - shortest distance and the nearest electrode object.
        """
        shortest_dist = 1000
        nearest_elec = self.master.electrode
        for electrode in self.electrodes:
            actual_distance = np.linalg.norm(ion.position - electrode.position)
            if actual_distance < shortest_dist:
                shortest_dist = actual_distance
                nearest_elec = electrode
        return shortest_dist, nearest_elec

    def _is_electrode(self, ion, nearest_electrode) -> bool:
        """
        Check whether a free ion is close enough to an electrode to bond.

        If the ion is within the bonding threshold, transform its attributes
        to electrode configuration, reassign it to the electrode group, and
        return True.

        Args:
            ion (Ion): Free ion of interest.
            nearest_electrode (Electrode): Nearest electrode to the ion.

        Returns:
            bool: True if the ion was transformed into an electrode; otherwise False.
        """
        if ion.electrode_dist <= config.ATOM_RADIUS*2 + config.STEP/2:
            self.ions.remove(ion)
            ion.transform_to_electrode(nearest_electrode)
            self.electrodes.append(ion)
            return True
        return False

    def _gen_biased_vector(self, ion, nearest_electrode) -> np.ndarray:
        """
        Calculate a biased motion vector for the ion.

        The returned vector is a normalized combination of the preferred
        direction (towards the nearest electrode, weighted by DIREC_PROB)
        and a random direction (weighted by 1 - DIREC_PROB).

        Args:
            ion (Ion): Free ion of interest.
            nearest_electrode (Electrode): Nearest electrode of the dendrimer.

        Returns:
            np.ndarray: Normalized motion vector for the ion movement.
        """
        probability = config.DIREC_PROB
        pref_direc = nearest_electrode.position - ion.position
        norm_pref_direc = pref_direc / np.linalg.norm(pref_direc)
        rand_direc = np.random.randn(3)
        norm_rand_direc = rand_direc / np.linalg.norm(rand_direc)
        biased_vec = (1 - probability) * norm_rand_direc + probability * norm_pref_direc
        return np.array(biased_vec / np.linalg.norm(biased_vec))
