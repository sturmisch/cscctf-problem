# CSCCTF 2019


## _crackwrr_


## Informasi Soal
| Kategori | Poin |
| -------- | ---- |
| Reverse Engineering | 1000 |


### Deskripsi
> Cracker jahat adalah h4ckwr baik yang tersakiti.....
>
> author: redspiracy

## Cara Penyelesaian


Diberikan file binary, dengan detail sebagai berikut:
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/1.jpg)


Selanjutnya kita dapat melakukan eksekusi binary tersebut, untuk melihat alur dan input/output yang diberikan. Berikut hasil dari binary yang dieksekusi.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/8.jpg)


Dari hasil tersebut dapat disimpulkan, bahwa binary setelah berjalan akan melakukan checking pada version elf tersebut. Namun, karena version yang didapatkan telah out-of-date, maka kita harus melakukan patching. Untuk melihat apa yang binary compare, kita dapat menggunakan ltrace.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/2.jpg)


Output dari ltrace ternyata tidak keluar, karena didapatkan ptrace (anti-debugger). Sehingga program tidak bisa ditrace atau didebug.
Untuk menyelesaikan soal ini, sebenarnya terdapat banyak cara, dari mulai menggunakan gdb atau debugger lain, melakukan patching pada debugger dan dilanjutkan dengan scripting python, sampai cara langsung, yaitu dengan melakukan patch dan export menjadi elf lalu run kembali.


Pada cara ini, saya menggunakan cara terakhir agar lebih mudah, tanpa harus melakukan scripting, dengan cara melakukan patching. Langkah awal, kita dapat membuka ida untuk melihat flow dari program tersebut.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/3.jpg)
Terlihat flow program ada yang merujuk ke print flag. Namun, sebelum sampai situ dilakukan comparing value, yang diduga yaitu version check.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/4.jpg)
Comparing value dilakukan pada [rbp+var_54], dengan 3419h lalu dilanjutkan dengan conditional jump (JZ) ke alamat loc_A03 jika hasilnya true.
Namun permasalahan yang dihadapi bahwa [rbp+var_54] tidak berisi value 3419h, sehingga hasil compare selalu mengembalikan nilai false.
Pada tahap ini, kita perlu untuk melakukan patch binary, pada alamat compare JZ, yang setelah dianalisa, alamat JZ terdapat pada 0x9F0, seperti berikut.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/5.jpg)


Didapat bahwa value dari JZ yaitu 74, kita perlu mengganti value dari JZ menjadi JNZ dengan value 75. Mengapa JNZ? karena kita akan membalikan return flow dari proses compare. Dari yang sebelumnya jika kondisi tersebut true maka flow akan berjalan ke kanan, menjadi jika kondisinya true flow akan berjalan ke kiri, sedangkan jika hasil compare tersebut bernilai false, maka flow akan berjalan ke kanan (dimana print flag dilakukan). Disini saya menggunakan https://hexed.it untuk melakukan patch dan mengexportnya kembali menjadi elf.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/6.jpg)


Pergi ke alamat 0x9F0, lalu ganti nilai 74 (JZ) menjadi 75(JNZ), kemudian lakukan export file.


Setelah export selesai, lakukan eksekusi kembali pada binary yang sudah di patch, lalu flag akan keluar.
![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/crackwrr/Screenshot/7.jpg)

## Flag
> CCC{cr4ck3r_m0r3_p000w3rfull_Th4n_j0k33r}
