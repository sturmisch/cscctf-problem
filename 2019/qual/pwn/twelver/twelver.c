#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>
#include <seccomp.h>

void initialization()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(10);
}

void setup_seccomp()
{
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(open),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
	seccomp_load(ctx);
}

void main()
{
	initialization();
	const char sc[] = "H1\xc0H1\xdbH1\xc9H1\xd2H1\xf6H1\xffH1\xedH1\xe4M1\xc0M1\xc9M1\xd2M1\xdbM1\xe4M1\xedM1\xf6M1\xff";
	char *rwx = mmap(0,0x1000,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
	memcpy(rwx,sc,0x30);

	write(1,"Shellcode > ",12);
	read(0,rwx+0x30,12);
	setup_seccomp();
	((void(*)(void))rwx)();
	exit(0);
}
