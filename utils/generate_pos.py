def generate_niti_b2_positions(N, cell_length):
    basis_Ni = [(0.0, 0.0, 0.0)]
    basis_Ti = [(0.5, 0.5, 0.5)]
    cell_par = [[N, 0.0,0.0],
                [0.0,N,0.0],
                [0.0,0.0,N]]
    positions = []

    # --------- Ni sublattice ---------
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for (x, y, z) in basis_Ni:
                    fx = (i + x) / N
                    fy = (j + y) / N
                    fz = (k + z) / N

                    # convert fractional → angstrom
                    positions.append(("Ni", fx * cell_length,
                                          fy * cell_length,
                                          fz * cell_length))

    # --------- Ti sublattice ---------
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for (x, y, z) in basis_Ti:
                    fx = (i + x) / N
                    fy = (j + y) / N
                    fz = (k + z) / N

                    positions.append(("Ti", fx * cell_length,
                                          fy * cell_length,
                                          fz * cell_length))

    return positions,cell_par

    
