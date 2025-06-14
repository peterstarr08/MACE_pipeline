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

