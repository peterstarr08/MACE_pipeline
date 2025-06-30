from pathlib import Path

from ase.io import read, write

from mace_aze.log.conf import get_logger
from mace_aze.sampler import FPS

log = get_logger(__name__)

def fps_select(
        configs_path: str,
        atoms: list[str],
        count: int,
        out_path: str = None
):
    configs_path = Path(configs_path).resolve(strict=True)

    if out_path is not None:
        out_path = Path(out_path)
    else:
        out_path = configs_path.with_name(configs_path.stem + f"__FPS_{count}.xyz")
    
    log.debug("Generatinf save file name: %s", str(out_path))

    db = read(configs_path, ':')
    log.info("Read %d configs", len(db))

    log.info("Initizaliing FPS")
    fps = FPS(atoms=atoms)

    selec_confs = fps.select(db, count)
    log.info("Selected %d configs", len(selec_confs))

    log.info("Saving to %s", str(out_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write(out_path, selec_confs)
