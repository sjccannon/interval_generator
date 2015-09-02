#this script generates an interval file for each refseq_mrna included in the .csv file submitted. 
#It prints each to screen, stores each in a separate file (if they do not already exist there) and finally,
#creates a master document containing each 

#importing all modules from bioservices, etree the xml parser and other python modules
from bioservices import *
from lxml import etree
from array import *
import os, os.path, sys, csv, glob, shutil
import wget

#assigning the biomart module to a variable
s=BioMart()

#adding the required dataset to xml generator
s.add_dataset_to_xml('hsapiens_gene_ensembl') 
sys.exit

#adding required attributes to xml generator
s.add_attribute_to_xml("chromosome_name")
s.add_attribute_to_xml("exon_chrom_start")
s.add_attribute_to_xml("exon_chrom_end")
#s.add_attribute_to_xml("strand")
s.add_attribute_to_xml("external_gene_name")
s.add_attribute_to_xml("rank")

#opening the csv file required
f=open('refseq.csv')

#reading the csv file and assigning to variable
csv_f = csv.reader(f)

#looping through the csv by row
for row in csv_f:

#adds the string in csv as a filter 
	s.add_filter_to_xml("refseq_mrna", (row[0]))
#generates and xml query based on the filters and attributes submitted
	xml = s.get_xml()
#assigns the results of the xml query to a variable which can easily be printed to the terminal
	res = s.query(xml)
#print results from the bioservices query  to terminal
	print res
#specifying how to parse the xml file
	parser = etree.XMLParser(remove_blank_text=True)
#parsing the xml file	
	elem = etree.XML(xml, parser)
#turning parsed xml into single string now with no blank text	
	xml_string = etree.tostring(elem)
#concatenating the  data  destination url, an xml header and the parsed xml string for the target mart service
	url = 'http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query>' + xml_string
#using wget to download the requested attributes based on refseq filter
	wget.download(url)
#rename each downloaded file 'martservice' as the refseq_mrna string used as the filter
	os.rename('martservice', (row[0]))	
	
#this takes all the individual interval files and combines into one file. This file is over written each time the program is run
rf = glob.glob("NM_*")
with open("generated_intervals.txt", "wb") as outfile:
	for f in rf:
		with open(f, "rb") as infile:
			outfile.write(infile.read())

#this moves the generated interval files to their own directory for local reference
#If the files are already present in the destination directory they are not moved and deleted instead. 

source = '/mnt/Data4/working_directory/stuart/python-2-7-10/scripts/interval_generator/bioservices'
dest = '/mnt/Data4/working_directory/stuart/python-2-7-10/scripts/interval_generator/bioservices/individual_intervals'
files  = os.listdir(source)
for ints in files:
	if ints.startswith("NM"): 
		current_file = ints
		if os.path.exists(dest + "/" + current_file) == False:
			shutil.move(current_file, dest)
		else:
			 os.remove(current_file)

#this creates a bed format file from the generated interval file, in this way there is extra information stored locally for each refseq_mrna  
infile = "generated_intervals.txt"
outfile = "generated_intervals.bed"		
with open(infile) as in_f, open(outfile, "w") as out_f:
	for row in in_f:
		#returning a list of the words from the string
		column = row.split()
		for element in column:
			del column[3:5]
			element = '	'.join(column)		
		out_f.write(element + '\n')	
#		out_f.write(column[0] + ' ' + column[1] + ' ' + column[2] + '\n')

os.remove(infile)
