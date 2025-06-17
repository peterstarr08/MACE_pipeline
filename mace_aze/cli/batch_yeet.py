import os
import argparse
from pathlib import Path
from utils.records import RawDataset
from ase.io import read, write

def arg_parse():
    parser = argparse.ArgumentParser(description="Export MD frames to single file")
    parser.add_argument('--dir', type=str, required=True, help="Give the directory of MD frames to yeet in database") 
    parser.add_argument('--label', type=str, required=True, help="Give a unique label. Must not be same as before used")
    parser.add_argument('--ext', type=str, choices=['xyz'], default='xyz', help="Extension for output config. Default .xyz")
    return parser.parse_args()


def validate_arguments(dir_name: str, label: str):
    if not os.path.isdir(dir_name):
        raise ValueError(f"{dir_name} does not exist")

def collect_frames(dir_path: Path):
    files = [f for f in dir_path.glob('*') if f.is_file()]
    db = []
    for frame in files:
        db.extend(read(frame, ':'))
    return db

def export_config(db, label: str, ext: str):
    rd = RawDataset(label, ext)
    os.makedirs(os.path.dirname(rd.full_path()))
    write(str(rd.full_path()), db)

def main():
    args = arg_parse()
    validate_arguments(args.dir, args.label)
    db = collect_frames(Path(args.dir))
    export_config(db, args.label, args.ext)


print("Starting Batch yeeeeet", __name__)
if __name__=="__main__":
    main()