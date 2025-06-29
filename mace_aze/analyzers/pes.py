from pathlib import Path

from ase.io import read
import matplotlib.pyplot as plt

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def plot(db: list, energy_key: str, out_path: Path):
    energies = []
    indices = []

    for i, frame in enumerate(db):
        energy = frame.info[energy_key]
        if energy is None:
            log.warning("Energy key '%s' not found in frame %d, skipping.", energy_key, i)
            continue
        energies.append(energy)
        indices.append(i)
    
    log.debug("Indices: %d  Energies: %d", len(indices), len(energies))

    if not energies:
        log.error("No valid energies found with key '%s'.", energy_key)
        return

    plt.figure(figsize=(8, 5))
    plt.plot(indices, energies, marker='o')
    plt.xlabel("Configuration Index")
    plt.ylabel(f"Energy ({energy_key}) (eV)")
    plt.title("Potential Energy Surface")
    plt.grid(True)
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)

    plt.close()

    log.info("File written to %s", str(out_path))


def plot_pes(xyz_path: str, energy_key: str, out_path: str):
    xyz_path = Path(xyz_path).resolve(strict=True)
    out_path = Path(out_path)

    log.info("Reading %s", str(xyz_path))
    frames = read(xyz_path, ":", format="extxyz")

    log.debug("Read %d configs", len(frames))

    log.info("Plotting...")
    plot(frames, energy_key, out_path)

    log.info("Done !!!")
