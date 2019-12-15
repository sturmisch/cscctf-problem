# unpaxxx


## Analisa


Diberikan binary stripped.

```
$ file unpaxx.packed
unpaxx.packed: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=886debbcb5ef865e7fa47ffde4e38d46724ceab6, stripped
$ ./unpaxx.packed
Usage: ./unpaxx.packed [password]
$ ./unpaxx.packed wtf
Try again.
```


Soal mengacu pada packer-unpacker, dari nama file beserta ekstensinya. Jika kita lihat pada disassembly bagian `.text`, terlihat instruksi assembly yang tidak normal:
```
Disassembly of section .text:

00000000004004e0 <.text>:
  4004e0:	94                   	xchg   esp,eax
  4004e1:	48 ec                	rex.W in al,dx
  4004e3:	2c 74                	sub    al,0x74
...
```


Bandingkan dengan contoh ELF helloworld berikut:
```
Disassembly of section .text:

0000000000400400 <.text>:
  400400:	31 ed                	xor    ebp,ebp
  400402:	49 89 d1             	mov    r9,rdx
...
```


Umumnya, algoritma dari sebuah packer dan/atau unpacker adalah:
1. Bedah executable dan bagi per bagian
2. Lakukan kompresi dan/atau enkripsi pada bagian yang diinginkan
3. Letakkan prosedur unpack pada suatu bagian di executable (alamat ini harus mempunyai permission executable)
4. Timpa entry point dari executable ke alamat dari prosedur unpack



Kita perlu mengetahui entry point dari ELF ini. Cukup lakukan `readelf -h`:
```
$ readelf -h unpaxx.packed
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x400880
  Start of program headers:          64 (bytes into file)
  Start of section headers:          4568 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         9
  Size of section headers:           64 (bytes)
  Number of section headers:         26
  Section header string table index: 25
```


Lokasi entrypoint ini tidak dapat di-disassemble melalui `objdump` karena bukan merupakan bagian dari `.text`. Namun kita dapat melihatnya melalui IDA atau Binary Ninja atau gdb.


## Penyelesaian


Kita akan membedah algoritma prosedur unpack ini agar kita dapat mengembalikkan ELF dalam bentuk semula. Beberapa instruksi pertama ini menyimpan nilai register ke stack, dan mengosongkan nilai tersebut untuk dipakai:
```
gef> x/82i 0x400880
   0x400880:	push   rax
   0x400881:	push   rdi
   0x400882:	push   rsi
   0x400883:	push   rdx
   0x400884:	push   rcx
   0x400885:	push   r8
   0x400887:	push   r9
   0x400889:	xor    eax,eax
   0x40088b:	xor    edi,edi
   0x40088d:	xor    esi,esi
   0x40088f:	xor    edx,edx
   0x400891:	xor    ecx,ecx
   0x400893:	xor    r8d,r8d
...
```


Berikutnya dipanggil `mprotect` untuk mengubah permission dari mapping; `0x400000-0x401000` ke rwx dan `0x600000-0x601000` ke rw.
```
...
   0x400896:	mov    edi,0x400000
   0x40089b:	mov    esi,0x1000
   0x4008a0:	mov    dl,0x7
   0x4008a2:	mov    al,0xa
   0x4008a4:	syscall 
   0x4008a6:	mov    edi,0x600000
   0x4008ab:	mov    esi,0x1000
   0x4008b0:	mov    dl,0x3
   0x4008b2:	mov    al,0xa
   0x4008b4:	syscall 
...
```


Bagian ini merupakan bagian utama dari unpacker. 
```
...
   0x4008b6:	xor    ecx,ecx
   0x4008b8:	push   rcx
   0x4008b9:	push   rcx
   0x4008ba:	mov    edx,0x2d2
   0x4008bf:	push   rdx
   0x4008c0:	push   0x4004e0
   0x4008c5:	push   rdx
   0x4008c6:	push   0x6004e0
   0x4008cb:	xor    edx,edx
   0x4008cd:	mov    dl,0x68
   0x4008cf:	push   rdx
   0x4008d0:	push   0x4007c0
   0x4008d5:	push   rdx
   0x4008d6:	push   0x6007c0
   0x4008db:	mov    dl,0xa0
   0x4008dd:	push   rdx
   0x4008de:	push   0x601020
   0x4008e3:	pop    rdi
   0x4008e4:	pop    r8
   0x4008e6:	xor    ecx,ecx
   0x4008e8:	test   rdi,rdi
   0x4008eb:	je     0x40091c
   0x4008ed:	lea    rdx,[rdi+rcx*1]
   0x4008f1:	mov    al,BYTE PTR [rdx]
   0x4008f3:	cmp    edx,0x601000
   0x4008f9:	jb     0x40090a
   0x4008fb:	mov    r9b,dl
   0x4008fe:	and    dl,0x3
   0x400901:	test   dl,dl
   0x400903:	mov    dl,r9b
   0x400906:	je     0x40090e
   0x400908:	jne    0x400912
   0x40090a:	test   al,al
   0x40090c:	je     0x400912
   0x40090e:	xor    al,0xa5
   0x400910:	mov    BYTE PTR [rdx],al
   0x400912:	inc    rcx
   0x400915:	cmp    rcx,r8
   0x400918:	jbe    0x4008ed
   0x40091a:	jmp    0x4008e3
...
```



Kumpulan instruksi push ini merupakan offset dan ukuran bagian yang ingin di-unpack. Alamatnya dibandingkan dengan `0x601000` (bagian `.data`), jika lebih kecil akan dicek kembali, nilai byte yang didapatkan dari alamat yang telah direference adalah null atau tidak. Apabila nilainya bukan null, akan dixor dengan 0xa5. Ini merupakan algoritma null preserving xor. Jika alamat masuk ke bagian `.data`, akan dicek apakah hasil modulus LSB terhadap 4 dalam bentuk instruksi `and dl, 0x3` merupakan 0 atau bukan. Jika 0, maka akan dilakukan xor terhadap nilai 0xa5.


Sisa instruksi merupakan `mprotect` dan pop untuk mengembalikkan permission dan register seperti semula; dan return ke original entry point.



Untuk membuat unpacker, harus melakukan parse terhadap executable yang ingin di-unpack. Saya pribadi membuat unpacker dalam script python agar mudah dipelajari oleh peserta. Setelah dibuat script/program-nya, Kita bisa lihat kode asli program. Namun masih terdapat satu halangan, yaitu ptrace atau anti-debugging:
```
...
  4005c2:	55                   	push   rbp
  4005c3:	48 89 e5             	mov    rbp,rsp
  4005c6:	b9 00 00 00 00       	mov    ecx,0x0
  4005cb:	ba 00 00 00 00       	mov    edx,0x0
  4005d0:	be 00 00 00 00       	mov    esi,0x0
  4005d5:	bf 00 00 00 00       	mov    edi,0x0
  4005da:	b8 00 00 00 00       	mov    eax,0x0
  4005df:	e8 dc fe ff ff       	call   4004c0 <ptrace@plt>
  4005e4:	48 83 f8 ff          	cmp    rax,0xffffffffffffffff
  4005e8:	75 16                	jne    400600 <exit@plt+0x130>
  4005ea:	48 8d 3d d7 01 00 00 	lea    rdi,[rip+0x1d7]        # 4007c8 <exit@plt+0x2f8>
  4005f1:	e8 aa fe ff ff       	call   4004a0 <puts@plt>
  4005f6:	bf ff ff ff ff       	mov    edi,0xffffffff
  4005fb:	e8 d0 fe ff ff       	call   4004d0 <exit@plt>
  400600:	90                   	nop
  400601:	5d                   	pop    rbp
  400602:	c3                   	ret
...
```



Ini adalah prosedur anti-debugging yang cukup umum; program mencoba melakukan debugging melalui `ptrace` terhadap diri sendiri, apa bila hasilnya adalah -1, maka program akan langsung keluar. Ketika dilakukan unpack, bisa langsung di-patch instruksi ini menjadi `nop`-sled; atau lakukan trik LD_PRELOAD untuk ptrace. Logika dari program saya buat cukup mudah, karena esensi soal adalah tentang ELF dan proses pack-unpack executable. Berikut pseudocode fungsi check_password/sub_40062F:
```C
int check_password(const char *s)
{
	if(sub_400603(s) != 40) return 1;
	for(int i=0;i<40;i++)
	{
		if((s[i] ^ 0x7f) + 0x7f != dword_601020[i]) return 1;
	}
	return 0;
}
```


Ambil terlebih dulu integer array yang ada pada alamat 0x601020, dan balikkan algoritma pengecekkan passwordnya (jika prosedur unpack tidak ditelaah dengan baik, maka array dan password akan salah). Flag dapat diperoleh dengan mudah:
```Python
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
```


Output script (panggil fungsi crack):
```
$ python unpacker.py 
CCC{If_Y0u_h4v3nt_Kn0wn_Unp4ck3r_Th1s_i5_0n3}
```
