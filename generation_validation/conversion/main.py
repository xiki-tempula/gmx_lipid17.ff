from ff_io import Reader, FFWriter, itpWriter, rtpWriter, atpWriter
from merge import merge, unique_rtp

start_residue_suffix = '1'
end_residue_suffix = '2'
acyl_list = ['LAL', 'MY', 'PA', 'OL', 'ST', 'AR', 'DHA']
head_group_list = ['PC', 'PE', 'PS', 'PGR', 'PH-']

if __name__ == '__main__':
    top_list = []
    for acyl_1 in acyl_list:
        for head_group in head_group_list:
            for acyl_2 in acyl_list:
                lipid = '{}_{}_{}'.format(acyl_1, head_group, acyl_2)
                top_list.append(Reader('../generation/{}.top'.format(lipid)).top)

    top_list.append(Reader('../generation/{}.top'.format('CHL')).top)
    top, residue_list = merge(top_list, start_residue_suffix, end_residue_suffix)
    FFWriter(top, '../../lipid17.ff')
    with open('../../lipid17.ff/atomtypes.atp', 'w') as f:
        atpWriter(top, f)

    with open('../../lipid17.itp', 'w') as f:
        for top in top_list:
            itpWriter(top, f)

    with open('../../lipid17.ff/lipids.rtp', 'w') as f:
        f.write('''[ bondedtypes ] 
; Column 1 : default bondtype
; Column 2 : default angletype
; Column 3 : default proper dihedraltype
; Column 4 : default improper dihedraltype
; Column 5 : This controls the generation of dihedrals from the bonding.
;            All possible dihedrals are generated automatically. A value of
;            1 here means that all these are retained. A value of
;            0 here requires generated dihedrals be removed if
;              * there are any dihedrals on the same central atoms
;                specified in the residue topology, or
;              * there are other identical generated dihedrals
;                sharing the same central atoms, or
;              * there are other generated dihedrals sharing the
;                same central bond that have fewer hydrogen atoms
; Column 6 : number of neighbors to exclude from non-bonded interactions
; Column 7 : 1 = generate 1,4 interactions between pairs of hydrogen atoms
;            0 = do not generate such
; Column 8 : 1 = remove proper dihedrals if found centered on the same
;                bond as an improper dihedral
;            0 = do not generate such
; bonds  angles  dihedrals  impropers all_dihedrals nrexcl HH14 RemoveDih 
     1       1          9        4        1           3      1     0 
     ''')
        residue_list, residuetypes = unique_rtp(residue_list, start_residue_suffix, end_residue_suffix)
        for residue in residue_list:
            rtpWriter(residue, f)

        with open('../../residuetypes.dat', 'w') as f:
            for residue in residuetypes:
                f.write('{} Protein\n'.format(residue))
        # change the type of chol
        with open('../../residuetypes.dat', 'r') as f:
            txt = f.read()
        with open('../../residuetypes.dat', 'w') as f:
            f.write(txt.replace('CHL Protein', 'CHL SOL'))





