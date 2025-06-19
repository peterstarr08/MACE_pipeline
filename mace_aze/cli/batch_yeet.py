import os
import argparse
from pathlib import Path
from mace_aze.utils.records import RawDataset
from mace_aze.log.conf import get_logger
from ase.io import read, write

log = get_logger(__name__)

def arg_parse():
    parser = argparse.ArgumentParser(description="Export MD frames to single file")
    parser.add_argument('--dir', type=str, required=True, help="Give the directory of MD frames to yeet in database") 
    parser.add_argument('--label', type=str, required=True, help="Give a unique label. Must not be same as before used")
    parser.add_argument('--ext', type=str, choices=['xyz'], default='xyz', help="Extension for output config. Default .xyz")
    return parser.parse_args()


def validate_arguments(dir_name: str, label: str):
    log.info("Looking for directory %s", dir_name)
    if not os.path.isdir(dir_name):
        raise ValueError(f"{dir_name} does not exist")
    log.info("Directory %s was found. Looks ugly. Let me organize it", dir_name)

def collect_frames(dir_path: Path):
    log.info("Globing files. Glob glob!")
    files = [f for f in dir_path.glob('*') if f.is_file()]
    db = []
    for frame in files:
        log.info("Reading %s", frame.name)
        db.extend(read(frame, ':'))
    return db

def export_config(db, label: str, ext: str):
    rd = RawDataset(label, ext)
    os.makedirs(os.path.dirname(rd.full_path()))
    log.info("Saving the file to %s", str(os.path.dirname(rd.full_path())))
    write(str(rd.full_path()), db)

def main():
    args = arg_parse()
    validate_arguments(args.dir, args.label)
    log.info("Starting Batch Yeeeeterr")
    db = collect_frames(Path(args.dir))
    export_config(db, args.label, args.ext)
    log.info("Successfully yeeted!")


if __name__=="__main__":
    main()