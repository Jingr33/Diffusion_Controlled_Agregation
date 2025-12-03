# Diffusion Controlled Aggregation

## Overview

This application simulates the formation of dendrimers through diffusion controlled aggregation during electrolysis. The simulation models the growth of dendritic structures as free ions diffuse in a biased random walk towards existing electrodes (growing dendrimer), where they bind and become part of the structure.

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

#### Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--layout` | string | `random` | Initial ion distribution layout. Choices: `cube`, `sphere`, `random` |
| `--atoms` | int (multiple) | `10 100` | Number of ions in each simulation (space-separated list) |
| `--sim` | flag | `True` | Run the simulation |
| `--visualize` | flag | `True` | Display visualization of initial and final dendrimer states |
| `--plot` | flag | `True` | Plot log N vs log Rg graph and calculate fractal dimension |
| `--clean_db` | flag | `False` | Clear all previous results from database before running |

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

#### Clean database and remove previous results
```bash
python src/main.py --clean_db True --atoms 500
```

## Configuration

Edit `src/config.py` to customize simulation parameters.
