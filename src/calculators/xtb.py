from .base import Calculator
from xtb.ase.calculator import XTB

DEFAULT_XTB_METHOD = "GFN2-xTB"

xtb_energy_key = "energy_xtb"
xtb_forces_key = "forces_xtb"


class XTBCalculator(Calculator):
    def __init__(self, method:str = DEFAULT_XTB_METHOD):
        super().__init__()
        self.xtb = XTB(method)
    
    @staticmethod
    def remove_calc(configs):
        for at in configs:
            at.calc = None

    def calculate(self, configs):
        for at in configs:
            at.pbc = False
            at.calc = self.xtb
            at.info[xtb_energy_key] = at.get_potential_energy()
            at.arrays[xtb_forces_key] = at.get_forces()
        XTBCalculator.remove_calc(configs)
        