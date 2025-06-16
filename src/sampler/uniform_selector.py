from .base import Selector
import numpy as np
from config import us_0_selected, us_off_selected

class UniformSelector(Selector):
    def __init__(self, offset: int = 0):
        super().__init__()
        self.offset = offset

    @staticmethod
    def clear_initial_selection(configs):
        for at in configs:
            for key in (us_0_selected, us_off_selected):
                at.info.pop(key, None)

    def select(self, configs, nframe):
        if len(configs)<nframe:
            raise ValueError(f'Not enough {nframe} frame(s) in Atoms[{len(configs)}] ')
        
        indices = np.linspace(0, len(configs), nframe, endpoint=False, dtype=int)
        offset_indices = np.linspace(self.offset, len(configs), nframe, endpoint=False, dtype=int)

        UniformSelector.clear_initial_selection(configs=configs)

        for i, at in enumerate(configs):
            if i in indices:
                at.info[us_0_selected] = True
            if i in offset_indices:
                at.info[us_off_selected] = True
        