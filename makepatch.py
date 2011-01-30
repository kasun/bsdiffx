import sys
import getopt
import cPickle
import bsdiff

def make(oldfilename, newfilename, patchfilename):
	try:
		oldfile = open(oldfilename)
		olddata = oldfile.read()
		oldfile.close()
	except IOError:
		print "Wrong input for old file"
		exit()

	try:
		newfile = open(newfilename)
		newdata = newfile.read()
		newfile.close()
	except IOError:
		print "Wrong input for new file"
		exit()
		
	newdatalength = len(newdata)
	diff_tuple = bsdiff.Diff(olddata, newdata)
	diffblocklength = len(diff_tuple[1])
	diffblockdifference=[]
	for (index, char) in enumerate(diff_tuple[1]):
		if char is not '\x00':
			diffblockdifference.append((index, char))

	patch_tuple = (diffblockdifference, diffblocklength, newdatalength, diff_tuple[0], diff_tuple[2])

	patchfile = open(patchfilename,'w')
	cPickle.dump(patch_tuple, patchfile, 1)
	patchfile.close()

	print 'Done. Patch file > ' + patchfilename

if __name__ == '__main__':
	#print sys.argv[1]
	try:
		opts, args = getopt.getopt(sys.argv[1:],'o:n:p:')
	except getopt.GetoptError:
		print "usage - python makepatch.py -o oldfile -n newfile -p patchfilename"
		exit()
	
	oldfile = None
	newfile = None
	patchfilename = None
	for opt, arg in opts:
		if opt == '-o':
			oldfile = arg
		elif opt == '-n':
			newfile = arg
		elif opt == '-p':
			patchfilename = arg
	
	if oldfile is None or newfile is None:
		print "usage - python makepatch.py -o oldfile -n newfile -p patchfilename"
		exit()
	elif patchfilename is None:
		patchfilename = 'patch'

	make(oldfile, newfile, patchfilename)
