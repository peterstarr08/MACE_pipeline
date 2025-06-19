from .base import Selector
import numpy as np
from mace_aze.config import us_0_selected, us_off_selected
from mace_aze.utils.generators import generate_space_offset
from mace_aze.log.conf import get_logger

log = get_logger(__name__)

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
        if len(indices)>0:
            log.debug("Indices - First element:%d   Last element:%d     Size:%d", indices[0], indices[-1], len(indices))
        else:
            log.critical("No indices was generated. Throwing error")
            raise RuntimeError("No indices were generated")
        
        if len(offset_indices)>0:
            log.debug("Offset Indices - First element:%d   Last element:%d     Size:%d", offset_indices[0], offset_indices[-1], len(offset_indices))
        else:
            log.warning("No offset indices were generated. No test set will be generated")

        UniformSelector.clear_initial_selection(configs=configs)

        for i, at in enumerate(configs):
            if i in indices:
                at.info[us_0_selected] = True
            if i in offset_indices:
                at.info[us_off_selected] = True
        