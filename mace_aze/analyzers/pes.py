from pathlib import Path

from ase.io import read
import matplotlib.pyplot as plt
import numpy as np

from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def plot(db: list, energy_key: str, out_path: Path):
    energies = []
    indices = []

    for i, frame in enumerate(db):
        if 'config_type' in frame.info and frame.info['config_type'] == 'IsolatedAtom':
            log.debug("Frame at index %d is Isolated Atom. Skipping", i)
            continue
        energy = frame.info.get(energy_key)
        if energy is None:
            log.warning("Energy key '%s' not found in frame %d, skipping.", energy_key, i)
            continue
        energies.append(energy)
        indices.append(i)

    log.debug("Indices: %d  Energies: %d", len(indices), len(energies))

    if not energies:
        log.error("No valid energies found with key '%s'.", energy_key)
        return

        energies = np.array(energies)
    mean_energy = np.mean(energies)
    abs_error = np.abs(energies - mean_energy)

    global_variance = np.var(energies)
    rolling_variance = np.convolve((energies - mean_energy) ** 2, np.ones(5)/5, mode='same')

    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(indices, energies, linewidth=1.0)
    axs[0].set_ylabel(f"Energy ({energy_key}) (eV)")
    axs[0].set_title("Potential Energy Surface")
    axs[0].grid(True)

    axs[1].plot(indices, abs_error, color='orange', linewidth=1.0)
    axs[1].set_ylabel("Abs(Error from Mean)")
    axs[1].set_title("Energy Deviation")
    axs[1].grid(True)

    axs[2].plot(indices, rolling_variance, color='green', linewidth=1.0, label='Rolling Variance (window=5)')
    axs[2].axhline(global_variance, color='red', linestyle='--', label=f'Global Variance = {global_variance:.3e}')
    axs[2].set_ylabel("Variance")
    axs[2].set_title("Energy Variance")
    axs[2].set_xlabel("Configuration Index")
    axs[2].grid(True)
    axs[2].legend()

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
