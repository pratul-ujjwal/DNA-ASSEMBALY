import random

def generate_read(genome, random_length):
    idx = random.randrange(0,len(genome) - random_length + 1)
    return genome[idx: (idx + random_length)]

genome = ''
gene_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\Coronavirus_final.txt","r")
reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","w")
reads_offset = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_offset.txt","w")
for rec in gene_file:
    genome += rec[:-1]

gene_file.close()
offset = 0
reads_offset.write(str(offset) + '\n')
for i in range(0,500):
    random_length = random.randrange(40,80)
    read = generate_read(genome, random_length)
    offset  = offset + len(read) + 1
    reads_offset.write(str(offset) + '\n')
    reads_file.write(read + '$' + '\n')
    
reads_offset.close()       
reads_file.close()