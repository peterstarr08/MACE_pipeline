from mace_aze.log.conf import get_logger
import warnings
warnings.filterwarnings("ignore")
from mace.cli.run_train import main as mace_run_train_main
import sys

lg = get_logger(__name__)

def train_mace(config_file_path):
    sys.argv = ["program", "--config", config_file_path]
    mace_run_train_main()