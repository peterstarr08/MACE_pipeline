from dscribe.descriptors import SOAP
from sklearn.metrics import pairwise_distances
from ase.data import atomic_numbers
import numpy as np

from .base import Selector

class FPS(Selector):
    def __init__(self, atoms,  r_cut = 5.0, n_max = 8.0, l_max = 6.0):
        super().__init__()
        self.atoms = atoms
        self.r_cut = r_cut
        self.n_max = n_max
        self.l_max = l_max
    
    def select(self, configs, nframe):
        if len(configs)<nframe:
            raise ValueError(f'Not enough {nframe} frame(s) in Atoms[{len(configs)}] ')
        
        soap = SOAP(species=[atomic_numbers[a] for a in self.atoms],
                    r_cut=self.r_cut,
                    n_max=self.n_max,
                    l_max=self.l_max
        )
        descriptor_list = [soap.create(s) for s in configs]
        X = np.array([desc.mean(axis=0) for desc in descriptor_list])
        selected = [0]

        for _ in range(nframe):
            dists = pairwise_distances(X[selected], X)
            min_dist = dists.min(axis=0)
            next_idx = np.argmax(min_dist)
            selected.append(next_idx)
        
        selected_structures = [configs[i] for i in selected]

        return selected_structures