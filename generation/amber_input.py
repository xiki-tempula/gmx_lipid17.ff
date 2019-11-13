
acyl_list = ['LAL', 'MY', 'PA', 'OL', 'ST', 'AR', 'DHA']
head_group_list = ['PC', 'PE', 'PS', 'PGR', 'PH-']
with open('tleap.in', 'w') as f:
    f.write('source leaprc.protein.ff14SB\n')
    f.write('source leaprc.lipid17\n')

    for acyl_1 in acyl_list:
        for head_group in head_group_list:
            for acyl_2 in acyl_list:
                f.write('lipid = sequence {{{} {} {}}}\n'.format(acyl_1, head_group, acyl_2))
                f.write('setBox lipid "vdw" 20\n')
                f.write('savepdb lipid {lipid}.pdb\n'.format(lipid='{}_{}_{}'.format(acyl_1, head_group, acyl_2)))
                f.write('saveamberparm lipid {lipid}.prmtop {lipid}.inpcrd\n'.format(
                    lipid='{}_{}_{}'.format(acyl_1, head_group, acyl_2)))

    # add Cholesterol

    f.write('lipid = sequence {{{}}}\n'.format('CHL'))
    f.write('setBox lipid "vdw" 20\n')
    f.write('savepdb lipid {lipid}.pdb\n'.format(lipid='CHL'))
    f.write('saveamberparm lipid {lipid}.prmtop {lipid}.inpcrd\n'.format(
        lipid='CHL'))