from mace.calculators import MACECalculator
from .base import Calculator
import numpy as np
from mace_aze.log.conf import get_logger

log = get_logger(__name__)

mace_energy_key = 'energy_mace'
mace_energy_variance_key = 'variance'
mace_avg_energy_key = 'average_mace_energy'
mace_max_force_variance = 'max_force_variance'
mace_max_force_std = 'max_force_std'


class MACEculator(Calculator):
    def __init__(self, model_paths: list[str], device: str = 'cuda'):
        super().__init__()
        if len(model_paths) == 0:
            log.critical("No MACE calculators provided")
            raise RuntimeError("MACE calculator required. Pass model with .model extension")

        log.info("Models provided %s", str(model_paths))
        
        # Use separate calculator instances for each model
        self.calculators = [
            MACECalculator(model_paths=[path], device=device) for path in model_paths
        ]
        self.total_calc = len(self.calculators)

    @staticmethod
    def remove_calc(configs):
        for at in configs:
            at.calc = None

    @staticmethod
    def compute_force_variance(forces):
        """
        forces: (n_models, n_atoms, 3)
        Returns max variance across atoms
        """
        mean_forces = np.mean(forces, axis=0)                  # (n_atoms, 3)
        diffs = forces - mean_forces                           # (n_models, n_atoms, 3)
        squared_norms = np.sum(diffs**2, axis=2)               # (n_models, n_atoms)
        var_per_atom = np.mean(squared_norms, axis=0)          # (n_atoms,)
        return np.max(var_per_atom)

    def calculate(self, configs):
        log.info("Beginning MACE committee calculations")
        log.debug("Configs size: %d", len(configs))

        for at_idx, at in enumerate(configs):
            if len(at) == 0:
                log.warning("Skipping empty config at index %d", at_idx)
                continue

            energies = []
            forces = []

            for i, calc in enumerate(self.calculators):
                at.calc = calc
                energy = at.get_potential_energy()
                force = at.get_forces()

                log.debug("configs[%d] model[%d] forces (first 3 atoms): %s", at_idx, i, np.array2string(force[:3], precision=4))

                energies.append(energy)
                forces.append(force)
                at.info[f'{mace_energy_key}_{i}'] = energy

            energies = np.array(energies)  # (n_models,)
            forces = np.array(forces)      # (n_models, n_atoms, 3)

            at.info[mace_energy_variance_key] = np.std(energies)
            at.info[mace_avg_energy_key] = np.mean(energies)

            max_force_var = self.compute_force_variance(forces)
            at.info[mace_max_force_variance] = max_force_var
            at.info[mace_max_force_std] = np.sqrt(max_force_var)

            log.debug("configs[%d]  CommEnergies %s EnergyVariance %f  EnergyAvg %f    MaxFVar %f  MaxFStd %f",
                      at_idx, str(energies), at.info[mace_energy_variance_key], at.info[mace_avg_energy_key],
                      at.info[mace_max_force_variance], at.info[mace_max_force_std])

        log.info("Calculations completed. Removing calculator")
        MACEculator.remove_calc(configs)
        log.info("Calculators removed")
