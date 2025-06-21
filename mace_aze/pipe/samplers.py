from mace_aze.log.conf  import get_logger

log = get_logger(__name__)

def thershold_sample(configs: list, threshold: float, key: str):
    log.info("Doing threshold sampling on %d configss", len(configs))
    sample_selected = [at for at in configs if at.info[key]>threshold]
    log.info("Samples selected %d", len(sample_selected))
    return sample_selected

def top_disagreement_sample(configs: list, count: int, key: str):
    log.info("Sampling top %d disagreemetns from %d configss", count, len(configs))
    log.debug("Sorting")
    sorted_config = sorted(configs, key=lambda at: at.info[key], reverse=True)
    if len(configs)<count:
        log.warning("Samples not enough returnig origianl configs")
        return configs
    return sorted_config[:count]