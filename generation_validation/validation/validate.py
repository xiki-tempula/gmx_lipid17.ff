import os
from subprocess import call
import numpy as np
#
os.environ["GMXLIB"] = os.path.split(os.path.split(os.getcwd())[0])[0]
os.environ["GMX_MAXBACKUP"] = '-1'
gmx = '/usr/local/gromacs/2019.4/bin/gmx'
sander = '/Users/grte2001/src/amber18/bin/sander'

def amber_energy(txt):
    with open(txt, 'r') as f:
        txt = f.read()
    txt = txt.strip().replace('\n', '')
    energy = txt.split()
    potential = float(energy[energy.index('EPtot')+2])
    bonded = float(energy[energy.index('BOND') + 2])
    angle = float(energy[energy.index('ANGLE') + 2])
    dihedral = float(energy[energy.index('DIHED') + 2])
    return potential, bonded, angle, dihedral

def gromacs_energy(txt):
    with open(txt, 'r') as f:
        txt = f.read()
    txt = txt.strip()
    txt = txt[txt.index('Energies (kJ/mol)'): txt.index('<======  ###############  ==>')]
    lines = txt.split('\n')
    names = lines[1].strip()+lines[3].strip()+lines[5].strip()
    names = [name for name in names.split('  ') if name]
    energys = lines[2].strip()+lines[4].strip()+lines[6].strip()
    energys = [energy for energy in energys.split('  ') if energy]

    potential = float(energys[names.index('Potential')]) * 0.239006
    bonded = float(energys[names.index('Bond')]) * 0.239006
    angle = float(energys[names.index('Angle')]) * 0.239006
    dihedral = float(energys[names.index('Proper Dih.')]) * 0.239006
    return potential, bonded, angle, dihedral

acyl_list = ['LAL', 'MY', 'PA', 'OL', 'ST', 'AR', 'DHA']
head_group_list = ['PC', 'PE', 'PS', 'PGR', 'PH-']
with open('energy_difference.log', 'w') as f:
    f.write('Energy difference:\n')
energy_difference_list = []
for acyl_1 in acyl_list:
    for head_group in head_group_list:
        for acyl_2 in acyl_list:
            lipid = '{}_{}_{}'.format(acyl_1, head_group, acyl_2)
            call('{gmx} pdb2gmx -f ../../gro/{lipid}.gro -o temp.gro -ff lipid17'.format(gmx=gmx, lipid=lipid), shell=True)
            call('{gmx} grompp -f gromacs.mdp -c ../generation/{lipid}.pdb -o {lipid}.tpr'.format(gmx=gmx,
                                                                                                           lipid=lipid),
                 shell=True)
            call('{gmx} mdrun -deffnm {lipid}'.format(gmx=gmx, lipid=lipid), shell=True)
            gmx_energy = gromacs_energy('{lipid}.log'.format(lipid=lipid))
            call('{sander} -O -i amber.in -p ../generation/{lipid}.prmtop -c ../generation/{lipid}.inpcrd -inf {lipid}.mdinfo'.format(sander=sander,
                                                                                                           lipid=lipid),
                 shell=True)
            amb_energy = amber_energy('{lipid}.mdinfo'.format(lipid=lipid))

            energy_difference = np.abs(np.array(amb_energy) - np.array(gmx_energy))
            energy_difference_list.append(energy_difference)
            with open('energy_difference.log', 'a+') as f:
                f.write('{}: Potential {:.2f}; Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(lipid, *energy_difference))

lipid = 'CHL'

call('{gmx} pdb2gmx -f ../../gro/{lipid}.gro -o temp.gro -ff lipid17'.format(gmx=gmx, lipid=lipid), shell=True)
call('{gmx} grompp -f gromacs.mdp -c ../generation/{lipid}.pdb -o {lipid}.tpr'.format(gmx=gmx, lipid=lipid), shell=True)
call('{gmx} mdrun -deffnm {lipid}'.format(gmx=gmx, lipid=lipid), shell=True)
gmx_energy = gromacs_energy('{lipid}.log'.format(lipid=lipid))
call(
    '{sander} -O -i amber.in -p ../generation/{lipid}.prmtop -c ../generation/{lipid}.inpcrd -inf {lipid}.mdinfo'.format(
        sander=sander,
        lipid=lipid),
    shell=True)
amber_energy = amber_energy('{lipid}.mdinfo'.format(lipid=lipid))

energy_difference = np.abs(np.array(amber_energy) - np.array(gmx_energy))
energy_difference_list.append(energy_difference)
with open('energy_difference.log', 'a+') as f:
    f.write('{}: Potential {:.2f}; Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(lipid, *energy_difference))

max_energy_difference_list = np.max(energy_difference_list, axis=0)
with open('energy_difference.log', 'a+') as f:
    f.write('Max: Potential {:.2f}; Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(*max_energy_difference_list))