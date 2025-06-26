import os

from ase.io import read

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def xyz_to_com(xyz_file: str, output_dir: str, method: str, basis: str, charge=0, mult=1):
    log.info("Converting xyz to gaussian input files")
    log.debug("Method: %s   Basis: %s", method, basis)
    log.debug("Charge: %s   Multiplicity: %s", str(charge), str(mult))
    
    log.info("Creating directory %s", output_dir)
    os.makedirs(output_dir, exist_ok=True)

    log.info("Reading %s", xyz_file)
    frames = read(xyz_file, index=':', format='extxyz')
    log.debug("Read %d frames", len(frames))

    for i, atoms in enumerate(frames):
        log.debug("Generating frame_%d.com", i)
        com_path = os.path.join(output_dir, f'frame_{i}.com')
        with open(com_path, 'w') as f:
            f.write(f"%chk=frame_{i}.chk\n")
            f.write(f"# {method}/{basis} Force\n\n")
            f.write(f"Frame {i} SPE + Forces\n\n")
            f.write(f"{charge} {mult}\n")

            for atom in atoms:
                sym = atom.symbol
                x, y, z = atom.position
                f.write(f"{sym}  {x:.6f}  {y:.6f}  {z:.6f}\n")
            f.write("\n") # .com files requires a blank just after atoms position
    log.info("Done !!!")