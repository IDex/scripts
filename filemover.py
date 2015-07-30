#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  filemover.py
#  
#  Copyright 2013 IDex <fuster94@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#Goal of this script is to move files from a temporary folder(tmpdir) to
#appropriate folders in (basedir) based on regexes found in (input) file

from os import listdir
import sys
import os
import re
import shutil

basedir = "/home/ide/Anime/"
tmpdir = "9tmp/flexd/"
curdir = os.path.dirname(sys.argv[0])# + "/"
folderlist = ""
filelist = ""
def listfiles():
	dirl = basedir+tmpdir
	files = listdir(dirl)
	return files
def regexfiles():
	stillfiles = False
	folderlist = ""
	filelist = ""
	files = listfiles()
	inputfile = open(curdir+"/input").read().splitlines()
	for i in inputfile:
		folderlist = ""
		filelist = ""
		for f in files:
			out = re.search(i, f, re.IGNORECASE)
			if out is not None:
				filelist = f
				break
		for u in findfolder():
			pout = re.search(i, u, re.IGNORECASE)
			if pout is not None:
				folderlist = u
				break
				
		if folderlist is not "" and filelist is not "":
			movefiles(filelist, folderlist)
			stillfiles = True
			
		#else: print("Folder/file pair was not found with regex %s" % i)
	if stillfiles:
		return True
	else:
		return False

def findfolder():
	folders = listdir(basedir)
	return folders
	
def movefiles(filelist, folderlist):
	print("File found: " + filelist + " with folder: " + folderlist)
	try:
    	        shutil.move(basedir+tmpdir+filelist, basedir+folderlist)
        except shutil.Error:
		print("File", filelist, "already exists in the destination folder.")
                try:
	                os.remove(basedir+tmpdir+filelist)
                except OSError:
                        pass

dirl = "/home/idex/Anime/9TMP/"
files = listfiles()
def main():
	check = True
	while check:
		check = regexfiles()
	print("No files left to move")
	return 0

if __name__ == '__main__':
	main()

