from .base import Selector
import numpy as np
from mace_aze.config import us_0_selected, us_off_selected
from mace_aze.utils.generators import generate_space_offset

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
        
        indices, offset_indices = generate_space_offset(nframe, len(configs), self.offset)

        UniformSelector.clear_initial_selection(configs=configs)

        for i, at in enumerate(configs):
            if i in indices:
                at.info[us_0_selected] = True
            if i in offset_indices:
                at.info[us_off_selected] = True
        