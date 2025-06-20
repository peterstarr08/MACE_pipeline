from .conf import (
    pipeline,

    generation,

    models_path,
    md_path,
    new_ds,

    meta,
    calc,
    sampler
)
from mace_aze.log.conf import get_logger
log = get_logger(__name__)


def validate_backward_dependencies(order, dependencies):
    for key in order:
        depend = dependencies.get(key, [])
        for d in depend:
            if d not in order:
                log.critical("%s requires %s", key, d)
                raise SyntaxError("Invalid syntax")

    
# To add meta data checking
def validate_yml(cfg: dict):
    log.info("Validating the pipeline flow")

    try:
        gens = len(cfg[pipeline])
    except KeyError:
        log.critical("%s key not provided", pipeline)
        raise SyntaxError("Bad YAML!")

    if gens <= 0:
        log.critical("No generations found. No pipeline found.")
        raise SystemError("Invalid pipeline syntax")
    
    log.info("Found %d generations", gens)

    for i, g in enumerate(cfg[pipeline]):
        log.info("Validating %s%d", generation, i)

        gen_keys = list(g[f'{generation}{i}'].keys())

        dependencies= {
            new_ds: [md_path],
            md_path: [models_path],
            models_path: []
        }

        validate_backward_dependencies(gen_keys, dependencies=dependencies)
    
    #Cheking metadata now
    if meta not in cfg:
        log.critical("No %s provided in pipeline", meta)
        raise SyntaxError("Invalid pipeline syntax")
    
    for meta_key in [calc, sampler]:
        if meta_key not in cfg[meta]:
            log.critical("No %s was provided", meta_key)
            raise SyntaxError("Invalid pipeline syntax")
        


            
            
