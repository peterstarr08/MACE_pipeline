from pathlib import Path

from mace_aze.log.conf import get_logger
from mace_aze.calculators import MACEculator
from mace_aze.log.conf import get_logger
from mace_aze.utils.io import read_trajectory
from mace_aze.utils.mace_md_log_paraser import get_temp

from ase.io import write

log = get_logger(__name__)

def attach_temperatures(configs, temperature):
    log.info("Attching temperature data")
    log.debug("%d configs   %d temp_points", len(configs), len(temperature))
    if len(configs)!=len(temperature):
        log.error("Length mismatch. This can cause incorrect labelling on configs but continuing")
    for at, temp in zip(configs, temperature):
        at.info['temperature_K'] = temp
        log.debug("Attached %s", str(temp))

def get_write_path(traj_path: str):
    return Path(traj_path).parent / "trajectory.xyz"

def comm_eval(model_paths: list[str], traj_path: list[str]):
    log.info("Initiating committee model evaluation")
    traj = read_trajectory(traj_path)
    log.info("Trajectory counts: %d", len(traj))
    traj = [at for at in traj if len(at) > 0]
    log.info("Trajectory loaded: %d frames after removing empty configs", len(traj))

    temp = get_temp(traj_path)

    calc = MACEculator(model_paths)
    calc.calculate(traj)

    if len(temp):
        attach_temperatures(traj, temp)
    else:
        log.warning("No temperature data found skipping")

    out_path = get_write_path(traj_path)
    log.info("Writing %s", str(out_path))
    write(out_path, traj)
    log.info("Job done!")
    