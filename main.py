from utils.config import *
from utils.write_func import *
from utils.default_dict import *
from utils.generate_pos import *

for lattice_par in lattice_par_list:
    atomic_positions, cell_parameters = generate_niti_b2_positions(3, lattice_par)
    for temperature in temp_list:
        namefile = f'niti_md_latpar{lattice_par}_temp{temperature}'
        outdir = f"{experiment_path}/{namefile}/"
        os.system(f"mkdir -p {outdir}")
        infile = f"{outdir}/{namefile}.in"
        write_qe_md_input(infile,atomic_positions,cell_parameters,temperature=temperature)
        write_sbatch_file(outdir+'run.sbatch', namefile,time_sim='00:30:00',QOS='debug',cpu_or_gpu='gpu')
