#!/usr/bin/python

from subprocess import check_output as co
import sys, os, requests, socket, json

def checkweb(port):
	r = requests.get("http://127.0.0.1:{:d}".format(port))
	return "good" if r.status_code == 200 else "bad"

def checktcp(port):
	s = socket.socket()
	s.connect(("127.0.0.1",port))
	sent = 0
	try:
	   sent = s.send("wtf\n")
	except:
	   s.close()
	finally:
	   s.close()
	return "good" if sent == 4 else "bad"

def check(challtype,port):
	return checkweb(port) if challtype == "web" else checktcp(port)

d = {
	"pwn": {
		"babystack": 1,
		"babyheap": 1,
		"signal": 1,
		"twelver": 1,
	},
	"web": {
		"flasklight": 1,
		"proveyouarenothuman": 1,
		"zlippery": 1,
	},
	"crypto": {
		"weakrandom": 1,
	}
}
basedir = os.getcwd()
challenges = {
	"babystack": "pwn",
	"signal": "pwn",
	"babyheap": "pwn",
	"twelver": "pwn",
	"weakrandom": "crypto",
	"flasklight": "web",
	"proveyouarenothuman": "web",
	"zlippery": "web",
}

if "docker" not in co(["/usr/bin/groups"]) and "root" not in co(["/usr/bin/whoami"]):
	print "If you're not root, please add \"docker\" to your group or use root/sudo for this script."
	sys.exit(-1)

for line in co(["/usr/bin/docker","ps","--format","{{.Image}}##{{.Ports}}##{{.Status}}"]).split('\n')[:-1]:
	chall, _, status = line.split("##")
	port = int(_.split("->")[0].split(':')[-1])
	if check(challenges[chall],port) == "bad":
		targetdir = basedir+"/{}/{}".format(challenges[chall],chall)
		os.chdir(targetdir)
		try:
			co(["/usr/bin/docker-compose","-f","./docker-compose.yml","down"])
			co(["/usr/bin/docker-compose","-f","./docker-compose.yml","up","--build","-d"])
		except:
			pass
		finally:
			os.chdir(basedir)
			d[challenges[chall]][chall] = 0
	else:
		d[challenges[chall]][chall] = 1
	
print json.dumps(d,indent=4,sort_keys=True)