from pathlib import Path

from mace_aze.log.conf import get_logger
from ase.io import read

log = get_logger(__name__)

def read_trajectory(path: str):
    log.info("Reading trajectory at %s", path)
    db = read(path, ':')
    log.info("Read %d configs from  %s", len(db), path)
    return db

def find_md_log(path: str):
    path = Path(path)
    mace_md_path = path.parent / "mace_md.log"
    log.info("Looking for %s", str(mace_md_path))
    if not mace_md_path.exists():
        log.info("Didn't find :(")
        return None
    
    log.info("Found! :)")
    return mace_md_path