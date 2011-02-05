import cPickle
import bsdiff

def makePatch(oldfilename, newfilename, patchfilename='patch'):
	if oldfilename is None or newfilename is None:
		raise BSDiffXException('Invalid oldfile or newfile')	
	try:
		oldfile = open(oldfilename)
		olddata = oldfile.read()
		oldfile.close()
	except IOError:
		raise BSDiffXException('Invalid oldfile')	

	try:
		newfile = open(newfilename)
		newdata = newfile.read()
		newfile.close()
	except IOError:
		raise BSDiffXException('Invalid newfile')	
		
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

def applyPatch(oldfilename, patchfilename, resultfilename='result'):
	if oldfilename is None or patchfilename is None:
		raise BSDiffXException('oldfilename or pathcfilename not defined')
	try:
		patchfile = open(patchfilename)
		patch_tuple = cPickle.load(patchfile)
		patchfile.close()
	except IOError:
		raise BSDiffXException('invalid patch file')

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

	try:
		oldfile = open(oldfilename)
		olddata = oldfile.read()
		oldfile.close()
	except IOError:
		raise BSDiffXException('invalid old file')

	patcheddata = bsdiff.Patch(olddata, newdatalength, controltuples, diffblock, extrablock)

	resultfile = open(resultfilename,'w')
	resultfile.write(patcheddata)
	resultfile.close()

class BSDiffXException(Exception):
	pass
