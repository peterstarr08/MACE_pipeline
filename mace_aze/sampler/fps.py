from dscribe.descriptors import SOAP
from sklearn.metrics import pairwise_distances
from ase.data import atomic_numbers
import numpy as np

from mace_aze.log.conf import get_logger

from .base import Selector

log = get_logger(__name__)

class FPS(Selector):
    def __init__(self, atoms,  r_cut = 5.0, n_max = 8.0, l_max = 6.0):
        super().__init__()
        self.atoms = atoms
        self.r_cut = r_cut
        self.n_max = n_max
        self.l_max = l_max
        self.soap = SOAP(species=[atomic_numbers[a] for a in self.atoms],
                    r_cut=self.r_cut,
                    n_max=self.n_max,
                    l_max=self.l_max
                )
        log.debug("Instantiated FPS with Atoms: %s  r_cut: %f   n_max: %f   l_max: %f", str(atoms), r_cut, n_max, l_max)

    def select(self, configs, nframe):
        if len(configs)<nframe:
            raise ValueError(f'Not enough {nframe} frame(s) in Atoms[{len(configs)}] ')
        
        log.info("Starting FPS selection on %d configs", len(configs))

        descriptor_list = [self.soap.create(s) for s in configs]
        X = np.array([desc.mean(axis=0) for desc in descriptor_list])
        selected = [0]

        for i in range(nframe):
            log.debug("Selecting :%d ", i)
            dists = pairwise_distances(X[selected], X)
            min_dist = dists.min(axis=0)
            next_idx = np.argmax(min_dist)
            selected.append(next_idx)
        
        log.debug("Selected indice: %s", str(selected))
        selected_structures = [configs[i] for i in selected]

        return selected_structures