gmx_lipid17.ff:
A gromacs port of the amber lipid force field LIPID17
==============================================================

This is a gromacs port of the amber LIPID17 force field. The amber to gromacs
format conversion is first done with ParmEd (https://github.com/ParmEd/ParmEd).
I have written a script to condense all the bonded interactions into force field
format, provide the corresponding gro file for every lipids and validate the
energy to make sure the gromacs port yield the same energy as the original amber
format.

# Usage
## Convert charmm lipid to amber lipid

To use the lipids in the LIPID17, one can use `charmmlipid2amber.py` to convert
the lipid membrane made in charmm-GUI membrane builder.

It is worth noting that not all charmm lipids are supported in amber lipid17
force field. Since lipid17 is a modular force field, each lipid is constructed
as two acryl chains and a head group. The available acryl chain and head groups are:

|            | Description              | Residue Name |
|------------|--------------------------|--------------|
| Acyl chain | Lauroyl (12:0)           | LAL          |
|            | Myristoyl (14:0)         | MY           |
|            | Palmitoyl (16:0)         | PA           |
|            | Oleoyl (18:1 n-9)        | OL           |
|            | Stearoyl (18:0)          | ST           |
|            | Arachidonoyl (20:4)      | AR           |
|            | Docosahexaenoyl (22:6)   | DHA          |
| Head group | Phosphatidylcholine      | PC           |
|            | Phosphatidylethanolamine | PE           |
|            | Phosphatidylserine       | PS           |
|            | Phosphatidylglycerol     | PGR          |
|            | Phosphaditic acid        | PH-          |
| Other      | Cholesterol              | CHL          |

To use `charmmlipid2amber.py`, [`MDAnalysis`](https://www.mdanalysis.org/) and python3
are required. `MDAnalysis` can be installed via simple pip installation.

```bash
pip install --upgrade MDAnalysis
```

Then one can use `charmmlipid2amber.py` to convert the charmm-GUI output to a
format which is compatible with lipid17.ff.

```bash
python charmmlipid2amber.py -f charmm2gmx.pdb -o amber_lipid.gro -lipids POPC
```

Which will convert the lipid `POPC` in the file `charmm2gmx.pdb` to
the file `amber_lipid.gro`. If the field `lipids` is left as blank, the script will
attempt to convert all lipids in charmm-GUI membrane builder to the corresponding
amber lipid.

The script will printout the name of the new converted amber lipids as well as
the number of the corresponding lipids for adding to the gromacs topology file.
A sample topology is given below.

```
; Include the lipid17 forcefield
#include "lipid17.ff/forcefield.itp"
; Include the lipid17 itp files
#include "lipid17.itp"

[ system ]
; Name
Lipid

[ molecules ]
; Compound        #mols
PA_PC_OL               1
```

The force field `lipid17.ff` and the itp file `lipid17.itp` needs to be included.
The name of amber lipid is arranged in the format of {AcrylChain1}\_{HeadGroup}\_{AcrylChain2}.
The popular POPC lipid will have a name of PA_PC_OL, whereas Cholesterol will
have a name of CHL. For the lipid where the two Acyl chains are the same such
as DMPC, the name of the lipid is MY_PC_MY.

## Use amber lipids directly

Alternatively, the amber lipids can be used directly. The gro file for each
lipid can be found in the [`gro`](https://github.com/xiki-tempula/gmx_lipid17.ff/tree/master/gro) folder. for lipid POPC, the gro file has a name
of `PA_PC_OL.gro`. Or one can generate the lipid bilayer in amber and use it in
gromacs.

# Generation and validation
The files and script for generation and validation can be found in the folder
[`generation_validation`](https://github.com/xiki-tempula/gmx_lipid17.ff/tree/master/generation_validation), where as the validation of `charmmlipid2amber.py`
can be found in the folder [`g_charmm4lipid17`](https://github.com/xiki-tempula/gmx_lipid17.ff/tree/master/g_charmm4lipid17).
