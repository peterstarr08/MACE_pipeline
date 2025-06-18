from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#==============Paths Dir==================
# Folder paths
RAWDATA_DIR = "raw_dataset"
DATASET_DIR = "dataset"
MODEL_DIR = "models"

# File paths
DATABASE_FILE = "db_mace.sqlite3"

#============Paths========================
db_path = ROOT / DATABASE_FILE
dataset_path = ROOT / DATASET_DIR
raw_dataset_path = ROOT / RAWDATA_DIR
model_path = ROOT / MODEL_DIR



#===============Better not thouch thses. I'll find ya if u do====================
#Uniform Selector key
us_0_selected = "us_0"
us_off_selected = "us_offset"