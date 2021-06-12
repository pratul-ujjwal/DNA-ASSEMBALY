def suffixArray(Read_concatenation):
    sorted_substrings = sorted([(Read_concatenation[i:],i) for i in range(0, len(Read_concatenation)+1)])
    return map(lambda j: j[1], sorted_substrings)

def generate_bwt(Read_concatenation):
    list = []
    SA = suffixArray(Read_concatenation)
    suffixArrayfile = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\suffix_file.txt","w")
    for i in SA:
        suffixArrayfile.write(Read_concatenation[i-1] + ',' + str(i) + '\n')
        if i == 0:
            list.append('#')
        else:
            list.append(Read_concatenation[i-1])
    suffixArrayfile.close()
    return ''.join(list)

reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","r")
full_read = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\full_search.txt","w")

read_string = ''
for rec in reads_file:
    rec1 = rec[:-1]
    read_string += rec1
   
length_reads = len(read_string)

bwt_string = generate_bwt(read_string)
full_read.write(read_string)
bwt_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\bwt_file.txt","w")
full_read.close()
bwt_file.write(bwt_string)
bwt_file.close()
reads_file.close()

