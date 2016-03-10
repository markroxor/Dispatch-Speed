import subprocess

lowerIp = 2
UpperIp = 5
adapter = ""

def findIP():
	global adapter
	p = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err=p.communicate()

	out = out.split()
 	
 	adapter = out[0]

 	for word in out:
		if "addr:172.16." in word:
			return word[5:]

def getFreeIPs(size_):
	freeIPs = []
	k=(findIP()[:(-len(str(findIP().split(".")[-1])))])

	for i in xrange(2,255):
		
		if len(freeIPs)>=size_:
			break

		k+=str(i)

		p = subprocess.Popen(['ping',k,'-c','1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err=p.communicate()
		out = out.split()
		if i and out[-5]=="100%":
			print ("appending",k)
			freeIPs.append(k)

		k=k[:-len(str(i-1))]

	return freeIPs


def main(num=5):
	findIP()
	initCommand = "sudo ip addr flush dev "+adapter
	subprocess.Popen(initCommand.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
	print (initCommand)

	startCommand = "dispatch start "

	for freeIP in getFreeIPs(num):
		command = "sudo ip addr add "+freeIP+"/22 dev "+adapter
		print (command)
		subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		startCommand += freeIP+"@1 "

	subprocess.Popen(startCommand.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print startCommand

main(10)
#print (-len(str(findIP().split(".")[-1])))
# for i in {2..9}; do sudo ip addr add 172.16.185.$i/22 dev enp7s0; done
# for i in {2..9}; do export iplist="172.16.185.$i@1 $iplist"; done
# dispatch start $iplist
