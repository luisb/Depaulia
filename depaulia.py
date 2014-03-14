#!/usr/bin/python
import sys, re
import elementtree.ElementTree as ET

if len(sys.argv) == 1:
  print "FATAL: depaulia.py expects to be passed at least one METS file."
  print "usage: depaulia.py file [file]..."
  sys.exit()

for File in sys.argv:
  if File == __file__:
    continue
    
  tree = ET.parse(File)
  root = tree.getroot()
  
  idmap = dict()
  
  try:
    register_namespace = ET.register_namespace
  except AttributeError:
    def register_namespace(prefix, uri):
      ET._namespace_map[uri] = prefix

  # register namespaces to preserve qualified names on output
  register_namespace('mets', "http://www.loc.gov/METS/")
  register_namespace('mods', "http://www.loc.gov/mods/v3")
  register_namespace('mix', "http://www.loc.gov/mix/v20")
  register_namespace('premis', "info:lc/xmlns/premis-v2")
  register_namespace('xlink', "http://www.w3.org/1999/xlink")
  register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")  
  
#  # Make sure the mets type attribute is "Newspaper"
#  for mets in root.getiterator('{http://www.loc.gov/METS/}mets'):
#    if mets.attrib['TYPE'] != 'Newspaper':
#      mets.attrib['TYPE'] = 'Newspaper'

  # Veridian cares about servicefile and doesn't about masterfile.
  # use servicefile instead of masterfile

  # loop through fileSec file elements
  for fileSec in root.getiterator('{http://www.loc.gov/METS/}fileSec'):
    for fileGrp in fileSec:
      for file in fileGrp:
        # change masterFile to serviceFile
        file.attrib['ID'] = re.sub('masterFile', 'serviceFile', file.attrib['ID'])

  # loop through structMap divs
  for div in root.getiterator('{http://www.loc.gov/METS/}div'):
    # we're interested in the "pages"
    if div.attrib['TYPE'] == 'np:page':
      
      # add page number (ORDER) as new attrib ORDERLABEL
      #div.attrib['ORDERLABEL'] = div.attrib['ORDER']
      
      # we know there are three files and they are ordered 
      # service, ocr, text
      fptr_count = 0
      # loop through fptrs of this page
      for fptr in div:
        fptr_count = fptr_count + 1
        fptr.attrib['FILEID'] = re.sub('masterFile', 'serviceFile', fptr.attrib['FILEID']) 
 
  new_File = "METS.xml"
  tree.write(new_File)

  with open("METS.xml", "a") as metsFile:
    metsFile.write("\n")

