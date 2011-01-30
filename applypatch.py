import cPickle
import bsdiff
import sys
import getopt

def apply(oldfilename, resultfilename, patchfilename):
	patchfile = open(patchfilename)
	patch_tuple = cPickle.load(patchfile)
	patchfile.close()

	diffblockdifference = patch_tuple[0]
	diffblocklength = patch_tuple[1]
	newdatalength = patch_tuple[2]
	controltuples = patch_tuple[3]
	extrablock = patch_tuple[4]

	diffblocklist=[]
	for i in range(diffblocklength - len(diffblockdifference)):
		diffblocklist.append('\x00')
	
	for index, char in diffblockdifference:
		diffblocklist.insert(index, char)

	diffblock = ''.join(diffblocklist)

	oldfile = open(oldfilename)
	olddata = oldfile.read()
	oldfile.close()

	patcheddata = bsdiff.Patch(olddata, newdatalength, controltuples, diffblock, extrablock)

	resultfile = open(resultfilename,'w')
	resultfile.write(patcheddata)
	resultfile.close()

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:],'o:r:p:')
	except getopt.GetoptError:
		print "usage - python applypatch.py -o oldfile -r resultfile -p patchfilename"
		exit()
	
	oldfile = None
	resultfile = None
	patchfilename = None
	for opt, arg in opts:
		if opt == '-o':
			oldfile = arg
		elif opt == '-r':
			resultfile = arg
		elif opt == '-p':
			patchfilename = arg
	
	if oldfile is None or resultfile is None:
		print "usage - python applypatch.py -o oldfile -n resultfile -p patchfilename"
		exit()
	elif patchfilename is None:
		patchfilename = 'patch'

	apply(oldfile, resultfile, patchfilename)
