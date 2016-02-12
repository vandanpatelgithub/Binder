#include <string>
#include "codearray.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <vector>
#include <sys/stat.h>
#include <sys/types.h>
#include <iostream>
#include <fstream>

using namespace std;

int main()
{

	/* The child process id */
	pid_t childProcId = -1;

	/* Go through the binaries */
	for(int progCount = 0; 	progCount < NUM_BINARIES; ++progCount)
	{

		FILE *fp;

		//template of the temperory file where Xs would be replace by unique random letters and numbers
		char template_name[] = "/tmp/cmguiXXXXXX";

		int temp_fd;

		//creates a temperoryfile
		temp_fd = mkstemp(template_name);

		//On error, -1 is returned
		if(temp_fd == -1)
		{
			fprintf(stderr, "Temp file didn't get created !");
			perror("mkstemp");
			exit(-1);
		}

		// Opens the temperory file
		fp = fdopen(temp_fd, "w");

		// if file can't be opened, throws an error and exit abnormally
		if(!fp)
		{
			perror("fopen");
			exit(-1);
		}

	 //Write the bytes of the program to the file
	 fwrite(codeArray[progCount], sizeof(char), programLengths[progCount],fp);
	 if(ferror(fp))
		{
			perror("fwrite");
			exit(-1);
		}

		fclose(fp);


		//Make the file executable
		if(chmod(template_name, 0777) < 0)
		{
			perror("chmod");
			exit(-1);
		}


		//Create a child process using fork
		childProcId = fork();

		// Turns the child process into the executable
		if(childProcId == 0)
		{
			// Turns the child process into the process running the program in the above file
			if(execlp(template_name, template_name, NULL) < 0)
			{
				perror("execlp");
				exit(-1);
			}

		}
	}

	/* Wait for all programs to finish */
	for(int progCount = 0; progCount < NUM_BINARIES; ++progCount)
	{
		/* Wait for one of the programs to finish */
		if(wait(NULL) < 0)
		{
			perror("wait");
			exit(-1);
		}
	}
}
