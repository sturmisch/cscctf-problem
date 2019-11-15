#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char *chunks[16];
unsigned int sizes[16];

void init()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}

int get_int()
{
	char buf[16];
	return atoi(fgets(buf,16,stdin));
}

void create()
{
	printf("Index: ");
	int idx = get_int();
	if(idx < 0 || idx > 15) puts("Invalid index!");
	else if(chunks[idx]) puts("That index is already allocated!");
	else
	{
		printf("Size: ");
		if((sizes[idx] = (unsigned int)get_int()) > 0x100) puts("Invalid size!");
		else
		{
			chunks[idx] = (char *)malloc(sizes[idx]);
			printf("Content: ");
			chunks[idx][read(0,chunks[idx],sizes[idx])] = 0;
			puts("Chunk created!");
		}
	}
}

void delete()
{
	printf("Index: ");
	int idx = get_int();
	if(idx < 0 || idx > 15) puts("Invalid index!");
	else if(!chunks[idx]) puts("That index is not allocated!");
	else
	{
		free(chunks[idx]);
		sizes[idx] = 0;
		chunks[idx] = 0;
		puts("Chunk deleted!");
	}
}

void show()
{
	printf("Index: ");
	int idx = get_int();
	if(idx < 0 || idx > 15) puts("Invalid index!");
	else if(!chunks[idx]) puts("That index is not allocated!");
	else printf("Chunk's content: %.*s\n",sizes[idx],chunks[idx]);
}

void menu()
{
	puts("Welcome to babyheap!");
	puts("====================");
	puts("1. Create");
	puts("2. Delete");
	puts("3. Show");
	puts("4. Exit");
}

int main()
{
	int choice;
	init();
	menu();
	while(1)
	{
		printf(">> ");
		switch((choice = get_int()))
		{
			case 1:
				create();
				break;
			case 2:
				delete();
				break;
			case 3:
				show();
				break;
			case 4:
				puts("bye bye!");
				exit(0);
				break;
			default:
				puts("Invalid choice!");
				break;
		}
	}
	return 0;
}