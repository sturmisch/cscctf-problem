### Weak Random


<p align="center">
<img src="https://github.com/EternalBeats/cscctf/blob/master/Screenshot/WeakRandom/start.png">
</p>


Diberikan connection nc, didalamnya diminta sebuah inputan angka. Setelah di input diberikan expected value nya. Dan setiap kita close connectionnya angkanya berubah menjadi expected angka yang baru, or it is?


> True randomness itu susah untuk diciptakan pasti ada suatu algoritma yang membuat dia menjadi "random", ini yang dinamakan pseudorandom.


Dengan memakai concept pseudorandom kita bisa mengetahui random itu mempunyai suatu seed (seed ini yang mengendalikan output dari value random kita). Jadi bila dicoba untuk di request berulang-ulang kali kita pasti mendapat suau duplicate. Duplicate ini yang akan membantu untuk hasil berikutnya.

```Python
#!/usr/bin/env python
from pwn import *
import sys

host = "weakrandom.problem.cscctf.com"
port = 10000

found = True

seen = []

while(found):
	sys.stdin.flush()
	sys.stdout.flush()
	s=remote(host, port)
	prompt = s.recv(4096)
	print prompt
	s.sendline("2267059\n")
	prompt = s.recv(4096)
	print prompt
	if "Wrong" in prompt:
		number = prompt.split('\n')[0]
		number = number.split(' ')[5]
		for i in range(len(seen)):
			if number == seen[i][0]:
				s.recv(4096)
				s.sendline(seen[i][1]+"\n")
				prompt = s.recv(4096)
				if "flag" in prompt:
					print prompt
				else:
					prompt = s.recv(4096)
					print prompt
				found = False
				s.close()
				break
		if "Insert" not in prompt:
			s.recv(4096)
		s.sendline("1\n")
		prompt = s.recv(4096)
		number2 = prompt.split('\n')[0]
		number2 = number2.split(' ')[5]
		seen.append([number, number2])
		s.close()
	else:
		print prompt
		found = False
		s.close()
```


Cara yang saya ambil yaitu dengan menyimpan expected value pertama dan kedua, setiap kali expected value pertama muncul dicheck lagi dengan apa yang ada di list (yang sudah pernah muncul), bila terdapat duplicate kita bisa anggap value berikutnya adalah expected value kedua dari yang sebelumnya expected value pertama (yang duplicate).


<p align="center">
<img src="https://github.com/EternalBeats/cscctf/blob/master/Screenshot/WeakRandom/end.png">
</p>


Flag : `CCC{tRu3_R4nd0mn3sS_1s_H4rd}`
