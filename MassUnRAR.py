from shutil import *
import os.path
import os
from sys import platform
import subprocess


def is_valid_path(path):
	if os.path.isdir(str(path)):
		print("\nPath given is valid\n")
		return True
	else:
		print("\nPath given is NOT valid\n")
		return False

def contains_ext(filenames):
	for file in filenames:
		if file[-len(fileTypeToCheckFor):].lower() == fileTypeToCheckFor.lower():
			# The above allows me to be dynamic to ensure that the extension being looked for will match whatever is put in, with or without the "."
			return file
			# return on the first find, doing so stops scanning the rest of the directory
			
def scan_directories(path):
	listOfMatchingFiles = []
	for dirname, dirnames, filenames in os.walk(path):
		if contains_ext(filenames):
			file = contains_ext(filenames)
			#print(dirname)
			#print(filenames)		# This just prints a list of all the filenames in the directory
			#for subdirname in dirnames:
			#print ((os.path.join(dirname, file)))
			listOfMatchingFiles.append(os.path.join(dirname, file))
	return listOfMatchingFiles

def extract_files(listOfFiles, directoryToExtractTo):
	# Check what platform this is running on and set the unRAR location accordingly
	# unRAR can be downloaded as part of WinRAR from http://www.rarlab.com/download.htm
	if platform.startswith('darwin'):
		# Looks for the unrar executable in the path that the script is being run from.
		unrarLocation = "./unrar"
		
		# Used this to call unrar initially. Had problems using this on Windows, hence the switch to subprocess
		# os.system("\'{0}\' x \"{1}\" \"{2}\"".format(unrarLocation, fileToExtract, directoryToExtractTo)) 
		
	elif platform.startswith('win32'):
		# Default location of WinRAR 4.20 install on x64 systems
		unrarLocation = "C:\\Program Files\\WinRAR\\unRAR.exe"
	amountOfFilesExtracted = 0
	for fileToExtract in listOfFiles:
		subprocess.call([unrarLocation, "x", fileToExtract, directoryToExtractTo])
		amountOfFilesExtracted +=1
	print("The amount of archives extracted out of: {}".format(amountOfFilesExtracted))
	
def add_Last_Slash(pathToAlter):
	if platform.startswith('darwin'):
		return pathToAlter + "/"
	elif platform.startswith('win32'):
		return pathToAlter + "\\"


######################################################################################################################################


# Makes input work between 2.x and 3.x
try: input = raw_input
except NameError: pass


# This is customisble, but it's mainly for RARs
fileTypeToCheckFor = ".rar" #input('Enter the extention to look for:')


locationToScan = input('Location to scan:')

if is_valid_path(locationToScan):
	extractPath =  input('Location to extract to:')
	
	# If the extractPath doesn't have a backslash at the end, add one otherwise it'll fail to extact
	if  extractPath.endswith(("\\", "/")):
		print("Good to go!")
	else:
		print("Extract path doesn't contain a slash on the end, I'll add one for you!")
		extractPath = add_Last_Slash(extractPath)
		print(extractPath)
		#scan_directories(x)
	listOfItemsToBeExtracted = scan_directories(locationToScan)
	print("List of items found \n")
	
	if listOfItemsToBeExtracted:
		print(listOfItemsToBeExtracted)
		extract_files(listOfItemsToBeExtracted, extractPath)
