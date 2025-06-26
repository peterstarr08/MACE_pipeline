from pathlib import Path
from numpy import linspace

from ase.io import read, write

from mace_aze.config import (
    uniform_key
)
from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def uniform_split(file_path: Path, count: int, out_dir: Path):
    db = read(file_path, ':')
    
    log.info("Read %d configs", len(db))

    if count > len(db):
        log.critical("Cannot extract %d configs from %d configs", count, len(db))
        return

    if 2*count > len(db):
        log.critical("Conifigs don't have enough length to generate two %d size configs", count)
        return
    
    indx = linspace(0, len(db), count * 2, dtype=int, endpoint=False)
    db_1 = [db[i] for i in indx if i % 2]
    db_2 = [db[i] for i in indx if i % 2 == 0]

    file_name = file_path.name

    if out_dir.is_file():
        out_dir = out_dir.parent
    
    out_dir.mkdir(parents=True, exist_ok=True)
    db1_path = out_dir/f"{file_name}_extract_1.xyz"
    db2_path = out_dir/f"{file_name}_extract_2.xyz"
     
    log.info("Writing to %s", str(db1_path))
    write(db1_path, db_1, format='extxyz')

    log.info("Writing to %s", str(db2_path))
    write(db2_path, db_2, format='extxyz')

    log.info("Done !!!")



def splitter(file_path: str, method: str, count: int, out_dir: str):
    file_path = Path(file_path).resolve(strict=True)    # Ensures file exists
    out_dir = Path(out_dir)

    log.info("Method: %s    Count: %d", method, count)

    if method==uniform_key:
        uniform_split(file_path=file_path, count=count, out_dir=out_dir)
    else:
        log.info("If you see this then something went wrong in parsing")
    
    log.info("Done !!!")