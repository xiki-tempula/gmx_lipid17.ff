import os
from fields import *
from top import Topology
class Reader():
    def __init__(self, filename):
        content_dict = {}
        content_list = []

        with open(filename, 'r') as f:
            txt = f.read()
        sections = txt.split('[')
        for section in sections:
            if ']' in section:
                name = section[:section.index(']')].strip()
                field = Field(name)
                content = section[section.index(']')+1:].strip()
                for line in content.split('\n'):
                    if line[0] == ';':
                        field.append(Comment(line[1:]))
                    elif name == 'defaults':
                        field.append(Default(*line.split()))
                    elif name == 'atomtypes':
                        field.append(Atomtype(*line.split()))
                    elif name == 'moleculetype':
                        field.append(Moleculetype(*line.split()))
                    elif name == 'atoms':
                        field.append(Atom(*line.split()))
                    elif name == 'bonds':
                        field.append(Bond(*line.split()))
                    elif name == 'pairs':
                        field.append(Pair(*line.split()))
                    elif name == 'angles':
                        field.append(Angle(*line.split()))
                    elif name == 'dihedrals':
                        # remove empty energy
                        fields = line.split()
                        if float(fields[5]) != 0 or float(fields[6]) != 0:
                            field.append(Dihedral(*fields))
                content_list.append(field)
                content_dict[name] = field

            else:
                # Assume the whole section is comments
                comments = section.split('\n')
                for line in comments:
                    content_list.append(Comment(line[1:]))

        top = Topology()
        top.name = os.path.splitext(os.path.split(filename)[-1])[0]
        top.content_list = content_list
        top.content_dict = content_dict
        self.top = top


class FFWriter():
    def __init__(self, topology, name):
        os.mkdir(name)

        with open('{}/forcefield.itp'.format(name), 'w') as f:
            f.write(topology.content_dict['defaults'].to_str())
            f.write('''
#include "ffnonbonded.itp"
#include "ffbonded.itp"''')

        with open('{}/ffnonbonded.itp'.format(name), 'w') as f:
            f.write(topology.content_dict['atomtypes'].to_str())

        with open('{}/ffbonded.itp'.format(name), 'w') as f:
            f.write(topology.content_dict['bondtypes'].to_str())
            f.write('\n')
            f.write(topology.content_dict['angletypes'].to_str())
            f.write('\n')
            f.write(topology.content_dict['dihedraltypes'].to_str())

class itpWriter():
    def __init__(self, topology, f):
        for comment in topology.content_list:
            if isinstance(comment, Comment):
                f.write(comment.to_str() + '\n')
        f.write('\n')
        f.write('''[ moleculetype ]
; Name            nrexcl
{}          3
'''.format(topology.name))

        f.write(topology.content_dict['atoms'].to_str())
        f.write('\n')
        f.write(topology.content_dict['bonds'].to_str())
        f.write('\n')
        f.write(topology.content_dict['pairs'].to_str())
        f.write('\n')
        f.write(topology.content_dict['angles'].to_str())
        f.write('\n')
        f.write(topology.content_dict['dihedrals'].to_str())
        f.write('\n')

