#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(15);
}

void main()
{
	char buf[0x100];
	init();
	for(int i=0;i<3;i++) printf(fgets(buf,0x100,stdin));
	exit(0);
}