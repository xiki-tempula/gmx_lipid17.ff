import parmed as pmd
from subprocess import call
import os
acyl_list = ['LAL', 'MY', 'PA', 'OL', 'ST', 'AR', 'DHA']
head_group_list = ['PC', 'PE', 'PS', 'PGR', 'PH-']
os.mkdir('../gro')
for acyl_1 in acyl_list:
    for head_group in head_group_list:
        for acyl_2 in acyl_list:
            lipid = '{}_{}_{}'.format(acyl_1, head_group, acyl_2)
            call('sander -O -i em.in -p {lipid}.prmtop -c {lipid}.inpcrd -r {lipid}.rst'.format(lipid=lipid), shell=True)
            amber = pmd.load_file('{}.prmtop'.format(lipid), '{}.rst'.format(lipid))
            amber.save('{}.top'.format(lipid))
            amber.save('gro/{}.gro'.format(lipid))
# add Cholesterol
lipid = 'CHL'
call('sander -O -i em.in -p {lipid}.prmtop -c {lipid}.inpcrd -r {lipid}.rst'.format(lipid=lipid), shell=True)
amber = pmd.load_file('{}.prmtop'.format(lipid), '{}.rst'.format(lipid))
amber.save('{}.top'.format(lipid))
amber.save('../gro/{}.gro'.format(lipid))