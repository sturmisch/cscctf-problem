#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <dlfcn.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>

const char sc[] = "H\x89\xfcH1\xc0H1\xdbH1\xc9H1\xd2H1\xffH1\xf6H1\xedM1\xc0M1\xc9M1\xd2M1\xdbM1\xe4M1\xedM1\xf6M1\xff";
const unsigned int sc_len = 48;

void init_seccomp()
{
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
	seccomp_load(ctx);
}

void init()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(5);
}

void error(const char *msg,int code)
{
	puts(msg);
	exit(code);
}

int main()
{
	init();
	void *handle;
	char *rwx, *rw;
	int fd;

	if(!(handle = dlopen("/home/maps/libflag.so",RTLD_LAZY))) error("dlopen",1);

	if((fd = open("/dev/urandom",O_RDONLY)) < 0) error("open",2);
	if(read(fd,&rwx,8) < 0 || read(fd,&rw,8) < 0) error("read",3);
	close(fd);

	rwx = (char *)mmap((void *)(((size_t)(rwx)&~0xfff)%0x777700000000),0x1000,7,34,-1,0);
	rw = (char *)mmap((void *)(((size_t)(rw)&~0xfff)%0x777700000000),0x1000,3,34,-1,0);
	if(!rwx || !rw) error("mmap",4);
	memcpy(rwx,sc,sc_len);

	puts("Welcome!");
	puts("Your flag is hid inside libflag.so");
	puts("Let's see what your shellcode can do");
	printf("> ");
	read(0,rwx+sc_len,1000-sc_len);

	init_seccomp();
	(*(void(*)(void *))rwx)(rw+0x800);

	return 0;
}