from numpy import linspace
from pathlib import Path
import re

from ase.io import read, write

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def read_frames(paths: list[Path]):
    db = []
    for path in paths:
        log.debug("Reading %s", str(path.name))
        try:                                                # Skipping files which are not valid coordinates
            db+=read(path, ':')
        except:
            log.warning("Failed to read %s", str(path.name))
            continue
    return db

def frame2xyz(frames_dir: str, out: str, count: int = -1):
    frames_path = Path(frames_dir).resolve(strict=True)
    out_path = Path(out)

    log.info("Checking directory %s", str(frames_path))

    files = sorted(frames_path.glob("*"), key=lambda f: int(re.search(r'\d+', f.name).group()))                    # Globs every shit
    log.info("Found %d files", len(files))

    if count>0 and len(files)>=count:
        log.info("Generatinf indices to select %d frames", count)
        indx = linspace(0, len(files), count, dtype=int, endpoint=False)
        files = [path for i, path in enumerate(files) if i in indx]
        log.debug("Final files count %d", len(files))


    db = read_frames(files)
    log.info("Read %d configs", len(db))

    # if count>0:
    #     log.info("Selecting %d frames", count)
    #     indx = linspace(0, len(db), count, dtype=int, endpoint=False)
    #     db = [db[i] for i in indx]
    #     log.debug("Final configs size %d", len(db))

    log.info("Writing to %s", str(out_path))
    if out_path.exists():
        log.warning("A file already exist at given out path. Overwriting it")
    out_path.mkdir(parents=True, exist_ok=True)
    write(out_path, db)
    log.info("Done !!!")

