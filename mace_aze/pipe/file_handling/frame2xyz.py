from pathlib import Path

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

def frame2xyz(frames_dir: str, out: str):
    frames_path = Path(frames_dir).resolve(strict=True)
    out_path = Path(out)

    log.info("Checking directory %s", str(frames_path))

    files = sorted(frames_path.glob("*"))                    # Globs every shit
    log.info("Found %d files", len(files))

    db = read_frames(files)
    log.info("Read %d configs", len(db))

    log.info("Writing to %s", str(out_path))
    if out_path.exists():
        log.warning("A file already exist at given out path. Overwriting it")
    out_path.mkdir(parents=True, exist_ok=True)
    write(out_path, db)
    log.info("Done !!!")

