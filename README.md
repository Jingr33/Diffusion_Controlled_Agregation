# Diffusion Controlled Aggregation

## Overview

This application simulates the formation of dendrimers through diffusion-controlled aggregation during electrolysis. The simulation models the growth of dendritic structures as free ions diffuse in a biased random walk towards existing electrodes (growing dendrimer), where they bind and become part of the structure.

### Key Features

- **3D Simulation**: Realistic dendrimer growth in three-dimensional space
- **Multiple Layout Options**: Support for cube, sphere, and random initial ion distributions
- **Interactive Visualization**: Real-time visualization of initial and final dendrimer states
- **Fractal Analysis**: Calculation and plotting of the fractal dimension (Df) of generated structures
- **Database Storage**: Persistent storage of simulation results for analysis

## How It Works

### Simulation Process

1. **Ion Initialization**: Free ions are randomly distributed in space according to the selected layout (cube, sphere, or random)
2. **Diffusion**: Each ion performs a biased random walk toward the nearest electrode
3. **Binding**: When an ion gets sufficiently close (within 2×ATOM_RADIUS) to an electrode, it binds and becomes part of the dendrimer
4. **Growth**: The process repeats until all ions are bound, forming a complete dendrimer structure

### Physics Model

- **Biased Random Walk**: Ion movement combines:
  - Random diffusion (weighted by 1 - DIREC_PROB)
  - Directed motion toward nearest electrode (weighted by DIREC_PROB)
  
- **Step Size**: Controlled by the `STEP` parameter in `config.py`
- **Probability Bias**: Controlled by the `DIREC_PROB` parameter

## Installation

### Prerequisites

- Python 3.8+
- SQL Server (for database storage)
- Required packages (see below)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jingr33/Diffusion_Controlled_Agregation.git
   cd Diffusion_Controlled_Agregation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   Create a `.env` file in the root directory to override database settings:
   ```
   DB_DRIVER={ODBC Driver 17 for SQL Server}
   DB_SERVER=localhost
   DB_NAME=DiffusionControlledAgregationDB
   DB_USER=sa
   DB_PASS=your_password
   ```

4. **Initialize database**:
   The database will be created automatically on first run with proper migrations.

## Usage

### Basic Command

Run the simulation with default parameters:
```bash
python src/main.py
```

### Command-Line Arguments

```bash
python src/main.py [OPTIONS]
```

#### Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--layout` | string | `random` | Initial ion distribution layout. Choices: `cube`, `sphere`, `random` |
| `--atoms` | int (multiple) | `10 100` | Number of ions in each simulation (space-separated list) |
| `--sim` | flag | `True` | Run the simulation |
| `--visualize` | flag | `True` | Display visualization of initial and final dendrimer states |
| `--plot` | flag | `True` | Plot log N vs log Rg graph and calculate fractal dimension |
| `--clean_db` | flag | `True` | Clear all previous results from database before running |

### Examples

#### Run simulations for different ion counts with cube layout
```bash
python src/main.py --layout cube --atoms 50 100 200 --sim --visualize
```

#### Run only visualization without simulation
```bash
python src/main.py --sim False --visualize
```

#### Run simulation, skip visualization but plot results
```bash
python src/main.py --atoms 100 200 300 --visualize False --plot
```

#### Don't clean database and keep previous results
```bash
python src/main.py --clean_db False --atoms 500
```

## Configuration

Edit `src/config.py` to customize simulation parameters:

### Key Parameters

```python
# Initial layout and atom count defaults
LAYOUT_DEFAULT = Layout.RANDOM
ATOMS_DEFAULT = [10, 100]

# Simulation physics
STEP = 0.25                  # Distance each ion moves per step
DIREC_PROB = 0.1            # Probability of biased direction (0-1)

# Visualization
ATOM_RADIUS = 0.7           # Sphere radius in visualization

# Color mapping for generations
ATOM_COLORS = {
    -1: "#87CEEB",  # Free ions (blue)
    0: "#9e0142",   # Generation 0 (dark red)
    # ... colors for subsequent generations
}
```

## Output

### Visualization

- **Left Column**: Initial state (only the electrode at origin)
- **Right Column**: Final dendrimer structure after simulation
- **Colors**: Represent generation levels (distance from initial electrode)
- **Interactive**: Use mouse to rotate, zoom, and pan (ArcBall camera)

### Fractal Dimension Plot

The plot displays:
- **X-axis**: log(Rg) - logarithm of radius of gyration
- **Y-axis**: log(N) - logarithm of number of particles
- **Line**: Linear fit showing fractal dimension
- **Fractal Dimension (Df)**: Printed in title

The fractal dimension indicates the structure type:
- Df ≈ 1.7 - 1.8: Cluster Aggregation (DLA-like)
- Df ≈ 2.0 - 2.5: Random Walk Aggregation
- Df ≈ 3.0: Dense structure

## Project Structure

```
Diffusion_Controlled_Agregation/
├── src/
│   ├── main.py                    # Entry point
│   ├── config.py                  # Configuration constants
│   ├── simulation.py              # Main simulation class
│   ├── calculation.py             # Numerical calculations
│   ├── visualizer.py              # 3D visualization
│   ├── chart_creator.py           # Fractal dimension plotting
│   ├── sim_state_type.py          # Enum for simulation states
│   ├── DI_container.py            # Dependency injection setup
│   ├── app_module.py              # Module configuration
│   │
│   ├── atoms/
│   │   ├── atom_base.py           # Abstract base class
│   │   ├── ion.py                 # Free ion class
│   │   ├── electrode.py           # Electrode/dendrimer node class
│   │   └── atom_type.py           # Atom type enum
│   │
│   ├── layout/
│   │   ├── layout.py              # Layout type enum
│   │   └── layout_generator.py    # Initial position generation
│   │
│   └── database/
│       ├── db_runner.py           # Database initialization
│       ├── db_cleaner.py          # Database cleaning
│       ├── db_connect.py          # Connection management
│       ├── db_config.py           # Database configuration
│       ├── models/
│       │   ├── base.py            # SQLAlchemy base
│       │   └── gyration_ratio.py  # Data model
│       ├── repositories/
│       │   └── gyration_ratio_repository.py   # Data access
│       └── services/
│           └── gyration_ratio_service.py      # Business logic
│
├── alembic/                       # Database migrations
├── alembic.ini                    # Alembic configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Input Parameters Reference

### Simulation Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `--layout` | enum | cube, sphere, random | random | Initial ion distribution |
| `--atoms` | list[int] | 1-10000 | [10, 100] | Number of ions per simulation |
| `--sim` | bool | true/false | true | Enable simulation execution |
| `--visualize` | bool | true/false | true | Show 3D visualization |
| `--plot` | bool | true/false | true | Display fractal dimension plot |
| `--clean_db` | bool | true/false | true | Clear database before run |

### Physics Configuration (config.py)

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `STEP` | float | 0.01-1.0 | 0.25 | Distance per diffusion step |
| `DIREC_PROB` | float | 0.0-1.0 | 0.1 | Probability bias toward electrode |
| `ATOM_RADIUS` | float | 0.1-2.0 | 0.7 | Visual sphere radius |

## Dependencies

- **alembic** (≥1.16.5): Database migrations
- **SQLAlchemy** (≥2.0.43): ORM and database layer
- **vispy** (0.14.3): 3D visualization
- **numpy** (≥1.26.4): Numerical computations
- **injector** (≥0.22.0): Dependency injection
- **pyodbc** (≥5.1.0): SQL Server connection
- **matplotlib** (≥3.8.0): Plotting and analysis

## Performance Considerations

- **Small simulations** (N < 500): < 1 second
- **Medium simulations** (500 < N < 5000): 5-30 seconds
- **Large simulations** (N > 5000): > 1 minute

Memory usage scales linearly with atom count (~1 MB per 1000 atoms).

## Troubleshooting

### Database Connection Issues

**Problem**: "Failed to connect to SQL Server"

**Solution**:
1. Verify SQL Server is running
2. Check `DB_SERVER`, `DB_USER`, `DB_PASS` in `.env` or `db_config.py`
3. Ensure ODBC driver is installed: `{ODBC Driver 17 for SQL Server}`

### Visualization Not Displaying

**Problem**: Visualization window doesn't appear

**Solution**:
- Ensure you're running on a system with GPU support
- Try `--visualize False` to skip visualization
- Check graphics drivers are up to date

### Out of Memory Error

**Problem**: Application crashes with memory error on large simulations

**Solution**:
- Reduce `--atoms` count
- Increase available system RAM
- Run simulations sequentially rather than in parallel

## Scientific Background

### Dendrimer Growth Models

This simulation implements a diffusion-limited aggregation (DLA) model similar to those found in:
- Electrochemical deposition
- Colloidal aggregation
- Fractal growth phenomena

### References

- Witten, T. A., & Sander, L. M. (1981). Diffusion-limited aggregation
- Meakin, P. (1992). Models for dendritic growth
- Jullien, R., & Botet, R. (1987). Aggregation and fractal aggregates

## License

This project is provided as-is for research and educational purposes.

## Contact

For questions or issues, please refer to the project repository.
