from pathlib import Path

from ase import Atoms
from ase.io import write
from ase.units import Hartree, Bohr
from cclib.io import ccread

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def validate(log_path: Path):
    if not log_path.is_dir():
        log.critical("Directory %s doesn't exist", log_path)
        raise RuntimeError("Invalid Path")

def convert_to_atoms(log_frame: Path):
    log.debug("Reading %s", str(log_frame))
    data = ccread(log_frame)

    if data is None:
        log.critical("Empty file or prase error for %s", str(log_frame))
        raise RuntimeError("Expected valid gaussian output file. File seems like is corrupt")
    
    pos =  data.atomcoords[-1]       # (N_atoms, 3) atomcoords originally is a size 1 array
    num = data.atomnos               # (N_atoms,)
    energy_ev = data.scfenergies[-1] # Already converts to eV
    
    log.debug("Total atoms %d", len(num))
    log.debug("Force: %s eV", str(energy_ev))

    if hasattr(data, "grads") and data.grads.size > 0:
        forces_ev_A = data.grads[-1] * (Hartree/Bohr) # Converts to eV / A
    else:
        raise RuntimeError("Expected force data but didn't found any")
    
    atoms = Atoms(numbers=num, positions=pos)
    atoms.arrays['forces_gauss'] = forces_ev_A
    atoms.info['energy_gauss'] = energy_ev

    return atoms

def log_to_xyz(log_dir: str, xyz_file: str):
    log_path = Path(log_dir).resolve()
    xyz_path = Path(xyz_file)

    validate(log_path)

    log.info("Given search directory: %s", str(log_path))

    db = []
    log_files = sorted(log_path.glob("*.log"))

    for log_file in log_files:
        db.append(convert_to_atoms(log_file))

    log.info("Found %d files ending with .log", len(log_files))
    log.info("Successfully converted %d configs", len(db))

    if xyz_path.exists():
        log.warning("A file already exists at %s. Overwriting it", str(xyz_path))

    log.info("Writing to %s", xyz_file)

    xyz_path.parent.mkdir(parents=True, exist_ok=True)
    write(xyz_path, db, format='extxyz')

    log.info("Done !!!")



