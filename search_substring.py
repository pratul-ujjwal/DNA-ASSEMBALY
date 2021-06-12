def rankBwt(bw):
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots:
                tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots

def reverseBwt(bw):
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0
    t = "$"
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t
        rowi = first[c][0] + ranks[rowi]
    return t

def rankAllBwt(bw):
    tots = {}
    rankAll = {}
    for ci in bw:
        if ci not in tots:
            tots[ci] = 0
            rankAll[ci] = []
    for ci in bw:
        tots[ci] += 1
        for ci in tots:
            rankAll[ci].append(tots[ci])
    return rankAll, tots


def firstCol(tots):
    first = {}
    totc = 0
    for c, count in sorted(tots.items()):
        first[c] = (totc, totc + count)
        totc += count
    return first

def get_match_index(bw, pr):
    rankAll, tots = rankAllBwt(bw)
    first = firstCol(tots)
    if pr[-1] not in first:
        return 0 # character doesn’t occur in T
    l1, r1 = first[pr[-1]]
    i = len(pr)-2
    while i >= 0 and r1 > l1:
        c1 = pr[i]
        l1 = first[c1][0] + rankAll[c1][l1-1]
        r1 = first[c1][0] + rankAll[c1][r1-1]
        i -= 1
    return l1,r1, pr[i+1:] # return the index of matched records and overlap string

def binary_scan(array, start, end, key):
    if (start < end):
        mid = (start + end)//2
        index1, read_no1  = array[mid]
        index2, read_no2  = array[mid+1]
        read_no1 = int(read_no1[:-1])
        read_no2 = int(read_no2[:-1])
        if ((read_no1 < key) and (read_no2 > key)):
            return index1
        elif (read_no1 > key):
            return binary_scan(array,start,mid,key)
        else:
            return binary_scan(array, mid+1,end,key)
    else:
        return -1

def get_matching_reads(suffix_lines, reads_offset):
    no_of_reads = 500
    matching_reads_sn = []
    for lines in suffix_lines:
        lines = lines[:-1]
        char, pos = lines.split(',')
        pos = int(pos)
        read_no = binary_scan(reads_offset, 0, no_of_reads, pos)
        matching_reads_sn.append(read_no)
    return matching_reads_sn

bwt_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\bwt_file.txt","r")
suffix_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\suffix_file.txt","r")
reads_offset = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_offset.txt","r")
reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","r")
overlap_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\overlap_file.txt","r")
bw = bwt_file.read()
offsets = []
for lines in enumerate(reads_offset):
    offsets.append(lines)
relevant_lines = []
ranks, tots = rankBwt(bw)
first = firstCol(tots)
rankAll, tots = rankAllBwt(bw)
node_count = 0
raw_graph_data = []
for rec in reads_file:
    rec1 = rec[:-1]
    top, bottom, overlap = get_match_index(bw,rec1)
    for i, lines in enumerate(suffix_file):
        if i < top:
            continue
        elif (i >= top) and (i <= bottom) :
            relevant_lines.append(lines)
        else:
            break
    read_match = get_matching_reads(relevant_lines, offsets)
    graph_line = str(node_count) + str(read_match) + '\n'
    raw_graph_data.append(graph_line)
    node_count+=1
overlap_file.write(raw_graph_data)
bwt_file.close()
suffix_file.close()
reads_offset.close()
    