
class Comment():
    def __init__(self, comment):
        self._content = comment
    def to_str(self):
        return '; ' + self._content
    def __getattr__(self, item):
        return None
    def __repr__(self):
        return self._content

class Default():
    def __init__(self, nbfunc, comb_rule, gen_pairs, fudgeLJ, fudgeQQ):
        self._nbfunc = nbfunc
        self._comb_rule = comb_rule
        self._gen_pairs = gen_pairs
        self._fudgeLJ = fudgeLJ
        self._fudgeQQ = fudgeQQ

    def to_str(self):
        return '{: <15} {: <15} {: <15} {: <12} {: <12}'.format(self._nbfunc, self._comb_rule, self._gen_pairs,
                                                                        self._fudgeLJ, self._fudgeQQ)

    def __eq__(self, other):
        if (self._nbfunc == other._nbfunc) and (self._comb_rule == other._comb_rule) and \
                (self._gen_pairs == other._gen_pairs) and (self._fudgeLJ == other._fudgeLJ) and \
                (self._fudgeQQ == other._fudgeQQ):
            return True
        else:
            return False

    def __repr__(self):
        return str((self._nbfunc, self._comb_rule, self._gen_pairs, self._fudgeLJ, self._fudgeQQ))

class Atomtype():
    def __init__(self, name, at_num, mass, charge, ptype, sigma, epsilon, comment=''):
        self._name = name
        self._at_num = at_num
        self._mass = mass
        self._charge = charge
        self._ptype = ptype
        self._sigma = sigma
        self._epsilon = epsilon
        self._comment = comment

    def to_str(self):
        return '{: <15} {: <3} {: <11} {: <12} {: <6} {: <16} {: <16} ; {}'.format(self._name, self._at_num, self._mass,
                                                                self._charge, self._ptype, self._sigma,
                                                                self._epsilon, self._comment)

    def __eq__(self, other):
        if (self._name == other._name) and (self._at_num == other._at_num) and \
                (self._mass == other._mass) and (self._charge == other._charge) and \
                (self._ptype == other._ptype) and (self._sigma == other._sigma) and \
                (self._epsilon == other._epsilon):
            return True
        else:
            return False

    def __repr__(self):
        return str((self._name, self._at_num, self._mass, self._charge, self._ptype, self._sigma, self._epsilon))

class Moleculetype():
    def __init__(self, name, nrexcl):
        self._name = name
        self._nrexcl = nrexcl

    def to_str(self):
        return self._name + ' ' + self._nrexcl

    def __repr__(self):
        return str((self._name, self._nrexcl))

class Atom():
    def __init__(self, nr, type, resnr, residue, atom, cgnr, charge, mass, typeB = '', chargeB = '', massB = ''):
        self._nr = int(nr)
        self._type = type
        self._resnr = int(resnr)
        self._residue = residue
        self._atom = atom
        self._cgnr = int(cgnr)
        self._charge = charge
        self._mass = mass
        self._typeB = typeB
        self._chargeB = chargeB
        self._massB = massB

    def to_str(self):
        # not printing the B states
        return '{: <5} {: <11} {: <7} {: <7} {: <7} {: <7} {: <12} {: <11}'.format(self._nr, self._type, self._resnr,
                                                                                   self._residue, self._atom, self._cgnr,
                                                                                   self._charge, self._mass)
    def __repr__(self):
        return str((self._nr, self._type, self._resnr, self._residue, self._atom, self._cgnr, self._charge, self._mass))

class Bond():
    def __init__(self, i, j, func, b0 = '', kb = '', comment=''):
        self._i = int(i)
        self._j = int(j)
        self._func = func
        self._b0 = b0
        self._kb = kb
        self._comment = comment

    def to_str(self):
        return '{: <7} {: <7} {: <6} {: <10} {: <14} ; {}'.format(self._i, self._j, self._func, self._b0, self._kb,
                                                                  self._comment)

    def __contains__(self, idx):
        return idx in [self._i, self._j]

    def __eq__(self, other):
        if (self._i == other._i) and (self._j == other._j) and \
                (self._func == other._func) and (self._b0 == other._b0) and \
                (self._kb == other._kb):
            return True
        else:
            return False

    def __repr__(self):
        return str((self._i, self._j, self._func, self._b0, self._kb))

class Pair():
    def __init__(self, i, j, func, b0 = '', kb = ''):
        self._i = i
        self._j = j
        self._func = func
        self._b0 = b0
        self._kb = kb
    def to_str(self):
        return '{: <7} {: <7} {: <6} {: <10} {: <14}'.format(self._i, self._j, self._func, self._b0, self._kb)

    def __repr__(self):
        return str((self._i, self._j, self._func, self._b0, self._kb))

class Angle():
    def __init__(self, i, j, k, func, th0 = '', cth = '', comment=''):
        self._i = int(i)
        self._j = int(j)
        self._k = int(k)
        self._func = func
        self._th0 = th0
        self._cth = cth
        self._comment = comment
    def to_str(self):
        return '{: <7} {: <7} {: <7} {: <6} {: <10} {: <14} ; {}'.format(self._i, self._j, self._k, self._func,
                                                                         self._th0, self._cth, self._comment)
    def __eq__(self, other):
        if (self._i == other._i) and (self._j == other._j) and \
                (self._func == other._func) and (self._k == other._k) and \
                (self._th0 == other._th0) and (self._cth == other._cth):
            return True
        else:
            return False
    def __repr__(self):
        return str((self._i, self._j, self._k, self._func, self._th0, self._cth))

class Dihedral():
    def __init__(self, i, j, k, l, func, phase = '', kd = '', pn='', comment=''):
        self._i = int(i)
        self._j = int(j)
        self._k = int(k)
        self._l = int(l)
        self._func = func
        self._phase = phase
        self._kd = kd
        self._pn = pn
        self._comment = comment
    def to_str(self):
        return '{: <7} {: <7} {: <7} {: <7} {: <6} {: <10} {: <14} {: <6} ; {}'.format(self._i, self._j, self._k, self._l,
                                                                                  self._func, self._phase, self._kd,
                                                                                  self._pn, self._comment)
    def __repr__(self):
        return str((self._i, self._j, self._k, self._l, self._func, self._phase, self._kd, self._pn))

    def __eq__(self, other):
        if (self._i == other._i) and (self._j == other._j) and \
                (self._k == other._k) and (self._l == other._l) and \
                (self._func == other._func) and (self._phase == other._phase) and \
                (self._kd == other._kd) and (self._pn == other._pn):
            return True
        elif (self._i == other._l) and (self._j == other._k) and \
                (self._k == other._j) and (self._l == other._i) and \
                (self._func == other._func) and (self._phase == other._phase) and \
                (self._kd == other._kd) and (self._pn == other._pn):
            return True
        else:
            return False

    def __contains__(self, idx):
        return idx in [self._i, self._j, self._k, self._l]

class Field():
    def __init__(self, name):
        self.name = name
        self.content = []

    def __eq__(self, other):
        current = [line for line in self.content if not isinstance(line, Comment)]
        other = [line for line in other if not isinstance(line, Comment)]
        return current == other

    def append(self, line):
        self.content.append(line)

    def uniqle(self):
        content = []
        for line in self.content:
            if not line in content:
                content.append(line)
        self.content = content

    def __iter__(self):
        return self.content.__iter__()

    def __getitem__(self, index):
        return self.content.__getitem__(index)

    def to_str(self):
        output = []
        output.append('[ {} ]'.format(self.name))
        for line in self.content:
            output.append(line.to_str())
        return '\n'.join(output)

    def union(self, other):
        for line in other:
            if not line in self.content:
                self.content.append(line)

    def sort_dihedral(self):
        '''Since dihedral A-B-C-D is the same as D-C-B-A,
        It is necessary to lump them together.'''
        self.content.sort(key = lambda x: sorted([(x._i, x._j, x._k, x._l), (x._l, x._k, x._j, x._i)]))

        # fix the atom order if D-C-B-A exist at the same time as A-B-C-D
        for i in range(1, len(self.content)):
            current = self.content[i]
            previous = self.content[i-1]
            if (current._i, current._j, current._k, current._l) == (previous._l, previous._k, previous._j, previous._i):
                current._i, current._j, current._k, current._l = previous._i, previous._j, previous._k, previous._l

    def atom_idx2attr(self, idx, attr):
        for line in self.content:
            if not isinstance(line, Comment):
                if line._nr == idx:
                    return getattr(line, attr)

    def atom_reindex(self):
        '''Alter the atom index to make sure that it can be used in rtp file'''
        for index, line in enumerate(self.content):
            if not isinstance(line, Comment):
                line._mass = index
                line._nr = ''


