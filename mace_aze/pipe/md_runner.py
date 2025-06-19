from mace_aze.log.conf import get_logger
from .conf import md_run_openmm_cli
import subprocess
import yaml

lg = get_logger(__name__)

def yaml_reader(path: str):
    with open(path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_args(cfg: dict):
    args = []
    for key in cfg.keys():
        args += [f'--{key}', str(cfg[key])]
    return args

def run(args: list[str]):
    subprocess.run(md_run_openmm_cli + args, check=True)

def mace_md(conf_path: str):
    lg.info("Reading md_run config")
    cfg = yaml_reader(conf_path)
    lg.info("Parsing arguments")
    args = get_args(cfg)
    lg.info("Beginning simulation")
    run(args)
    lg.info("Simulation finished")
    
    