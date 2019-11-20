# Procedure of charmmlipid2amber.py generation
## Lipid generation
All of the charmm lipids, which are supported by amber are generated from the
charmm-GUI membrane builder and the corresponding file for gromacs is included
in the folder `charmm-gui_gromacs`.

## Script validation
The validation of the script is tested against the original charmm implementation
in the folder `validate`, where the bond, angle and dihedral energy are compared
between the original charmm implementation and the converted amber format to ensure
that no atom name has been mislabelled.

```bash
cd validate
python validate.py
```
