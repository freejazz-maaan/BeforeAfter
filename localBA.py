import os, os.path, shutil, sys, time, datetime, shutil, glob, re, tkMessageBox, tempfile, dominate
from dominate.tags import *


#to do: add counters for the image groups

#get the image folder from standard input
#check that it is a directory, and that it contains our SOURCE jp(e)g
#exit if not a folder or no jp(e)g found
if os.path.isdir(sys.argv[1]) == True:
	workingDir = sys.argv[1]
else:
	print "I only like folders."
	sys.exit()
dirtyroots = glob.glob(os.path.join(workingDir, '*.jpg'))
dirtyroots.extend(glob.glob(os.path.join(workingDir, '*.jpeg')))
if len(dirtyroots) == 0:
	print "I need some original JPGs!"
	sys.exit()

#Creates a list of filenames without the full path (useful for labels)
def clean(each):
	name = os.path.basename(each)
	name = name.split("_v")[0]
	return name
#for every file - add it to a dictionary with basename:fullpath
#first we lookup in the dictionary if basename exists. if basename exists, append file to list
#sort the list so we have our original (v1, v2, v3)
masterDict = {}
for each in dirtyroots:
	if clean(each) in masterDict:
		masterDict[clean(each)].append(os.path.basename(each))
	else:
		fileList = []
		fileList.append(os.path.basename(each))
		masterDict[clean(each)] = fileList

for each in masterDict:
	masterDict[each].sort()
	print "\n"

#for each key in masterDict, lets make a gif of it's constituent members
#we start by making a string for the constituent files that will be passed to imagemagick
#then we use a system to call to run the imagemagick convert executable on our images.
totalGroupCount = len(masterDict)
imageList= ""
groupCount=0
for each in masterDict:
	groupCount=groupCount+1
	listy = masterDict[each]
	for image in listy:
		os.system("""convert %s -resize 1000x1000 %s""" % (image, image))
		os.system("""convert %s -background white -gravity center -extent 1000x1020 %s""" % (image, image))
		os.system("""convert %s  -gravity North -splice 0x18 -annotate +0+2 "%s/%s" -font Helvetica-Bold %s""" % (image, groupCount,totalGroupCount, image))
		os.system("""convert %s  -gravity South -splice 0x18 -annotate +0+2 "%s" -font Helvetica-Bold %s""" % (image, image, image))
	

f1 = open('testfile.html', 'w')
import dominate
from dominate.tags import *

doc = dominate.document(title='LOCAL COLOR')

with doc.head:
    link(rel='stylesheet', href='style.css')
    script(type='text/javascript', src='script.js')
    script(type='text/javascript', src='http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js')
    script(type='text/javascript', src='http://malsup.github.io/jquery.cycle2.js')
    script(type='text/javascript', src='http://malsup.github.io/jquery.cycle2.scrollVert.js')
    script(type='text/javascript', src='http://malsup.github.io/jquery.cycle2.tile.js')
    script(type='text/javascript', src='http://malsup.github.io/jquery.cycle2.center.js')

# outerSlideShowDiv = div(cls='cycle-slideshow', id='slideshow')
# outerSlideShowDiv['data-cycle-fx']="none"
# outerSlideShowDiv['data-cycle-loop']="0"
# outerSlideShowDiv['data-cycle-allow-wrap']="true"
# outerSlideShowDiv['data-cycle-slides']="> div"
# outerSlideShowDiv['data-cycle-timeout']="0"
# outerSlideShowDiv['data-cycle-prev']="#prev"
# outerSlideShowDiv['data-cycle-next']="#next"




def innerSlideShowDiv():
	divVar= div(cls='cycle-slideshow', id='inner-slideshow')
	divVar['data-cycle-fx']="none"
	divVar['data-cycle-loop']="0"
	divVar['data-cycle-center-horz']="true"
	divVar['data-cycle-timeout']="2500"
	return divVar


with doc:
	h1("LOCAL COLOR")
	p("Comparison Page")
	p("Bonobos Test Round")
	outerSlideShowDiv = div(cls='cycle-slideshow', id='slideshow')
	outerSlideShowDiv['data-cycle-fx']="none"
	outerSlideShowDiv['data-cycle-loop']="0"
	outerSlideShowDiv['data-cycle-allow-wrap']="true"
	outerSlideShowDiv['data-cycle-slides']="> div"
	outerSlideShowDiv['data-cycle-timeout']="0"
	outerSlideShowDiv['data-cycle-prev']="#prev"
	outerSlideShowDiv['data-cycle-next']="#next"
	with outerSlideShowDiv:
		for i in masterDict:
			with div():
				subDiv = innerSlideShowDiv()
				with subDiv:
					for each in masterDict[i]:
						img(a(each, href='/%s.html' % each), src=each, cls="displayed")
	with div(cls="center"):
		span("<<prev",id = "prev")
		span("next>>", id = "next" )



docString = str(doc)
f1.write(docString)
