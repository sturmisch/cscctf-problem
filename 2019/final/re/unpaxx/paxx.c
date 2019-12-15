#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <elf.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>

#define XOR_MAGIC 0xa5
#define ELF_BASE 0x400000

typedef struct Elf64_offset
{
	char *name;
	uint section;
	Elf64_Off offset;
	Elf64_Xword size;
} Elf64_Offset;

int pack_ELF(const char *path)
{
	int rfd = open(path,O_RDONLY);
	if(rfd < 0) return -1;
	int len = strlen(path);
	char *paxx = calloc(len+0x10,sizeof(char));
	strncat(paxx,path,len);
	strncat(paxx,".packed",8);

	struct stat s = {0}, ssc = {0};

	stat(path,&s);
	char *elf = calloc(s.st_size+0x10,sizeof(char));
	char *p = 0, *sc = 0;

	read(rfd,elf,s.st_size);
	close(rfd);


	Elf64_Ehdr eheader = {0};
	memcpy(&eheader,elf,sizeof(Elf64_Ehdr));

	Elf64_Shdr *sheaders = calloc(eheader.e_shnum+1,sizeof(Elf64_Shdr));
	Elf64_Addr oep = eheader.e_entry;

	Elf64_Offset *offsets = calloc(eheader.e_shnum+1,sizeof(Elf64_Offset));
	int idx = 0;

	for(int i=0;i<eheader.e_shnum;i++)
	{
		p = elf + eheader.e_shoff + (i*sizeof(Elf64_Shdr));
		memcpy(&(sheaders[i]),p,sizeof(Elf64_Shdr));
		if(sheaders[i].sh_type == SHT_STRTAB)
		{
			offsets[idx].section = i;
			if(offsets[idx].section != eheader.e_shstrndx) continue;
			offsets[idx].offset = sheaders[i].sh_offset;
			idx++;
		}
	}

	for(int i=0;i<eheader.e_shnum;i++)
	{
		p = elf + offsets[0].offset + sheaders[i].sh_name;
		if(!strcmp(p,".text") || !strcmp(p,".eh_frame") || !strcmp(p,".rodata") || !strcmp(p,".data"))
		{
			offsets[idx].name = p;
			offsets[idx].section = i;
			offsets[idx].offset = sheaders[i].sh_offset;
			offsets[idx].size = sheaders[i].sh_size;
			idx++;
		}
	}

	for(int i=0;i<idx;i++)
	{
		if(offsets[i].name)
		{
			if(strcmp(offsets[i].name,".eh_frame"))
			{
				p = elf + offsets[i].offset;
				printf("%s: %p %p\n",offsets[i].name,(void *)offsets[i].offset,(void *)offsets[i].size);
				for(int j=0;j<offsets[i].size;j++)
				{
					if(p[j]) p[j] = (p[j] ^ XOR_MAGIC) & 0xff;
				}
			}
			else
			{
				((Elf64_Ehdr *)elf)->e_entry = ELF_BASE + offsets[i].offset;
				system("nasm ./unload.asm");
				rfd = open("./unload",O_RDONLY);

				stat("./unload",&ssc);

				sc = calloc(ssc.st_size+0x10,sizeof(char));
				read(rfd,sc,ssc.st_size);
				close(rfd);

				p = elf + offsets[i].offset;
				memcpy(p,sc,ssc.st_size);
			}
		}
	}

	int wfd = open(paxx,O_WRONLY|O_CREAT|O_TRUNC,S_IRUSR|S_IWUSR|S_IXUSR);
	write(wfd,elf,s.st_size);

	close(wfd);
	memset(elf,0,s.st_size);
	free(elf);
	memset(sc,0,ssc.st_size);
	free(sc);
	memset(sheaders,0,sizeof(Elf64_Shdr)*eheader.e_shnum);
	free(sheaders);
	return 0;
}

int main(int argc, char **argv)
{
	if(argc != 2) printf("Usage: %s [ELF]",argv[0]);
	else
	{
		if(pack_ELF(argv[1]) < 0)
		{
			puts("error");
		}
	}
	return 0;
}