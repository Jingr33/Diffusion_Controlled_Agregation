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
            master (Simulation): Parent simulation instance.
        """
        self.master = simulation
        self.ions = simulation.ions
        self.electrodes = simulation.electrodes

    def calculate_sim (self) -> None:
        """
        Perform all simulation steps until all ions become electrodes.

        The simulation advances while there is at least one free particle in space;
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

    def final_pos_optimalization (atom) -> np.array:
        """
        Optimize a particle's position when the ion is bound to the dendrimer
        and comes to rest.

        Args:
            atom (Atom): Atom of interest.

        Returns:
            np.array: Adjusted position of the atom in space.
        """
        electrode_pos = atom.parent_electrode.position
        elec_to_ion = np.array(atom.position - electrode_pos)
        distance = np.linalg.norm(elec_to_ion)
        if distance == 0:
            return np.array(atom.position)
        norm_elec_to_ion = np.array(elec_to_ion / distance)
        return np.array(electrode_pos + norm_elec_to_ion * 2 * config.ATOM_RADIUS)


    def vec_magnitude (vector : np.array) -> float:
        """
        Return the magnitude of a vector.

        Args:
            vector (np.array): Input vector.

        Returns:
            float: Magnitude of the vector.
        """
        return np.linalg.norm(vector)

    def opposite_direction (vector : np.array) -> np.array:
        """
        Return the opposite direction of a 3D vector.

        Args:
            vector (np.array): Input vector.

        Returns:
            np.array: Vector pointing in the opposite direction.
        """
        return (-vector[0], -vector[1], -vector[2])

    def _shortest_electrode_dist(self, ion):
        """
        Calculate the distance from an ion to the nearest electrode of the dendrimer.

        Args:
            ion (Atom): Atom of interest.

        Returns:
            float: Shortest distance to the nearest electrode.
            Atom: The nearest electrode object.
        """
        shortest_dist = 1000
        nearest_elec = self.master.electrode
        for electrode in self.electrodes:
            actual_distance = np.linalg.norm(ion.position - electrode.position)
            if actual_distance < shortest_dist:
                shortest_dist = actual_distance
                nearest_elec = electrode
        return shortest_dist, nearest_elec

    def _is_electrode (self, ion, nearest_electrode) -> bool:
        """
        Check whether a free ion is close enough to an electrode.

        If the ion is within the bonding threshold, transform its attributes
        to electrode configuration, reassign it to the electrode group, and
        return True.

        Args:
            ion (Atom): Atom of interest.
            nearest_electrode (Atom): Nearest electrode to the atom.

        Returns:
            bool: True if the ion was transformed into an electrode; otherwise False.
        """
        if ion.electrode_dist <= config.ATOM_RADIUS*2 + config.STEP/2:
            self.ions.remove(ion)
            ion.transform_to_electrode(nearest_electrode)
            self.electrodes.append(ion)
            return True
        return False

    def _gen_biased_vector (self, ion, nearest_electrode) -> np.array:
        """
        Calculate a biased motion vector for the atom.

        The returned vector is a normalized combination of the preferred
        direction (towards the nearest electrode, weighted by a probability
        from the config) and a random direction (weighted by 1 - probability).

        Args:
            ion (Atom): Atom of interest.
            nearest_electrode (Atom): Nearest electrode of the dendrimer.

        Returns:
            np.array: Normalized motion vector for the atom.
        """
        probability = config.DIREC_PROB
        pref_direc = nearest_electrode.position - ion.position
        norm_pref_direc = pref_direc / np.linalg.norm(pref_direc)
        rand_direc = np.random.randn(3)
        norm_rand_direc = rand_direc / np.linalg.norm(rand_direc)
        biased_vec = (1 - probability) * norm_rand_direc + probability * norm_pref_direc
        return np.array(biased_vec / np.linalg.norm(biased_vec))
