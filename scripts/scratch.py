stats = """
Number of Published Files	Queries - as Admin	Queries - Not Logged In	Incremental - as Admin	Incremental - Not Logged In
0	868	374	n/a	n/a
1	922	428	54	54
2	1107	661	185	233
3	1258	812	151	151
4	1409	963	151	151
5	1560	1114	151	151
6	1711	1265	151	151
7	1862	1416	151	151
8	2013	1567	151	151
9	2164	1718	151	151
10	2315	1869	151	151
15	2662	2216	347	347
20	3009	2563	347	347
30	3601	3155	592	592
50	4634	4188	1033	1033
""".split('\n')

slines = [x.strip() for x in stats if len(x.strip()) > 0]

ol = []
for cnt, l in enumerate(slines, 1):
    fmt_items = [x.strip() for x in l.split('\t')]
    ol.append('|%s|' % '|'.join(fmt_items))
    if cnt == 1:
        hyphens = '-------------'
        ol.append('|'.join(len(fmt_items) * [hyphens]))

print '\n'.join(ol)


