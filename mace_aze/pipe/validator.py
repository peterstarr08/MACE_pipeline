from .conf import (
    pipeline,
    generation,
    models_path,
    md_path,
    new_ds
)
from mace_aze.config import ROOT, pipeline_path
from mace_aze.log.conf import get_logger
log = get_logger(__name__)


def check_exists(path: str):
    log.info("Looking for %s", str(pipeline_path/path))
    if (pipeline_path/path).exists():
        log.info("File found!")
        return
    
    log.debug("No files at %s", str(pipeline_path/path))
    log.debug("Looking for %s", str(ROOT/path))
    
    if (ROOT/path).exists():
        log.info("File found!")
        return
    else:
        log.critical("No file found at %s or %s. Throwing FileNotFoundError", str(pipeline_path/path), str(ROOT/path))
        raise FileNotFoundError(f'{pipeline_path/path} or {ROOT/path} doesn\'t exist')
         
# To add meta data checking
def validate_yml(cfg: dict):
    log.info("Validating the pipeline flow")

    try:
        gens = len(cfg[pipeline])
    except KeyError:
        log.critical("%s key not provided", pipeline)
        raise SyntaxError("Bad YAML!")

    if gens <= 0:
        log.critical("No generations found. Use correct labelling")
    log.info("Found %d generations", gens)

    for i, g in enumerate(cfg[pipeline]):
        log.info("Validing %s%d", generation, i)
        for key in [models_path, md_path, new_ds]:
            if key not in g[f'{generation}{i}']:
                log.critical("%s not provided in gen%d", key, i)
                raise SyntaxError("Bad YAML!")
            if len(g[f'{generation}{i}'])<=0:
                log.critical("No paths provided in %s for gen%d", key, i)
                raise ValueError("Incomplete YAML!")
            for path in g[f'{generation}{i}']:
                check_exists(path)

            
            
