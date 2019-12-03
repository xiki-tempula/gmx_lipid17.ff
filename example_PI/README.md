# Procedure of DMPI topology generated with custom PI head group
## Forcefield modification
To paramertise the phosphatidylinositol (PI) head group, the file lipids.rtp in
the forcefield folder (lipid17.ff) has to be modified to include the entry for
PI. The file `residuetypes.dat` also need to modified where a line for the PI
head group has to be added to allow `pdb2gmx` to recognise the head group correctly.

## Lipid topology generation
After the relevant filed are modified. The topology for the new file can be
generated using the `pdb2gmx` function of Gromacs. The `GMXLIB` has to be set to
the current directory first.

```bash
export GMXLIB=$PWD
gmx pdb2gmx -f DMPI.pdb -o DMPI.gro -ff lipid17
```

## Charmm lipid conversion

The script `charmmlipid2amber.py` has been modified to allow PI head group
to be converted from charmm name to amber name.

# Note regarding the parameterisation of acryl chain
Due to the way inter-residue bonded interactions are recognised in Gromacs.
The first and the second acry chain cannot share the same topology. Thus, if one
were to create the custom acry chain, two copys of the same residue has to be
generated.

Say if we were to recreate the acryl chain Myristoyl (MY). Two copys of the MY,
namely `MY1` and `MY2` need to be created. The first `MY1` need to have a bond which
connect it to the head group. Since the head group is the *next* residue with
respect to MY. The atoms in the head group need to have a `+` in front of its
atom name, which gives `C21     +C12` in `MY1`.

However, for the second MY, since the head group is the residue *before* it. We
have to add a `-` before the atom name, which gives `C21     -C12`. However,
since this bond is already included in the head group. This line can be omitted
in `MY2`.

To tell Gromacs that the fist acryl chain has the name of `MY1` and the second
acryl chain has the name `MY2`. We have to add a line to `lipids.r2b` to indicate
this relationship.
```
MY MY MY1 MY2 -
```

Similarly, the `residuetypes.dat` is also need to be modified to allow Gromacs
to recognise these two residues.

```
MY1 Protein
MY2 Protein
```
