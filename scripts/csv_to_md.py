import sys
from os.path import isfile

def show_md_table(fname):
    assert isfile(fname), 'File not found: %s' % fname

    slines = [x.strip() for x in open(fname, 'r').readlines() if len(x.strip()) > 0]

    ol = ['|Query count|SQL Statement|']
    for cnt, l in enumerate(slines, 1):
        fmt_items = [x.strip() for x in l.split(',', 1)]
        if cnt == 1:
            hyphens = '-------------'
            ol.append('|'.join(len(fmt_items) * [hyphens]))
        ol.append('|%s|' % '|'.join(fmt_items))

    print '\n'.join(ol)


if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        show_md_table(args[1])
    else:
        print """
-------------------------------------------
Show output file in table format for github.
Assumes input is a 2 column csv table.

- Headers added will be: '|Query count|SQL Statement|'
-------------------------------------------

> python csv_to_md.py [name of csv file]

Example: > python csv_to_md.py ../query_counts/ds-09-files-no-login_counts.csv
"""