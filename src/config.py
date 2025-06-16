from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#==============Paths Dir==================
# Folder paths
RAWDATA_DIR = "raw_dataset"
DATASET_DIR = "dataset"

# File paths
DATABASE_FILE = "db_mace.sqlite3"

#============Paths========================
db_path = ROOT / DATABASE_FILE
dataset_path = ROOT / DATASET_DIR
raw_dataset_path = ROOT / RAWDATA_DIR


#=================Args=======================

#Samplers
uniform_samp_key = "uniform"
fps_samp_key = "fps"
calculator_keys=['xtb']

#===============Better not thouch thses. I'll find ya if u do====================
DEFAULT_XTB_METHOD = "GFN2-xTB"
ISOLATED_ATOM_KEY = "IsolatedAtom"

xtb_energy_key = "energy_xtb"
xtb_forces_key = "forces_xtb"

#Uniform Selector key
us_0_selected = "us_0"
us_off_selected = "us_offset"