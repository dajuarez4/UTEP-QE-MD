########################################################## QE input writer #####################################################################################

def write_qe_md_input(
    filename,
    atomic_positions,
    cell_parameters,
    kpoints=(1, 1, 1, 0, 0, 0),
    atomic_species=None,
    temperature = 100
):

    if atomic_species is None:
        atomic_species = [
            ('Ni', 58.6934, 'Ni.pbe-spn-kjpaw_psl.1.0.0.UPF'),
            ('Ti', 47.867,  'Ti.pbe-spn-kjpaw_psl.1.0.0.UPF'),
        ]

    kx, ky, kz, sx, sy, sz = kpoints

    lines = []

    # ------------------------- CONTROL -------------------------
    lines.append("&CONTROL")
    lines.append(f"  calculation   = '{calculationd}',")
    lines.append(f"  restart_mode  = '{restart_mode}',")
    lines.append(f"  prefix        = '{prefix}',")
    lines.append(f"  pseudo_dir    = '{pseudo_dir}',")
    lines.append(f"  outdir        = '{outdir}',")
    lines.append(f"  dt            = {dt},")
    lines.append(f"  tstress       = {tstress},")
    lines.append(f"  tprnfor       = {tprnfor},")
    lines.append(f"  nstep         = {nstep},")
    lines.append(f"  max_seconds   = {max_seconds},")
    lines.append("/\n")

    # ------------------------- SYSTEM --------------------------
    lines.append("&SYSTEM")
    lines.append(f"  ibrav        = {ibrav},")
    lines.append(f"  nat          = {len(atomic_positions)},")
    lines.append(f"  ntyp         = {ntyp},")
    lines.append(f"  ecutwfc      = {ecutwfc},")
    lines.append(f"  ecutrho      = {ecutrho},")
    lines.append(f"  occupations  = '{occupations}',")
    lines.append(f"  smearing     = '{smearing}',")
    lines.append(f"  degauss      = {degauss},")
    lines.append(f"  nosym        = {nosym},")
    # optional:
    # lines.append("  nspin        = 2,")
    # lines.append("  starting_magnetization(1) = 0.5,")
    lines.append("/\n")

    # ------------------------ ELECTRONS ------------------------
    lines.append("&ELECTRONS")
    lines.append(f"  conv_thr     = {conv_thr},")
    # lines.append("  electron_maxstep = 1000,")
    lines.append(f"  mixing_beta  = {mixing_beta},")
    lines.append("/\n")

    # -------------------------- IONS ---------------------------
    lines.append("&IONS")
    lines.append(f"  pot_extrapolation = '{pot_extrapolation}',")
    lines.append(f"  wfc_extrapolation = '{wfc_extrapolation}',")
    lines.append(f"  ion_temperature   = '{ion_temperature}',")
    # lines.append("  ion_dynamics    = 'bfgs',")
    lines.append(f"  tempw           = {temperature},")
    lines.append(f"  nraise          = {nraise},")
    lines.append("/\n")

    # -------------------- ATOMIC SPECIES ----------------------
    lines.append("ATOMIC_SPECIES")
    for sym, mass, pp in atomic_species:
        lines.append(f"  {sym}  {mass:.4f}  {pp}")
    lines.append("")

    # ------------------- CELL PARAMETERS ----------------------
    lines.append("CELL_PARAMETERS (angstrom)")
    for row in cell_parameters:
        lines.append("  " + "  ".join(f"{v: .10f}" for v in row))
    lines.append("")

    # ------------------- ATOMIC POSITIONS ---------------------
    lines.append("ATOMIC_POSITIONS (angstrom)")
    for sym, x, y, z in atomic_positions:
        lines.append(f"  {sym}  {x: .10f}  {y: .10f}  {z: .10f}")
    lines.append("")

    # ------------------------ K-POINTS ------------------------
    lines.append("K_POINTS automatic")
    lines.append(f"  {kx}  {ky}  {kz}  {sx}  {sy}  {sz}")
    lines.append("")

    # ----------------------- WRITE FILE -----------------------
    text = "\n".join(lines)
    with open(filename, "w") as f:
        f.write(text)

    return 'Input File created'#text  

##################################################################### SBATCH writer ############################################################################

def write_sbatch_file(path, namefile,time_sim,QOS,cpu_or_gpu):
    sbatch_text = f"""#!/bin/bash
#SBATCH -A m3845
#SBATCH -C {cpu_or_gpu}
#SBATCH -q {QOS}
#SBATCH -t {time_sim}
#SBATCH -N 1
#SBATCH -G 4
#SBATCH -J {namefile}
#SBATCH -o {namefile}.out
#SBATCH -e {namefile}.err

module reset
module load gpu PrgEnv-nvidia cray-hdf5-parallel cray-fftw

QE_BIN=/global/cfs/projectdirs/m3845/Diego_projects/QE/UTEP-QE-MD/Executable

srun -n 32 --gpus-per-node=4 $QE_BIN/pw.x -in {namefile}.in > {namefile}.log
"""

    with open(path, "w") as f:
        f.write(sbatch_text)
