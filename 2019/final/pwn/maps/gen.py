#!/usr/bin/python

import os, random, string

def rand_str(n):
	return ''.join(random.sample(string.ascii_letters+string.digits,n))

os.system("rm -f ./libflag.c 2>/dev/null")
flag = open("flag.txt",'r').read().strip()
flen = len(flag)-len("CCC{}")

code = """
#define _GNU_SOURCE
#include <stdio.h>

"""

x = random.randrange(13337)

for i in xrange(random.randrange(13337)):
	code += 'char *wrong_flag_{0}(){{ return "CCC{{{1}}}"; }}\n'.format(i,rand_str(flen))

code += 'char *correct_flag_13333337(){{ return "{0}"; }}\n'.format(flag)

for i in xrange(x,x+random.randrange(13337)):
	code += 'char *wrong_flag_{0}(){{ return "CCC{{{1}}}"; }}\n'.format(i,rand_str(flen))

open("libflag.c",'w').write(code)
os.system("gcc ./libflag.c -o ./libflag.so -fPIC -shared -ldl ")
