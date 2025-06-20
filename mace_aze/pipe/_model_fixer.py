import os
import torch
from mace.modules.models import ScaleShiftMACE
from torch.serialization import add_safe_globals
from torch.nn import Parameter

from mace_aze.log.conf import get_logger
log = get_logger(__name__)

# Trust MACE class
add_safe_globals([ScaleShiftMACE])


def fix_atomic_energies_shape(model_path: str):
    log.debug("Loading model at %s", model_path)
    model = torch.load(model_path, map_location="cpu", weights_only=False)

    # Fix shape by replacing the Parameter
    with torch.no_grad():
        log.info("Fixing shape of model")
        old_param = model.atomic_energies_fn.atomic_energies
        log.debug("Original shape: %s", str(old_param.shape))

        # Flatten and replace the Parameter entirely
        new_param = Parameter(old_param.view(-1).clone(), requires_grad=old_param.requires_grad)
        model.atomic_energies_fn.atomic_energies = new_param

        log.debug("Fixed shape: %s", str(model.atomic_energies_fn.atomic_energies.shape))

    # Save fixed model
    base, ext = os.path.splitext(model_path)
    fixed_path = f"{base}_fixed{ext}"
    torch.save(model, fixed_path)
    log.debug("Saved fixed model to: %s", fixed_path)