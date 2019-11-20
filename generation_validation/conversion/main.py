from ff_io import Reader, FFWriter, itpWriter
from merge import merge

acyl_list = ['LAL', 'MY', 'PA', 'OL', 'ST', 'AR', 'DHA']
head_group_list = ['PC', 'PE', 'PS', 'PGR', 'PH-']

if __name__ == '__main__':
    top_list = []
    for acyl_1 in acyl_list:
        for head_group in head_group_list:
            for acyl_2 in acyl_list:
                lipid = '{}_{}_{}'.format(acyl_1, head_group, acyl_2)
                top_list.append(Reader('../generation/{}.top'.format(lipid)).top)

    top_list.append(Reader('../generation/{}.top'.format('CHL')).top)
    top = merge(top_list)
    FFWriter(top, '../lipid17.ff')
    with open('../lipid17.itp', 'w') as f:
        for top in top_list:
            itpWriter(top, f)
