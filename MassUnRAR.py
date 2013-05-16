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
	listOfHoldingDirectories = []
	for dirname, subdirnames, filenames in os.walk(path):
		if contains_ext(filenames):
			file = contains_ext(filenames)
			listOfHoldingDirectories.append(dirname)
			listOfMatchingFiles.append(os.path.join(dirname, file))
	return [listOfMatchingFiles,listOfHoldingDirectories]

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
	else:
		print("Sorry! You're running this on an unsupported platform. \nThis script doesn't support it. It's designed for OSX and Windows.")
	amountOfFilesExtracted = 0
	for fileToExtract in listOfFiles:
		subprocess.call([unrarLocation, "x", fileToExtract, directoryToExtractTo])
		amountOfFilesExtracted +=1
	print("The amount of archives extracted out of: {}".format(amountOfFilesExtracted))

# If the extract path lacks a slash at the end, the the extract will fail. This add a slash based on system
def add_Last_Slash(pathToAlter):
	if platform.startswith('darwin'):
		return pathToAlter + "/"
	elif platform.startswith('win32'):
		return pathToAlter + "\\"

def delete_source_data(listOfData):
	for folder in listOfData:
		rmtree(folder,True)
		print("Deleted: {}".format(folder))
	

		

######################################################################################################################################


# Makes input work between 2.x and 3.x
try: input = raw_input
except NameError: pass


# This is customisble, but it's mainly for RARs
fileTypeToCheckFor = ".rar" #input('Enter the extention to look for:')

# Using the os.path.expanduser allows to account for the use of ~/ on OSX as this otherwise failed the valid path check. It also needs to be done on the extract path, as otherwise it will extract the wrong directory.
locationToScan = os.path.expanduser(input('Location to scan:'))


if is_valid_path(locationToScan):
	# Check to see if the source data should be deleted
	loopCondition = True
	while loopCondition:
		deleteSource = input("Delete source files? [Y/N]:")
		if deleteSource.lower() == 'y':
			deleteSource = True
			print("Ok, the source files will be deleted.\n")
			loopCondition = False
		elif deleteSource.lower() == 'n':
			deleteSource = False
			print("Source files will NOT be deleted.\n")
			loopCondition = False
		else:
			print("You have not entered a correct value. Please either either a Y or N\n")
	
	extractPath = os.path.expanduser(input('Location to extract to:'))
	# If no value is entered for the extract path, the extracts would be placed in the script's location
	if extractPath =='':
		print("Extract path was not entered. Will output to the source path.")
		extractPath = locationToScan
		extractPath = add_Last_Slash(extractPath)
	elif extractPath.endswith(("\\", "/")):
		# If the extractPath doesn't have a backslash at the end, add one otherwise it'll fail to extact
		print("Good to go!")
	else:
		print("Extract path doesn't contain a slash on the end, I'll add one for you!")
		extractPath = add_Last_Slash(extractPath)
		print(extractPath)
		
	listOfItemsToBeExtracted = scan_directories(locationToScan)[0]
	listOfFoldersToDelete = scan_directories(locationToScan)[1]

	if listOfItemsToBeExtracted:
		print("\nList of {} items found:".format(len(listOfItemsToBeExtracted)))
		print(listOfItemsToBeExtracted)
		extract_files(listOfItemsToBeExtracted, extractPath)
		if deleteSource:
			print("\nList of {} folders to delete:".format(len(listOfFoldersToDelete)))
			print(listOfFoldersToDelete)
			delete_source_data (listOfFoldersToDelete)
