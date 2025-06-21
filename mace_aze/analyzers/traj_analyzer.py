import os
import matplotlib.pyplot as plt
import numpy as np
from mace_aze.log.conf import get_logger
from mace_aze.calculators import MACEculator
from mace_aze.calculators.mace import (
    mace_energy_key,
    mace_energy_variance_key,
    mace_avg_energy_key,
    mace_max_force_variance,
    mace_max_force_std
)
from mace_aze.utils.io import read_trajectory
from mace_aze.utils.mace_md_log_paraser import get_temp

log = get_logger(__name__)


# Returns array of shape (n_frames, n_models)
def get_comm_energy(traj):
    valid_traj = [at for at in traj if f'{mace_energy_key}_0' in at.info]
    n_models = len([k for k in valid_traj[0].info.keys() if mace_energy_key in k])
    energies = np.array([
        [at.info[f'{mace_energy_key}_{i}'] for i in range(n_models)]
        for at in valid_traj
    ])
    return energies


# Returns (n_frames,)
def get_energy_var(traj):
    return np.array([
        at.info[mace_energy_variance_key]
        for at in traj if mace_energy_variance_key in at.info
    ])


def get_avg_energy(traj):
    return np.array([
        at.info[mace_avg_energy_key]
        for at in traj if mace_avg_energy_key in at.info
    ])


def get_max_force_var(traj):
    return np.array([
        at.info[mace_max_force_variance]
        for at in traj if mace_max_force_variance in at.info
    ])


def get_force_std(traj):
    return np.array([
        at.info[mace_max_force_std]
        for at in traj if mace_max_force_std in at.info
    ])


def plot_models(
        traj_path: str,
        model_paths: list[str],
        time_unit: int,
        output_dir: str
):
    log.info("Starting plot_models with traj: %s", traj_path)
    traj = read_trajectory(traj_path)
    traj = [at for at in traj if len(at) > 0]
    log.info("Trajectory loaded: %d frames after removing empty configs", len(traj))

    calc = MACEculator(model_paths=model_paths)
    calc.calculate(traj)

    # Filter again to ensure energy keys exist
    traj = [at for at in traj if f'{mace_energy_key}_0' in at.info]
    log.info("Trajectory filtered: %d frames with valid energy info", len(traj))

    temp_data = get_temp(traj_path)
    comm_energies = get_comm_energy(traj)
    energy_var = get_energy_var(traj)
    energy_avg = get_avg_energy(traj)
    force_var_max = get_max_force_var(traj)
    force_std_max = get_force_std(traj)

    n_frames = len(traj)
    time_fs = np.arange(n_frames) * time_unit
    plot_counts = 5 + int(len(temp_data) > 0)

    fig, ax = plt.subplots(plot_counts, 1, figsize=(10, 2.5 * plot_counts), sharex=True)
    if plot_counts == 1:
        ax = [ax]

    i = 0

    if len(temp_data) > 0:
        log.debug("Plotting temperature")
        ax[i].plot(time_fs, temp_data, color='r')
        ax[i].set_ylabel("T (K)")
        ax[i].set_title("Temperature")
        i += 1

    log.debug("Plotting individual model energies")
    for j in range(comm_energies.shape[1]):
        ax[i].plot(time_fs, comm_energies[:, j], label=f'Model {j + 1}')
    ax[i].set_ylabel("E (eV)")
    ax[i].set_title("Individual Model Energies")
    ax[i].legend()
    i += 1

    log.debug("Plotting average energy")
    ax[i].plot(time_fs, energy_avg, color='blue')
    ax[i].set_ylabel("Avg E (eV)")
    ax[i].set_title("Committee Average Energy")
    i += 1

    log.debug("Plotting energy variance")
    ax[i].plot(time_fs, energy_var, color='orange')
    ax[i].set_ylabel("Energy Variance")
    ax[i].set_title("Committee Energy Variance")
    i += 1

    log.debug("Plotting max force variance")
    ax[i].plot(time_fs, force_var_max, color='green')
    ax[i].set_ylabel("Force Var (max)")
    ax[i].set_title("Max Force Variance")
    i += 1

    log.debug("Plotting max force std")
    ax[i].plot(time_fs, force_std_max, color='purple')
    ax[i].set_ylabel("Force Std (max)")
    ax[i].set_title("Max Force Std Dev")
    ax[i].set_xlabel("Time (fs)")

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, 'mace_model_diagnostics.png')
    fig.savefig(fig_path, dpi=300)
    log.info("Plot saved to %s", fig_path)
    plt.close(fig)
