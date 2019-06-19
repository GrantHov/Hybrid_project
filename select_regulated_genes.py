import sys
with open(sys.argv[1],"r+") as closest_genes:
        for line in closest_genes.readlines():
                line=line.rstrip().split('\t')
                if abs(int(line[-1]))<1000:
                        if line[9]=='+':
                                if int(line[1])<int(line[6]):
                                        print '\t'.join(line)
                        elif line[9]=="-":
                                if int(line[2])>int(line[7]):
                                        print '\t'.join(line)
