import os

from ase.io import read

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def xyz_to_com(xyz_file: str, output_dir: str, method: str, basis: str, split: int = 1, charge=0, mult=1):
    log.info("Converting xyz to gaussian input files")
    log.debug("Method: %s   Basis: %s", method, basis)
    log.debug("Charge: %s   Multiplicity: %s", str(charge), str(mult))
    
    log.info("Creating directory %s", output_dir)
    os.makedirs(output_dir, exist_ok=True)

    log.info("Reading %s", xyz_file)
    frames = read(xyz_file, index=':', format='extxyz')
    n_frames = len(frames)
    log.debug("Read %d frames", n_frames)

    # compute chunk size
    chunk_size = (n_frames + split - 1) // split  # ceiling division

    for i in range(split):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n_frames)
        subfolder = os.path.join(output_dir, f"com_{start}_{end - 1}")

        log.info("Creating folder %s", str(subfolder))
        os.makedirs(subfolder, exist_ok=True)

        for j in range(start, end):
            atoms = frames[j]
            com_path = os.path.join(subfolder, f'frame_{j}.com')
            log.debug("Generating %s", com_path)
            with open(com_path, 'w') as f:
                f.write(f"%chk=frame_{j}.chk\n")
                f.write(f"# {method}/{basis} Force\n\n")
                f.write(f"Frame {j} SPE + Forces\n\n")
                f.write(f"{charge} {mult}\n")

                for atom in atoms:
                    sym = atom.symbol
                    x, y, z = atom.position
                    f.write(f"{sym}  {x:.6f}  {y:.6f}  {z:.6f}\n")
                f.write("\n")
        log.info("Written from %d to %d", start, end)
    
    log.info("Done !!!")