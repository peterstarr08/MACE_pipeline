import os
import matplotlib.pyplot as plt
import numpy as np
from mace_aze.log.conf import get_logger
from mace_aze.calculators.mace import (
    mace_energy_key,
    mace_energy_variance_key,
    mace_avg_energy_key,
    mace_max_force_variance,
    mace_max_force_std
)
from mace_aze.utils.io import read_trajectory

log = get_logger(__name__)


def plot_models(
        traj_path: str,
        save_interval: int,
        output_dir: str
):
    log.info("Starting plot_models with traj: %s", traj_path)
    traj = read_trajectory(traj_path)
    traj = [at for at in traj if len(at) > 0]
    log.info("Trajectory loaded: %d frames after removing empty configs", len(traj))

    # Detect model energy keys like 'key_0', 'key_1', ...
    sample_info = traj[0].info
    model_keys = []
    i = 0
    while f"{mace_energy_key}_{i}" in sample_info:
        model_keys.append(f"{mace_energy_key}_{i}")
        i += 1
    log.info("Detected %d model energy keys", len(model_keys))

    def extract_from_key(key):
        return np.array([at.info[key] for at in traj if key in at.info])

    comm_energies = np.array([
        [at.info[key] for key in model_keys]
        for at in traj
    ])
    energy_var = extract_from_key(mace_energy_variance_key)
    energy_avg = extract_from_key(mace_avg_energy_key)
    avg_energy_per_atom = energy_avg / np.array([len(atoms) for atoms in traj])
    force_var_max = extract_from_key(mace_max_force_variance)
    force_std_max = extract_from_key(mace_max_force_std)
    temp_data = extract_from_key("temperature_K")

    n_frames = len(traj)
    time_fs = np.arange(n_frames) * save_interval
    plot_counts = 6 + int(len(temp_data) > 0)

    fig, ax = plt.subplots(plot_counts, 1, figsize=(10, 2.5 * plot_counts), sharex=True)
    if plot_counts == 1:
        ax = [ax]

    i = 0

    if len(temp_data) > 0:
        log.debug("Plotting temperature")
        ax[i].plot(time_fs, temp_data, color='r')
        ax[i].set_ylabel("T (K)")
        i += 1

    log.debug("Plotting individual model energies")
    for j in range(comm_energies.shape[1]):
        ax[i].plot(time_fs, comm_energies[:, j], label=f'Model {j + 1}')
    ax[i].set_ylabel("E (eV)")
    ax[i].legend()
    i += 1

    log.debug("Plotting average energy")
    ax[i].plot(time_fs, energy_avg, color='blue')
    ax[i].set_ylabel("Avg E (eV)")
    i += 1

    log.debug("Plotting average energy per atom")
    ax[i].plot(time_fs, avg_energy_per_atom, color='cyan')
    ax[i].set_ylabel("Avg E/atom (eV)")
    i += 1

    log.debug("Plotting energy variance")
    ax[i].plot(time_fs, energy_var, color='orange')
    ax[i].set_ylabel("Energy Variance (eV)^2")
    i += 1

    log.debug("Plotting max force variance")
    ax[i].plot(time_fs, force_var_max, color='green')
    ax[i].set_ylabel("Force Var (max) (eV/A)^2")
    i += 1

    log.debug("Plotting max force std")
    ax[i].plot(time_fs, force_std_max, color='purple')
    ax[i].set_ylabel("Force Std (max) (ev/A)")
    ax[i].set_xlabel("Time (fs)")

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, 'mace_model_diagnostics.png')
    fig.savefig(fig_path, dpi=300)
    log.info("Plot saved to %s", fig_path)
    plt.close(fig)
