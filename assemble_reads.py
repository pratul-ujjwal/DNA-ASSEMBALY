from itertools import chain

def find_overlap(read_a, read_b, minimum_length = 15):
    start = 0
    while(True):
        start = read_a.find(read_b[:minimum_length],start)
        if start == -1:
            return 0
        if read_b.startswith(read_a[start:]):
            return len(read_a) - start
        start+=1

reads = []
overlaps = []
overlap_vectors = []
merged_reads = []
overlap_matrix = [[0 for i in range(500)] for j in range(500)] 

reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","r")
overlap_config_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\overlap_config.txt","r")
overlap_strings_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\overlap_data.txt","r")
contig_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\contigs.txt","w")

count = 0

for rec in overlap_strings_file:
    overlaps.append(rec)

for rec in reads_file:
    reads.append(rec[:-2])

for rec in overlap_config_file:
    overlap_vectors.append(rec)
    if rec == '[]\n':
        count+=1
        continue
    rec = rec[1:-2]
    rec = list(rec.split(','))
    for i in rec:
        i = int(i)
        read_a = reads[count]
        read_b = reads[i]
        if read_b in read_a:
            overlap_matrix[count][i] = -1
            continue
        else:
            overlap = find_overlap(read_a, read_b, 15)
            overlap_matrix[count][i] = overlap
    overlap_matrix[count][count] = 0
    count+=1
while (True):
    flatten_matrix = list(chain.from_iterable(overlap_matrix))
    #olen = min(flatten_matrix)
    if max(flatten_matrix) > 0:
        olen_min = min(i for i in flatten_matrix if i > 0)
    else:
        break
    if olen_min >= 15:
        index = flatten_matrix.index(olen_min)
        row = index//500
        column = index%500
        overlap_row = overlap_vectors[row]
        overlap_row = overlap_row[1:-2]
        overlap_row = list(overlap_row.split(','))
        read_a = reads[row]
        for i in overlap_row:
            i = int(i)
            if i == row:
                continue
            olen = overlap_matrix[row][i]
            if olen != 0:
                if olen != -1:
                    read_b = reads[i]
                    reads[i] = read_a + read_b[olen:]
                else:
                    reads[i] = read_a
                overlap_matrix[row][i] = 0
                for j in range(500):
                    overlap_matrix[j][i] = overlap_matrix[j][row]
        for i in range(500):
            overlap_matrix[row][i] = 0
        reads[row] = ''
    else:
        break
for read in reads:
    contig_file.write(read + '\n')
contig_file.close()
    
    
