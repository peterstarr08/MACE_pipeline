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
        if isinstance(cfg[key], bool):
            if cfg[key]:
                args.append(f'--{key}')
        else:
            args += [f'--{key}', str(cfg[key])]
    return args

def run(args: list[str]):
    lg.info("Arguments: %s", " ".join(args))
    subprocess.run(md_run_openmm_cli + args, check=True)

def mace_md(conf_path: str):
    lg.info("Reading md_run config")
    cfg = yaml_reader(conf_path)
    lg.info("Parsing arguments")
    args = get_args(cfg)
    lg.info("Beginning simulation")
    run(args)
    lg.info("Simulation finished")
    
    