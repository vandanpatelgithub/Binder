Assignment 1, CS-456, Fall 2015
Due Date: 11/26/2015 at 11:59 pm

Group Members:
	- Diego M. Perilla (Diego.Perilla@csu.fullerton.edu)
	- Vandankumar Patel (vandan@csu.fullerton.edu)
	- Maria Villa (ganymede527@gmail.com)

Node Info:
  - Domain: opal.ecs.fullerton.edu
  - Username: cs2
  - Password: hepivtypmy

- The /B flag of the copy command treats the file as binary, and copies them byte for byte instead of the default behavior which
  treats them as lines of text with end-of-file and end-of-line characters.

- The behavior here depends on the program we use to open the file. if we are using the 7z to open a compressed file, it
  will keep looking for .7z content in the file until it reaches the end. However, when we try and open .gif file, the
  program expect to see .gif content inside it. If they find something that is not .gif in the beginning of the file,
  they would consider it as a corrupt file.

- Hiding Malicious Codes

  - You can put some malicious code inside your .7z file with a legit .7z content (worm.bat). When you try and open that file
    with 7z, 7z would ignore the part which is not .7z, and would only show you legit .7z content. So you won't even notice
    that there was something else (malicious code) in this file, in addition to these legit .7z content. In this case, you can
    put malicious code anywhere in the file, since 7z program would scan the whole file until it finds the legit .7z content.

  - You can achieve the above stealth with .gif file as well. But you have to be careful about where you place your malicious
    code in this case. If you place something which is not .gif (malicious code) in the beginning of the file, the program would
    consider the whole file as corrupted. However, if you put .gif content in the beginning, and then the malicious code, it won't
    complain.

- How robust is this technique in terms of avoiding detection by anti-virus tools?

  - The robustness would totally depend on how widespread this technique is. In other words, how often it is used. If this technique
    is there for a while, and many systems have been infected by it, it would get the eyes of the anti-virus companies. They would
    update their software and employ the detection mechanism that detect the binders. To avoid detection by anti-virus tools, you
    either have to search in hacking forums or make one by yourself.

** No extra credit was completed for this assignment. **
