#include <stdio.h>
#include <unistd.h>

size_t vuln()
{
	unsigned long long buf;
	return read(0,&buf,0x100);
}

int main()
{
	alarm(10);
	return (int)vuln();
}