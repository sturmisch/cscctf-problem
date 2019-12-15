#!/usr/bin/python

from struct import pack, unpack

"""
typedef uint16_t Elf64_Half;
typedef uint32_t Elf64_Word;
typedef	int32_t  Elf64_Sword;
typedef uint64_t Elf64_Xword;
typedef	int64_t  Elf64_Sxword;
typedef uint64_t Elf64_Addr;
typedef uint64_t Elf64_Off;

typedef struct
{
  unsigned char	e_ident[EI_NIDENT];	/* Magic number and other info */
  Elf64_Half	e_type;			/* Object file type */
  Elf64_Half	e_machine;		/* Architecture */
  Elf64_Word	e_version;		/* Object file version */
  Elf64_Addr	e_entry;		/* Entry point virtual address */
  Elf64_Off	e_phoff;		/* Program header table file offset */
  Elf64_Off	e_shoff;		/* Section header table file offset */
  Elf64_Word	e_flags;		/* Processor-specific flags */
  Elf64_Half	e_ehsize;		/* ELF header size in bytes */
  Elf64_Half	e_phentsize;		/* Program header table entry size */
  Elf64_Half	e_phnum;		/* Program header table entry count */
  Elf64_Half	e_shentsize;		/* Section header table entry size */
  Elf64_Half	e_shnum;		/* Section header table entry count */
  Elf64_Half	e_shstrndx;		/* Section header string table index */
} Elf64_Ehdr;

typedef struct
{
  Elf64_Word	sh_name;		/* Section name (string tbl index) */
  Elf64_Word	sh_type;		/* Section type */
  Elf64_Xword	sh_flags;		/* Section flags */
  Elf64_Addr	sh_addr;		/* Section virtual addr at execution */
  Elf64_Off	sh_offset;		/* Section file offset */
  Elf64_Xword	sh_size;		/* Section size in bytes */
  Elf64_Word	sh_link;		/* Link to another section */
  Elf64_Word	sh_info;		/* Additional section information */
  Elf64_Xword	sh_addralign;		/* Section alignment */
  Elf64_Xword	sh_entsize;		/* Entry size if section holds table */
} Elf64_Shdr;
"""

def get_cstr(addr, offset):
	idx = offset
	l = []
	while addr[idx] != '\x00':
		l.append(addr[idx])
		idx += 1
	return ''.join(l)

def unpack_ELF(filename):
	ELF_BASE = 0x400000
	MAGIC_XOR = 0xa5
	rawelf = open(filename,"rb").read()
	byteelf = bytearray(rawelf)
	elf = {
		"header": {
			"e_ident": "",
			"e_type": 0,
			"e_machine": 0,
			"e_version": 0,
			"e_entry": 0,
			"e_phoff": 0,
			"e_shoff": 0,
			"e_flags": 0,
			"e_ehsize": 0,
			"e_phentsize": 0,
			"e_phnum": 0,
			"e_shentsize": 0,
			"e_shnum": 0,
			"e_shstrndx": 0
		},
		"sections": {}
	}

	(
		elf["header"]["e_ident"], elf["header"]["e_type"], elf["header"]["e_machine"], 
		elf["header"]["e_version"] , elf["header"]["e_entry"], elf["header"]["e_phoff"],
		elf["header"]["e_shoff"], elf["header"]["e_flags"] ,elf["header"]["e_ehsize"],
		elf["header"]["e_phentsize"], elf["header"]["e_phnum"], 
		elf["header"]["e_shentsize"], elf["header"]["e_shnum"],
		elf["header"]["e_shstrndx"]
	) = unpack("16sHHIQQQIHHHHHH",rawelf[:64])

	offsets = []
	for i in xrange(elf["header"]["e_shnum"]):
		offset = i*64
		(
			sh_name, sh_type, sh_flags,
			sh_addr, sh_offset, sh_size,
		 	sh_link, sh_info, sh_addralign, sh_entsize
		) = unpack("IIQQQQIIQQ",rawelf[elf["header"]["e_shoff"]+offset:elf["header"]["e_shoff"]+offset+64])

		# from elf.h:
		# #define SH_STRTAB 3
		if sh_type == 3 and i == elf["header"]["e_shstrndx"]:
			offsets.append((i,sh_offset,-1))

	for i in xrange(elf["header"]["e_shnum"]):
		offset = i*64
		(
			sh_name, sh_type, sh_flags,
			sh_addr, sh_offset, sh_size,
		 	sh_link, sh_info, sh_addralign, sh_entsize
		) = unpack("IIQQQQIIQQ",rawelf[elf["header"]["e_shoff"]+offset:elf["header"]["e_shoff"]+offset+64])
		s = get_cstr(rawelf,offsets[0][1]+sh_name)
		if s == ".text" or s == ".eh_frame" or s == ".data" or s == ".rodata":
			elf["sections"][s] = {
				"section": i,
				"offset": sh_offset,
				"size": sh_size,
			}

	# copy unpacking algorithm
	for section in elf["sections"].keys():
		offset = elf["sections"][section]["offset"]
		size = elf["sections"][section]["size"]
		if section != ".eh_frame" and section != ".data":
			# replace entry point with _start
			if section == ".text": byteelf[24:32] = pack("Q",ELF_BASE+offset)
			for i in xrange(size):
				# nop out the ptrace check
				if offset+i >= 0x5c3 and offset+i <= 0x600: byteelf[offset+i] = 0x90
				# null preserving xor
				elif byteelf[offset+i] != 0: byteelf[offset+i] ^= 0xa5
		elif section == ".data":
			for i in xrange(0x20,size):
				# non null preserving xor
				if i%4 == 0:
					byteelf[offset+i] ^= 0xa5

	open("unpaxx_unpacked","wb").write(byteelf)

def crack():
	flag = ''
	flag_enc = [
		0x000000b5,0x00000098,0x0000009f,0x000000a5,
		0x000000ce,0x00000089,0x0000009f,0x00000096,
		0x000000ca,0x00000088,0x000000cb,0x00000090,
		0x0000008a,0x0000009f,0x000000b3,0x00000090,
		0x000000ce,0x00000087,0x00000090,0x0000009f,
		0x000000a9,0x00000090,0x0000008e,0x000000ca,
		0x0000009b,0x00000093,0x000000cb,0x0000008c,
		0x0000009f,0x000000aa,0x00000096,0x000000cd,
		0x0000008b,0x0000009f,0x00000095,0x000000c9,
		0x0000009f,0x000000ce,0x00000090,0x000000cb
	]
	for c in flag_enc:
		flag += chr((c-0x7f)^0x7f)

	print "CCC{{{}}}".format(flag)

# unpack_ELF("./unpaxx.packed")
crack()