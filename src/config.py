"""
Configuration of the app.
"""

from layout.layout import Layout

# ARGUMENTS
LAYOUT_DEFAULT = Layout.RANDOM
ATOMS_DEFAULT = [10, 100]
SIM_DEFAULT = True
VISUALIZATION_DEFAULT = True
PLOT_DFAULT = True
CLEAN_DB_DEFAULT = True

#COLORS
ATOM_EDGE_COLOR = (0.5, 0.5, 0.5, 0.5)
ATOM_COLORS = {
    -1 : "#87CEEB", # ion color
    0 : "#9e0142", # electrode generation colors
    1 : "#d53e4f",
    2 : "#f46d43",
    3 : "#fdae61",
    4 : "#fee08b",
    5 : "#e6f598",
    6 : "#abdda4",
    7 : "#66c2a5",
    8 : "#3288bd",
    9 : "#5e4fa2",
}

#SIMULATION
STEP = 0.25
DIREC_PROB = 0.1

# DISPLAY
ATOM_RADIUS = 0.7
