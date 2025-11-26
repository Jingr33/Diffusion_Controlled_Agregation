import matplotlib.pyplot as plt
import numpy as np


class ChartCreator ():
    """
    Create a chart at the end of the application run.

    Chart content:
        log N (number of particles in the simulation) vs. log Rg (gyration radius).
        Shows the estimated fractal dimension of dendrimers created from a layout.
    """

    def __init__(self):
        """
        Initialize the chart creator.
        """
        self.atoms_numbers = []
        self.gyrations = []
        self._load_data()
        self._calc_data()
        self._plot()

    def _load_data (self) -> None:
        """
        Load data from the database file.
        """
        lines = []
        with open ("database_cube.txt", "r+", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            data = line.split(" ")
            self.gyrations.append(float(data[0]))
            self.atoms_numbers.append(int(data[1]))

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
        if self.log_rg.size <= 0 or self.log_n.size <= 0:
            print("No data to plot.")
            return
        plt.scatter(self.log_rg, self.log_n, color="#3288bd")
        plt.plot(self.log_rg, self.p(self.log_rg), linestyle="dotted")
        plt.title(f"Závislost logaritmu počtu atomů na logaritmu gyračního poloměru\nFraktální dimenze Df = {self.fractal_dimension}")
        plt.xlabel("log Rg")
        plt.ylabel("log N")
        plt.show()
