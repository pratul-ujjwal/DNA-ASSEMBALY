class Node:
    def __init__(self, label):
        self.label = label
        self.incoming = 0
        self.outgoing = 0

class Edge:
    def __init__(self,label):
        self.label = label

def generate_kmer(read, length):
    for i in range(len(read)-length+1):
        yield (read[i:i+length-1], read[i+1:i+length])


reads_file = open(r"C:\Users\pratu\Desktop\UMD\Winter-2020\CIS-586\genomes\simulated_reads_part.txt","r")
reads = []
for read in reads_file:
    reads.append(read[:-2])

edges = dict()
nodes = dict()
        
for read in reads:
    for kmerL,kmerR in generate_kmer(read,16):
        if kmerL in edges.keys():
            nodes[kmerL].outgoing+=1
            edges[kmerL]+= [Edge(kmerR)]
        else:
            nodes[kmerL] = Node(kmerL)
            nodes[kmerL].outgoing+=1
            edges[kmerL] = [Edge(kmerR)]
        if kmerR in edges.keys():
            nodes[kmerR].incoming+=1
        else:
            nodes[kmerR] = Node(kmerR)
            nodes[kmerR].incoming+=1
            edges[kmerR] = []
    
list_node = list(nodes.keys())
first_node = list_node[0]
for key in nodes.keys():
    if nodes[key].incoming < nodes[first_node].incoming:
        first_node = key

contig = first_node
cursor = first_node

while len(edges[cursor]) > 0:
    next_node = edges[cursor][0]
    del edges[cursor][0]
    contig += next_node.label[-1]
    cursor = next_node.label

print(contig)


          
            
            