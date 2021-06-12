def rankBwt(bwt_string):
    total = dict()
    ranks = []
    for i in bwt_string:
        if i not in total:
                total[i] = 0
        ranks.append(total[i])
        total[i] += 1
    return ranks, total

def rankAllBwt(bwt_string):
    total = {}
    rankAll = {}
    for i in bwt_string:
        if i not in total:
            total[i] = 0
            rankAll[i] = []
    for i in bw:
        tots[i] += 1
        for i in total:
            rankAll[i].append(total[i])
    return rankAll, total


def firstCol(total):
    first = {}
    totcount = 0
    for c, count in sorted(total.items()):
        first[c] = (totcount, totcount + count)
        totcount += count
    return first

def get_match_index(bwt, pr):
    rankAll, total = rankAllBwt(bwt)
    first = firstCol(total)
    if pr[-1] not in first:
        return 0 # character doesn’t occur in read
    l1, r1 = first[pr[-1]]
    i = len(pr)-2
    while i >= 1 and r1 > l1:
        c1 = pr[i]
        l1 = first[c1][0] + rankAll[c1][l1-1]
        r1 = first[c1][0] + rankAll[c1][r1-1]
        i -= 1
    return l1, r1, pr[i+1:]


def binary_scan(array, start, end, key):
    if (start < end):
        mid = (start + end)//2
        index1, read_no1  = array[mid]
        index2, read_no2  = array[mid+1]
        read_no1 = int(read_no1[:-1])
        read_no2 = int(read_no2[:-1])
        if ((read_no1 <= key) and (read_no2 >= key)):
            if read_no2 == key:
                return index2
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

def get_relevant_lines(all_lines, top, bottom):
    i = 0
    for lines in all_lines:
        if i < top:
            i+=1
            continue
        elif (i >= top) and (i < bottom) :
            relevant_lines.append(lines)
            i+=1
        else:
            return relevant_lines
    return relevant_lines
bwt_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\bwt_file.txt","r")
suffix_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\suffix_file.txt","r")
reads_offset_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_offset.txt","r")
reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","r")
overlap_config_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\overlap_config.txt","w")
overlap_strings_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\overlap_data.txt","w")
bw = bwt_file.read()
offsets = []
all_lines = []
for lines in enumerate(reads_offset_file):
    offsets.append(lines)
for i, lines in enumerate(suffix_file):
    all_lines.append(lines)
ranks, tots = rankBwt(bw)
first = firstCol(tots)
rankAll, tots = rankAllBwt(bw)
#node_count = 0
overlap_config = []
overlap_data = []
for rec in reads_file:
    read_match = []
    relevant_lines = []
    rec = rec[:-2]
    top, bottom, overlap = get_match_index(bw,rec)
    if len(overlap) < 12:
        overlap_config.append(read_match)
        overlap_data.append(overlap)
        continue;
    relevant_lines = get_relevant_lines(all_lines, top, bottom)
    read_match = get_matching_reads(relevant_lines, offsets)
    overlap_config.append(read_match)
    overlap_data.append(overlap)
for rec in overlap_config:
    rec1 = str(rec) + '\n'
    overlap_config_file.write(rec1)
for rec in overlap_data:
    rec1 = str(rec) + '\n'
    overlap_strings_file.write(rec1)

bwt_file.close()
suffix_file.close()
reads_offset_file.close()
reads_file.close()
overlap_strings_file.close()
overlap_config_file.close()