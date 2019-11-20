import sys
import MDAnalysis as mda
import numpy as np
from subprocess import call
sys.path.insert(0,'../../')
from charmmlipid2amber import resname2lipid17
gmx = '/usr/local/gromacs/2019.4/bin/gmx'
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
    try:
        angle = float(energys[names.index('Angle')]) * 0.239006
    except:
        angle = float(energys[names.index('U-B')]) * 0.239006
    dihedral = float(energys[names.index('Proper Dih.')]) * 0.239006
    return potential, bonded, angle, dihedral

u = mda.Universe('../charmm-gui_gromacs/step5_charmm2gmx.pdb')
u.dimensions = [100,100,100,90,90,90]
max_bond = 0
max_angle = 0
max_dihedral = 0
for residue in u.residues:
    if not residue.resname in ['CLA', 'TIP3', 'POT']:
        u.select_atoms('resname {}'.format(residue.resname)).write('charmm/{}.gro'.format(residue.resname))
        with open('charmm/topol.top', 'w') as f:
            with open('charmm/topol.top.tmp', 'r') as tmp:
                f.write(tmp.read().format(mol=residue.resname))
        call('{gmx} grompp -f gromacs.mdp -c charmm/{lipid}.gro -o charmm/{lipid}.tpr -p charmm/topol.top -maxwarn 1'.format(gmx=gmx,lipid=residue.resname), shell=True)
        call('{gmx} mdrun -deffnm charmm/{lipid}'.format(gmx=gmx, lipid=residue.resname), shell=True)
        charmm_energy = gromacs_energy('charmm/{lipid}.log'.format(lipid=residue.resname))
        with open('energy.log', 'a+') as f:
            f.write('{}:\n'.format(residue.resname))
            f.write('Potential {:.2f}; Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(*charmm_energy))

        new, new_name = resname2lipid17(u.select_atoms('resname {}'.format(residue.resname)))
        new.dimensions = [100,100,100,90,90,90]
        new.write('amber/{}.gro'.format(new_name))
        with open('amber/topol.top', 'w') as f:
            with open('amber/topol.top.tmp', 'r') as tmp:
                f.write(tmp.read().format(mol=new_name))
        call('{gmx} grompp -f gromacs.mdp -c amber/{lipid}.gro -o amber/{lipid}.tpr -p amber/topol.top'.format(gmx=gmx,lipid=new_name), shell=True)
        call('{gmx} mdrun -deffnm amber/{lipid}'.format(gmx=gmx, lipid=new_name), shell=True)
        amber_energy = gromacs_energy('amber/{lipid}.log'.format(lipid=new_name))
        with open('energy.log', 'a+') as f:
            f.write('Potential {:.2f}; Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(*amber_energy))
        difference = np.abs(np.array(amber_energy)-np.array(charmm_energy))
        if difference[1] > max_bond:
            max_bond = difference[1]
        if difference[2] > max_angle:
            max_angle = difference[2]
        if difference[3] > max_dihedral:
            max_dihedral = difference[3]
with open('energy.log', 'a+') as f:
    f.write('Max difference: Bond {:.2f}; Angle {:.2f}; Dihedral {:.2f}\n'.format(max_bond, max_angle, max_dihedral))




