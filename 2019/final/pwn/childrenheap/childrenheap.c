#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <unistd.h>

int sizes[0x10];
char *ptrs[0x10];

void error(const char *msg)
{
	puts(msg);
	exit(-1);
}

int read_int()
{
	char buf[0x10];
	return atoi(fgets(buf,0x10,stdin));
}

void init()
{
	mallopt(M_MXFAST,0);
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}

void allocate()
{
	printf("Index: ");
	int idx = read_int();
	if(idx < 0 || idx >= 16) error("Invalid index!");
	else if(ptrs[idx]) error("Index is already allocated!");
	printf("Size: ");
	int size = read_int();
	if(size < 0x10 || size > 0x100) error("Invalid size!");
	ptrs[idx] = (char *)malloc(size);
	sizes[idx] = size;
	printf("Content: ");
	ptrs[idx][read(0,ptrs[idx],size)-1] = 0;
}

void update()
{
	printf("Index: ");
	int idx = read_int();
	if(idx < 0 || idx >= 16) error("Invalid index!");
	else if(!ptrs[idx]) error("Index is not allocated!");
	printf("Content: ");
	ptrs[idx][read(0,ptrs[idx],sizes[idx])] = 0;
}

void show()
{
	printf("Index: ");
	int idx = read_int();
	if(idx < 0 || idx >= 16) error("Invalid index!");
	else if(!ptrs[idx]) error("Index is not allocated!");
	printf("Chunk %d's content: %.*s\n",idx,sizes[idx],ptrs[idx]);
}

void delete()
{
	printf("Index: ");
	int idx = read_int();
	if(idx < 0 || idx >= 16) error("Invalid index!");
	else if(!ptrs[idx]) error("Index is not allocated!");
	free(ptrs[idx]);
	ptrs[idx] = 0;
	sizes[idx] = 0;
}

int main()
{
	init();
	while(1)
	{
		puts("Children Heap");
		puts("=============");
		puts("1. Allocate");
		puts("2. Update");
		puts("3. Show");
		puts("4. Free");
		puts("5. Exit");
		printf(">> ");
		switch(read_int())
		{
			case 1:
				allocate();
				break;
			case 2:
				update();
				break;
			case 3:
				show();
				break;
			case 4:
				delete();
				break;
			case 5:
				puts("Bye!");
				exit(0);
			default:
				puts("Huh ?");
				exit(-1);
		}
	}
	return 0;
}