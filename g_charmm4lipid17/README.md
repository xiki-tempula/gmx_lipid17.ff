# Procedure of charmmlipid2amber.py generation
## Lipid generation
All of the charmm lipids, which are supported by amber are generated from the
charmm-GUI membrane builder and the corresponding file for gromacs is included
in the folder [`charmm-gui_gromacs`](https://github.com/xiki-tempula/gmx_lipid17.ff/tree/master/g_charmm4lipid17/charmm-gui_gromacs).

## Script validation
The validation of the script is tested against the original charmm implementation
in the folder [`validate`](https://github.com/xiki-tempula/gmx_lipid17.ff/tree/master/g_charmm4lipid17/validate), where the bond, angle and dihedral energy are compared
between the original charmm implementation and the converted amber format to ensure
that no atom names has been mislabelled.

```bash
cd validate
python validate.py
```
