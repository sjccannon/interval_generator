#this script generates a separate file for each refseq_mrna submitted via csv file,amalgamets them into one then moves them to a separate directory
from bioservices import *
from lxml import etree
import wget, os, sys, csv, glob, shutil

s=BioMart()

#adding the required dataset to xml generator
s.add_dataset_to_xml('hsapiens_gene_ensembl')

#adding required attributes to xml generator
s.add_attribute_to_xml("chromosome_name")
s.add_attribute_to_xml("exon_chrom_start")
s.add_attribute_to_xml("exon_chrom_end")
s.add_attribute_to_xml("strand")
s.add_attribute_to_xml("external_gene_name")
s.add_attribute_to_xml("rank")

#do you have a csv file (y/n)?

#if y print request for pathway
#take pathway as variable 

#this takes column 0 and changes it into a list of strings however the xml generator 
#does not generate an xml for each filter but chucks all refseqs in at once. I will therefore loop through the rows as below

#opening the csv file required
f=open('refseq.csv')

#reading the csv file
csv_f = csv.reader(f)

for row in csv_f:
	s.add_filter_to_xml("refseq_mrna", (row[0]))
	xml = s.get_xml()
	res = s.query(xml)
	print res
	parser = etree.XMLParser(remove_blank_text=True)
	elem = etree.XML(xml, parser)
	xml_string = etree.tostring(elem)
	url = 'http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query>' + xml_string
	wget.download(url)
	os.rename('martservice', (row[0]))	
	
#combines multiple text files

rf = glob.glob("NM_*")
with open("generated_intervals.txt", "wb") as outfile:
	for f in rf:
		with open(f, "rb") as infile:
			outfile.write(infile.read())



source = '/mnt/Data4/working_directory/stuart/python-2-7_env/scripts/interval_generator/bioservices'
dest = '/mnt/Data4/working_directory/stuart/python-2-7_env/scripts/interval_generator/bioservices/individual_intervals'

files  = os.listdir(source)

for ints in files:
	if (ints.startswith("NM")):
		shutil.move(ints, dest)
		

#storing the NM numbers as an array to then use each to rename a file


#create an array of header names which could be included in each file
