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