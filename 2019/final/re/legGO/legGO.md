# CSCCTF 2019
## _legGO_

## Informasi Soal
| Kategori | Poin |
| -------- | ---- |
| Reverse Engineering | 1000 |
### Deskripsi
> Leggo! mari takhlukanlah dengan cepat dan efektif semaksimal mungkin. Flag disana menantimu :D
>
> Author: redspiracy

## Cara Penyelesaian
Diberikan sebuah binary yang dibuat menggunakan bahasa Go, atau Golang.

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/1.jpg)

Binary tersebut ketika dijalankan, akan meminta input number yang nantinya akan dilakukan pengecekan untuk key dari xor flag.
Namun ketika binary diberikan input, program berhenti karena limit calculation, yang disebabkan oleh concurrent runtime.

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/2.jpg)

Dari hasil tersebut kita diminta untuk menganalisa maksud dari program legGO berjalan. Karena pada saat final, sourcecode telah diberikan, lebih efisien untuk kita meneliti function berdasarkan dari sourcecode dan binarynya seperti berikut.
Pertama, kita perlu tau main address dari binary tersebut yang dapat di ketahui melalui IDA, untuk melihat urutan function yang dijalankan.

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/3.jpg)

Dari gambar tersebut kita mengetahui bahwa function yang dijalankan pertama kali adalah main_calcnum(). Selanjutnya kita perlu menganalisa apa yang ada dalam funtion tersebut.

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/4.jpg)

Function main_calcnum berisi code yang digunakan untuk menghitung key yang diulang sebanyak 8678, yang kemudian dilakukan function checking untuk angka perlooping, lalu dalam main_check() dilakukan pemanggilan funtion modulonum(). 
Pada funtion tersebut angka yang dilempar dari main_check() dilakukan operasi modulus dan lainnya seperti berikut:

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/6.jpg)

Jika diteliti lebih lanjut, terdapat sebuah string array yang terdapat pada qword_4EDD80, yaitu berisi sebuah char:

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/7.jpg)

![image](https://raw.githubusercontent.com/redspiracy/write-ups/master/cscctf2019/final/legGO/Screenshot/8.jpg)

Sehingga jika di translate secara keseluruhan dan digabung dengan hint akhir akan menjadi seperti ini:
```
package main

import (
	"fmt"
	"strconv"
	"time"
	"os"
)

func modulonum(seed, num int) int{
	for seed%num == 0{
		seed = seed / num
	}
	return seed
}

func timeout() {
	time.Sleep(3 * time.Second)
	fmt.Println("Ouch, calculation key timeout :(")
	os.Exit(1)
}

func check(n int) int{
	var result int

	n = modulonum(n, 2)
	n = modulonum(n, 3)
	n = modulonum(n, 5)

	if n == 1{
		result = 1
	} else {
		result = 0
	}

	return result
}

func calcnum() int{
	var i = 1
	var count = 1
	
    for 8678 > count {
        i += 1
        if check(i) == 1{
			count += 1
		}
	}

    return i 
}

func main(){
	var key int
	var superkey int
	var secret = [...]int{102, 120, 52, 94, 118, 62, 109, 93, 90, 103, 124, 75, 98, 61, 55, 79, 109}
	
	fmt.Printf("legGO buddy! please input the key number: ")
	fmt.Scan(&key)

	go timeout()

	superkey = calcnum()

	if superkey == key{
		key := strconv.Itoa(key)	
		flag := ""

		for i := range key {
			char, err := strconv.Atoi(string(key[i]))
			if err == nil{
				flag += string(char ^ secret[i])
			} 
		}

	fmt.Println("Congrats! your flag is : CCC{" + flag + "}")
	}else{
		fmt.Println("Ouch, wrong.")
	}
}
```

Jika dilihat lebih lanjut, maka algoritma tersebut mencari nilai 8678 yang memiliki faktor dari 2, 3, dan 5. Namun permasalahan yang terjadi adalah, untuk menghitung pengulangan sebanyak 8678 ini membutuhkan waktu yang sangat-sangat lama, sehingga diperlukan optimisasi.
Berikut script python optimisasi yang digunakan:
```
def getuglynum(n): 
    ugly = [0] * n
    ugly[0] = 1
  
    i2 = i3 =i5 = 0
  
    i = 2
    j = 3
    k = 5
  
    for l in range(1, n): 
        ugly[l] = min(i, j, k) 
  
        if ugly[l] == i: 
            i2 += 1
            i = ugly[i2] * 2
  
        if ugly[l] == j: 
            i3 += 1
            j = ugly[i3] * 3
  
        if ugly[l] == k:  
            i5 += 1
            k= ugly[i5] * 5
  
    return ugly[-1] 

key = getuglynum(8678)

result = ""
secret = [102, 120, 52, 94, 118, 62, 109, 93, 90, 103, 124, 75, 98, 61, 55, 79, 109]

for x in range(len(secret)):
    result += chr(int(str(key)[x]) ^ secret[x])
    
print "CCC{" + result + "}"
```

## Flag
> CCC{by3_u9lY_nuMb44Hh}
