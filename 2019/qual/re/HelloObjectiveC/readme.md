# HelloObjectiveC


Diberikan binary Mac:
```
$ file HelloObjectiveC 
HelloObjectiveC: Mach-O 64-bit x86_64 executable, flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>
```


Mari kita lihat pseudocode IDA:
```C
v6 = flag;
flag = v5;
objc_release(v6);
v7 = (void *)objc_alloc(&OBJC_CLASS___NSString);
v11 = objc_msgSend(v7, "initWithFormat:", CFSTR("%@TF"), CFSTR("C"));
v8 = (void *)objc_alloc(&OBJC_CLASS___NSMutableString);
v10 = objc_msgSend(v8, "initWithFormat:", CFSTR("%@come_%@_%@-C"), CFSTR("W3l"), CFSTR("T0"), CFSTR("0bj3ct1v3"));
objc_msgSend(flag, "appendFormat:", CFSTR("%@{%@}"), v11, v10);
printf("%s\n", "CTF{This_is_not_the_flag}");
```


Jika kita cari "%@ Objective C" di Google, kita mendapati bahwa format specifier ini dipakai untuk menyebut objek ObjectiveC (dalam case ini, constant CFString). Kita substitusi manual dan dapatkan flagnya.


Flag: `CCC{W3lcome_T0_0bj3ct1v3-C}`
