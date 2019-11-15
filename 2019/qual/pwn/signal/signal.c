#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}

int main()
{
	char buf[0x100];
	const volatile unsigned long long ret = 0;
	init();
	read(0,buf,0x200);
	return ret;
}