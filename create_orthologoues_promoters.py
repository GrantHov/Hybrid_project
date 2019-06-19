with open("../../orth_list_SC_SB.txt","r+") as orthologs,\
open("SC_promoters_1000bp.bed") as SC_intervals,\
open("SU_promoters_1000bp.bed") as SU_intervals,\
open("SC_orth_promoters.bed","w") as SC_orth,\
open("SU_orth_promoters.bed","w") as SU_orth,\
open("orth_promoter_length.txt","w") as length_data:
	orth_dict={}
	orthologs.next()
	for line in orthologs:
		line=line.rstrip().split("\t")
		orth_dict[line[0]]=line[-1]
	#for k,v in orth_dict.iteritems():
	#	print k,v

	SC_promoters={}
	for line in SC_intervals:
		line=line.rstrip().split("\t")
#		print line
		SC_promoters[line[1]]=line
#	print SC_promoters
	
	SU_promoters={}
        for line in SU_intervals:
                line=line.rstrip().split("\t")
                SU_promoters[line[1]]=line
 #       print SU_promoters

	for SC,SU in orth_dict.iteritems():
		if SC in SC_promoters and SU in SU_promoters:
			print SC,SU, SC_promoters[SC],SU_promoters[SU]
			SC_orth.write("%s\t%s\t%s\t%s\n"%(SC_promoters[SC][0],SC_promoters[SC][2],SC_promoters[SC][3],SC_promoters[SC][1]))
			SU_orth.write("%s\t%s\t%s\t%s\n"%(SU_promoters[SU][0],SU_promoters[SU][2],SU_promoters[SU][3],SU_promoters[SU][1]))
			length_data.write("%s\t%s\n"%(SC_promoters[SC][4],SU_promoters[SU][4]))
			
