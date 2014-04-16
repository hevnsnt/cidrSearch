from netaddr import IPSet
import argparse
import re

#script, textfile, ipaddr = argv




#-------------------Get command line input----------------------------------
parser = argparse.ArgumentParser(description='Search for IP Inclusion through a large list of CIDR blocks', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', action='store_true', dest='verboseMode', help='Verbose mode will direct output to screen as well as logfile\n\n')
parser.add_argument('-f','--file', help='File with CIDR blocks', required=True, dest='infile')
parser.add_argument('ipaddr', action="store", help='IP Address to search')
#-------------------End command line input----------------------------------
#-------------------Init global vars----------------------------------
results = parser.parse_args()
infile = results.infile
verbose = results.verboseMode
ipaddr = results.ipaddr
infile = open(infile)
#-------------------Init global vars----------------------------------


def is_ipv4(ip):
	try:
		match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", ip)
		if not match:
			return False
		quad = []
		for number in match.groups():
			quad.append(int(number))
		if quad[0] < 1:
			return False
		for number in quad:
			if number > 255 or number < 0:
				return False
		return True
	except:
		return False

def loadSet(infile):
	cidrSet = set([])
	if verbose: print("[+] Loading CIDR blocks from %s" % results.infile)
	for line in infile:
		line = line.strip()
		cidrSet.add(line)
	cidrSet = IPSet(cidrSet)
	if verbose: print("[+] done")
	return cidrSet

if is_ipv4(ipaddr):
	#cidrSet = loadSet(infile)
	if ipaddr in loadSet(infile):
		print("%s exists in %s" % (ipaddr, results.infile))
	else:
		print("%s WAS NOT FOUND in %s" % (ipaddr, results.infile))
else:
	print("Please input a valid IP address to test")