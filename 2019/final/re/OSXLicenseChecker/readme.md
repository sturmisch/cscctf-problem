# OSX License Checker


Diberikan binary Mach-O yang ketika dijalankan meminta license key:
```
$ file OSXLicenseChecker && ./OSXLicenseChecker
OSXLicenseChecker: Mach-O 64-bit executable x86_64
Please enter the license: 
```


Ketika dimasukkan dalam decompiler, terlihat banyak constraint yang dibutuhkan dalam memvalidasi flagnya, lalu diakhir dilakukan checksum terhadap MD5 `b7575a9d0a6bc912480b28ef3597c444`



Setelah script solver dibuat untuk menyelesaikan constraint-constraintnya, masih sulit mencari karakter yang sesuai.
```
$ python solver-before.py
Th&_=&g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
Th'_='g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
Th#_=#g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
Th3_=3g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
Th7_=7g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
Th5_=5g_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_f`r_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_f"r_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_f2r_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_frr_Ti$_ChEA,&igT_,z_,iD0M"T
ThE_=Eg_fjr_Ti$_ChKA,$igT_(z_(eD0M(T
ThE_=Eg_fjr_Ti$_ChKA,$egT_(z_(eD0M(T
The_=eg_fjr_Ti$_ChOA,$egT_(z_(eD0M(T
ThE_=Eg_fjr_Ti$_ChOA,$egX_(z_(eD0M(X
The_=eg_fjr_Ti$_ChOA,&egX_(z_(eD0M(X
ThE_=Eg_fjr_Ti$_ChOA,&egX_(z_(eD0M(X
ThE_=Eg_fjr_Ti$_ChOA,,egX_(z_(eD0M(X
```


Namun polanya sudah terlihat, yang jika dituliskan secara normal yakni `the flag for this challenge is indomie`. Sehingga kita dapat mengoptimalkan script bruteforce kita dengan membantu memberikan constraint tambahan.
```
$ python solver-after.py
Th3_Pl3g_f0r_T1$_Ch4ll4ng3_1z_1nD0M23
Th3_Pl3g_f0r_T1$_Ch4114ng3_1z_1nD0M23
```


Sehingga pada akhirnya didapatkan flag yang benar
```
$ ./OSXLicenseChecker
Please enter the license: Th3_Pl3g_f0r_T1$_Ch4114ng3_1z_1nD0M13
Correct, submit CTF{Th3_Pl3g_f0r_T1$_Ch4114ng3_1z_1nD0M13} as the flag.
```