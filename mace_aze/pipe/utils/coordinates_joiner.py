from pathlib import Path

from ase.io import read, write

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def dir_join(dir_path: Path):
    log.info("Globbing all files from %s", str(dir_path))
    
    files = sorted([f for f in dir_path.glob('*') if f.is_file()])
    db = []

    for frame in files:
        db = db + read(frame, ':', format='extxyz')

    log.info("Files found total: %d", len(files))
    log.info("Configs converted: %d", len(db))

    return db

def file_join(paths: list[Path]):
    db = []
    for p in paths:
        if p.exists():
            db = db + read(p, ':', format='extxyz')
    log.info("Configs converted: %d", len(db))

    return db

def join(paths: list[str], out: str):
    if len(paths)==1:
        log.info("Looks like you gave a directory. Checking") 

        if paths[0].is_dir():
            log.info("Yupp, it's a directory. Processing to combine all frames inside this folder into single file")
            db = dir_join(Path(paths))
        else:
            log.info("I can't do anything with just one file. Exiting")
            return
        
    else:
        log.info("Processing to combine %s into single file", str(paths))
        db = file_join([Path(path) for path in paths])
    
    out_path = Path(out)
    if out_path.exists():
        log.warning("Files exists at %s, overwtiting it", out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write(out_path, db)
    log.info("Done !!!")