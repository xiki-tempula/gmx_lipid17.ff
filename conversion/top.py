import copy
import os
from fields import *

class Topology():
    def __init__(self):
        self.content_dict = {}
        self.content_list = []
        self.name = None


    def _idx2name(self, idx):
        for atom in self.content_dict['atoms']:
            try:
                if atom._nr == idx:
                    return atom._type
            except:
                pass

    def convert_ff(self):
        for atomtype in self.content_dict['atomtypes']:
            atomtype._comment = self.name

        bondtypes = Field('bondtypes')
        for bond in self.content_dict['bonds']:
            if not isinstance(bond, Comment):
                new_bond = copy.copy(bond)
                new_bond._comment = self.name + bond.to_str()
                bond._b0 = ''
                bond._kb = ''
                new_bond._i = self._idx2name(bond._i)
                new_bond._j = self._idx2name(bond._j)
                bondtypes.append(new_bond)
        bondtypes.uniqle()
        self.content_dict['bondtypes'] = bondtypes

        angletypes = Field('angletypes')
        for angle in self.content_dict['angles']:
            if not isinstance(angle, Comment):
                new_angle = copy.copy(angle)
                new_angle._comment = self.name + angle.to_str()
                angle._th0 = ''
                angle._cth = ''
                new_angle._i = self._idx2name(angle._i)
                new_angle._j = self._idx2name(angle._j)
                new_angle._k = self._idx2name(angle._k)
                angletypes.append(new_angle)
        angletypes.uniqle()
        self.content_dict['angletypes'] = angletypes

        dihedraltypes = Field('dihedraltypes')
        for dihedral in self.content_dict['dihedrals']:
            if not isinstance(dihedral, Comment):
                new_dihedral = copy.copy(dihedral)
                new_dihedral._comment = self.name + dihedral.to_str()
                dihedral._phase = ''
                dihedral._kd = ''
                dihedral._pn = ''
                if dihedral._func == '1':
                    dihedral._func = '9'
                    new_dihedral._func = '9'
                new_dihedral._i = self._idx2name(dihedral._i)
                new_dihedral._j = self._idx2name(dihedral._j)
                new_dihedral._k = self._idx2name(dihedral._k)
                new_dihedral._l = self._idx2name(dihedral._l)

                dihedraltypes.append(new_dihedral)
        dihedraltypes.sort_dihedral()
        dihedraltypes.uniqle()
        self.content_dict['dihedrals'].uniqle()
        self.content_dict['dihedraltypes'] = dihedraltypes
