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
        if len(model_paths)<=0:
            log.critical("No MACE calculators provided")
            raise RuntimeError("MACE calculator required. Pass model with .model extension")
        self.mace_calc = MACECalculator(model_paths=model_paths, device=device)
        self.total_calc = len(model_paths)
    @staticmethod
    def remove_calc(configs):
        for at in configs:
            at.calc = None

    @staticmethod
    def max_force_variance(at):
        '''Written by ChatGPT. Must check for validation. Formula based NIkhil Boi papers'''
        forces = at.get_forces()  # shape: (n_models, n_atoms, 3)
        mean_forces = np.mean(forces, axis=0)  # shape: (n_atoms, 3)
        diffs = forces - mean_forces  # shape: (n_models, n_atoms, 3)
        squared_norms = np.sum(diffs**2, axis=2)  # shape: (n_models, n_atoms)
        var_per_atom = np.mean(squared_norms, axis=0)  # shape: (n_atoms,)
        return np.max(var_per_atom)

    def calculate(self, configs):
        log.info("Beginning MACE committe calculations")
        for at in configs:
            at.calc = self.mace_calc
            engs = at.get_potential_energies()
            for i in range(self.total_calc):
                at.info[f'{mace_energy_key}_{i}'] = engs[i]
            at.info[mace_energy_variance_key] = np.std(engs)
            at.info[mace_avg_energy_key] = np.average(engs)
            at.info[mace_max_force_variance] = MACEculator.max_force_variance(at)
            at.info[mace_max_force_std] = np.sqrt(at.info[mace_max_force_variance])
        log.info("Calculations completed. Removing calculator")
        MACEculator.remove_calc(configs)
        log.info("Calculators removed")
        