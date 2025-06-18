#=================pipeline.yml configurations===================
pipeline = "pipeline"
generation = "gen"
models_path = "models_path"
md_path = "md_path"
new_ds = "new_dataset_path"

meta = "metadata"
calc = "calculator"
sampler="sampler"


available_calc = ['xtb']
available_sampler = ['nikhil', 'full']

md_run_openmm_cli = [
     "micromamba", "run", "-n", "mace-opnemm", "md-run"
]