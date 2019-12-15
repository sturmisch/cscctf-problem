#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>

int ____[]= { 181,152,159,165,206,137,159,150,202,136,203,144,138,159,179,144,206,135,144,159,169,144,142,202,155,147,203,140,159,170,150,205,139,159,149,201,159,206,144,203 };

void __attribute__((constructor)) isDebuggerPresent()
{
	if(ptrace(PTRACE_TRACEME,0,0,0) == -1)
	{
		puts("Kamu hek hek nanti saya pukul!");
		exit(-1);
	}
}

int my_strlen(const char *string)
{
	int i = -1;
	while(string[++i]);
	return i;
}

char checkpassword(const char *string)
{
	if(my_strlen(string) != 40) return 1;
	for(int i=0,c=0;i<40;i++)
	{
		c = ((string[i] ^ 0x7f) & 0xff) + 0x7f;
		if(c != ____[i]) return 1;
	}
	return 0;
}

int main(int argc, char **argv)
{
	if(argc != 2) printf("Usage: %s [password]\n",argv[0]);
	else
	{
		if(checkpassword(argv[1])) puts("Try again.");
		else printf("Congrats, your flag is CCC{%s}\n",argv[1]);
	}
	return 0;
}