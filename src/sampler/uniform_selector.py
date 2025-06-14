from .base import Selector
import numpy as np

class UniformSelector(Selector):
    def __init__(self, offset: int = 0):
        super().__init__()
        self.offset = offset

    def select(self, configs, nframe):
        if len(configs)<nframe:
            raise ValueError(f'Not enough {nframe} frame(s) in Atoms[{len(configs)}] ')
        
        indices = np.linspace(self.offset, len(configs), nframe, dtype=int)
        return [configs[i].copy() for i in indices]