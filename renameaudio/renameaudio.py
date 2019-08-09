#!/usr/bin/env python

import audio_metadata
import os
from os import listdir
from os.path import isfile, join, isdir
import re
import sys
import argparse


parser = argparse.ArgumentParser(description='Rename audio files to add or remove bpm and key metadata')
parser.add_argument('-r', '--remove', action='store_true', required=False)
args = parser.parse_args()

def sortfile(filename, bpm, key, path):
	bpmint = int(re.search(r'\d+', bpm).group())
	formattedbpm = format(bpmint, '03d')
	prefix = formattedbpm + " " + key

	if filename.startswith(prefix + " "):
		if args.remove:
			filenamenoprefix = filename[len(prefix + " "):]
			os.rename(join(path, filename), join(path, filenamenoprefix))
		else:
			print("File already tagged: ", filename)
		return

	if not args.remove:
		newfilename = prefix + " " + filename
		#print(formattedbpm, key, filename)
		#print(newfilename)
		os.rename(join(path, filename), join(path, newfilename))

def getAllFilesInDirAndSubdirs(mypath):


	#mypath = os.getcwd()

	#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	onlyfiles = [(f, mypath) for f in listdir(mypath) if isfile(join(mypath, f))]
	onlyfolders = [f for f in listdir(mypath) if isdir(join(mypath, f))]

	if len(onlyfolders) > 0:
		subfolderfiles = []
		for folder in onlyfolders:
			subfolderfiles = subfolderfiles + getAllFilesInDirAndSubdirs(join(mypath, folder))

		onlyfiles = onlyfiles + subfolderfiles
	return onlyfiles

files = getAllFilesInDirAndSubdirs(os.getcwd())

for (f, path) in files:
	#print("Working on file: ", f)
	try:
		#print("Getting metadata")
		metadata = audio_metadata.load(join(path,f))
		#print("Got metadata")
	except audio_metadata.exceptions.UnsupportedFormat:
		print("Unsupported Format: ", join(path, f))
		continue
	except audio_metadata.exceptions.InvalidHeader:
		print("InvalidHeader: ", join(path, f))
		continue
	except:
		print("No clue: ", join(path, f))
		continue
		#raise
	else:
		try:
			#print("HERE")
			tags = metadata['tags']
			bpm = tags['bpm'][0]
			key = tags['TKEY'][0]
			#print("Got tags")
			#print(bpm)
			#print(bpm)
			sortfile(f, bpm, key, path)
		except:
			print("Error retrieving tags: ", join(path, f))
			continue
