import glob, os
global ii
def rename(dir, pattern, titlePattern,i):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, titlePattern % str(i).zfill(4) ))
        i = i + 1
    global ii
    ii = i
    print(i)
	
rename(r'/home/godfather/Documents/text-search-engine-master/input',r'*',r'doc%s',0)

for x in range(ii):
	with open("input/doc" + str(x).zfill(4),'r') as infile,open("corpus/doc" + str(x).zfill(4), 'w') as outfile:
		for line in infile:
			if not line.strip():
				continue
			outfile.write(line)
	infile.close()
	outfile.close()		

















# with open("corpus/doc" + str(x).zfill(4),'w') as write_to , open('o.txt', 'r') as write_from:
# 			for line in write_from:
# 				write_to.write(line)
# 			write_to.close()
# 			write_from.close()



	# with open("corpus/doc" + str(doc_id).zfill(4)) as infile, open('output.txt', 'w') as outfile:
 #    	for line in infile:
 #        	if not line.strip(): continue  # skip the empty line
 #        	outfile.write(line)  # non-empty line. Write it to output