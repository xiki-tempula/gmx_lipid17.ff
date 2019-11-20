from ff_io import Reader, FFWriter, itpWriter
from top import Topology


def merge(top_list):
    content_dict = {}
    content_list = []

    for top in top_list:
        top.convert_ff()
        if 'defaults' in content_dict:
            assert top.content_dict['defaults'] == content_dict['defaults']
        else:
            content_dict['defaults'] = top.content_dict['defaults']

        for section_name in ['atomtypes', 'bondtypes', 'angletypes', 'dihedraltypes']:
            if section_name in content_dict:
                content_dict[section_name].union(top.content_dict[section_name])
            else:
                content_dict[section_name] = top.content_dict[section_name]

    top = Topology()
    top.content_list = content_list
    top.content_dict = content_dict
    return top
