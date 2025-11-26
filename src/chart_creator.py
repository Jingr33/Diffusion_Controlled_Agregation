import matplotlib.pyplot as plt
import numpy as np

from DI_container import injector
from layout.layout import Layout
from database.services.gyration_ratio_service import GyrationRatioService


class ChartCreator ():
    """
    Create a chart at the end of the application run.

    Chart content:
        log N (number of particles in the simulation) vs. log Rg (gyration radius).
        Shows the estimated fractal dimension of dendrimers created from a layout.
    """

    def __init__(self, layout : Layout):
        """
        Initialize the chart creator.
        """
        self._gyratio_ratio_service = injector.get(GyrationRatioService)
        self.layout = layout
        self.atoms_numbers = []
        self.gyrations = []
        self._load_simulation_data_from_db()
        self._calc_data()
        self._plot()

    def _load_simulation_data_from_db (self) -> None:
        """
        Load data from the database.
        """
        simulation_data = self._gyratio_ratio_service.get_all_gyration_ratios_with_layout(self.layout)
        self.gyrations = [
            (
                x.cube_gr if self.layout == Layout.CUBE
                else x.sphere_gr if self.layout == Layout.SPHERE
                else x.random_gr
            )
            for x in simulation_data
        ]
        self.atoms_numbers = [x.atoms for x in simulation_data]

    def _calc_data (self) -> None:
        """
        Prepare data for the chart and calculate the fractal dimension of the dendrimers.
        """
        self.log_n = np.log10(self.atoms_numbers)
        self.log_rg = np.log10(self.gyrations)
        coeffs = np.polyfit(self.log_rg, self.log_n, 1)
        self.p = np.poly1d(coeffs)
        self.fractal_dimension = np.round(coeffs[0], 4)

    def _plot(self) -> None:
        """
        Plot the data.
        """
        plt.scatter(self.log_rg, self.log_n, color="#3288bd")
        plt.plot(self.log_rg, self.p(self.log_rg), linestyle="dotted")
        plt.title(f"Závislost logaritmu počtu atomů na logaritmu gyračního poloměru\nFraktální dimenze Df = {self.fractal_dimension}")
        plt.xlabel("log Rg")
        plt.ylabel("log N")
        plt.show(block=True)
