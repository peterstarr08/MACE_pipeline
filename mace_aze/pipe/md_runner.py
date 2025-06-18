from mace_aze.log.conf import get_logger
from .conf import md_run_openmm_cli
import subprocess

lg = get_logger(__name__)

def mace_md(*args):
    subprocess.run(md_run_openmm_cli + list(args), check=True)