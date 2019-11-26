Forensic - DUARRR!!<br>
Indonesia telah memasuki tahun 2027, ASEAN telah membentuk kesepakatan untuk melakukan pengawasan ketat terhadap peredaran memes karena diduga merusak kejiwaan pemuda pemudi negara asia<br>
Kamu diberikan arahan untuk menginvestigasi printer dari seorang warga negara Indonesia yang diduga telah mencetak memes secara illegal, coba cari tahu apa yang sebenarnya dicetak<br>

Diberikan sebuah printerlog
<br><br>
<p align="center">
<img src="https://github.com/laBigby/cscctf-foren2/blob/master/201.JPG">
</p>
<br><br>
Terdapat 262144 entry di dalam log tersebut, dan di setiap entry terdapat 3 value yang yang dipisahkan oleh koma<br>
Ketiga value tersebut merupakan RGB value, kita harus merangkai gambar yang dimaksud pixel by pixel sesuai dengan RGB value di setiap entry<br>
Terdapat 262144 entry yang berarti 262144 pixel, yang berarti gambar berukuran 512x512 pixel<br><br>
Soal bisa diselesaikan dengan scripting<br><br>


```Python
from PIL import Image
import re
f=open("printerlog", 'r')
x = []
for line in f.readlines():
	try:
		(front,r,g,b,back) = map(int, re.findall(r'\d+', line))
	except:
		continue
	x.append((front,r,g,b,back))
gbr = Image.new("RGB", (512,512))
pixel = gbr.load()
k=0
for i in range(0,512):
	for j in range(0,512):
		pixel[j,i] = (x[k][1], x[k][2], x[k][3])
		k+=1
gbr.save("new.jpg")
```	


<p align="center">
<img src="https://github.com/laBigby/cscctf-foren2/blob/master/new.jpg">
</p>
<br><br>
Dapat di scan QR code nya dan didapatkan flag di google drive
<br>


Flag : `CCC{1_r4n_0ut_of_1d3as_t0_wr1t3_as_fl4g}`
