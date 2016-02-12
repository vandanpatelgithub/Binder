import os
import sys
from subprocess import call
import os
from subprocess import Popen, PIPE

# The file name
FILE_NAME = "codearray.h";

###########################################################
# Returns the hexidecimal dump of a particular binary file
# @execPath - the executable path
# @return - returns the hexidecimal string representing
# the bytes of the program. The string has format:
# byte1,byte2,byte3....byten,
# For example, 0x19,0x12,0x45,0xda,
##########################################################
def getHexDump(execPath):

	# The return value
	retVal = None

	# Run the process
	process = Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', execPath], stdout=PIPE)

	# Grab the stdout and stderr streams
	(output,err) = process.communicate()

	# Wait for the process to finish and get the exit code
	exit_code = process.wait()

	# If there is no error, then return the output
	if exit_code == 0:

		retVal = output

	# TODO:
	# 1. Use popen() in order to run hexdump and grab the hexadecimal bytes of the program.
	# 2. If hexdump ran successfully, return the string retrieved. Otherwise, return None.
	# The command for hexdump to return the list of bytes in the program in C++ byte format
	# the command is hexdump -v -e '"0x" 1/1 "%02X" ","' progName

	return retVal

###################################################################
# Generates the header file containing an array of executable codes
# @param execList - the list of executables
# @param fileName - the header file to which to write data
###################################################################

def generateHeaderFile(execList, fileName):


	# The header file
	headerFile = None

	# The program array
	progNames = sys.argv

	# Open the header file
	headerFile = open(fileName, "w")

	# The program index
	progCount = 0

	# The lengths of programs
	progLens = []

	# Write the array name to the header file
	headerFile.write("#include <string>\n\nusing namespace std;\n\nunsigned char* codeArray["+ str(len(execList)) +"] = {");

	for progName in execList:

		# Count the program
		progCount += 1

		print("Generating hexdump of ", progName)

		# Generate the hex code
		hexCode = getHexDump(progName)

		print("Done!")

		#Failed to get the hex dump for the program
		if not hexCode:

			print("Invalid path for program " + progName)

			# Close the file
			headerFile.close()

			os.remove(FILE_NAME)

			# Exit abnormally
			exit(1)

		# Remove the last comma
		if len(hexCode) > 0:
			hexCode = hexCode.decode("utf-8").rstrip(",")

		# Get the program lengths
		programLength = len(hexCode.split(","))

		progLens.append(str(programLength))

		headerFile.write("new unsigned char[" + str(programLength) + "]{" + hexCode + "}")

		# if this is the last element, insert closing "}"
		if progCount == len(execList):
			headerFile.write("};")

		else:
			#Add the ","
			headerFile.write(",")



	# Add array to containing program lengths to the header file
	headerFile.write("\n\nunsigned programLengths["+ str(len(progLens))  +"] = {")

	# The number of programs
	numProgs = 0

	if len(progLens) > 1:
		for length in progLens[:-1]:
			headerFile.write(length + ", ")
		headerFile.write(progLens[-1])

	else:
		for length in progLens:
			headerFile.write(length)

	headerFile.write("};")

	headerFile.write("\n\n#define NUM_BINARIES " +  str(len(progNames) - 1))

	headerFile.close()

############################################################
# Compiles the combined binaries
# @param binderCppFileName - the name of the C++ binder file
# @param execName - the executable file name
############################################################

def compileFile(binderCppFileName, execName):

	print("Compiling...")

	process = Popen(["g++", binderCppFileName, "-o", execName, "-std=gnu++11"], stdout=PIPE)

	# Grab the stdout and the stderr streams
	(output, err) = process.communicate()

	exit_code = process.wait()

	if exit_code == 0:
		print("Compilation Succeded!")

	else:
		print("Compilation Failed !")
		print(err)

generateHeaderFile(sys.argv[1:], FILE_NAME)
compileFile("binderbackend.cpp", "bound")
