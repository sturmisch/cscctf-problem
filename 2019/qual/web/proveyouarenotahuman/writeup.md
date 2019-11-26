# Prove You Are Not A Human

## Ground

Secara garis besar, web yang diberikan memiliki dua fungsi utama: yang pertama web akan menampilkan beberapa kata-kata seperti **Coffee**, **Coffey**, gambar kopi, dan sebagainya. Fungsi kedua adalah web akan menerima input berapa jumlah kata-kata **Coffee** yang tampil pada layar. Bila user menghitung dengan benar, maka nilai streak akan bertambah 1. Dari elemen yang terdapat pada halaman web, nilai streak harus lebih dari 1000 untuk membuktikan bahwa user adalah robot dan bukan manusia.

## Solve

Problem ini dapat dilakukan dengan mudah menggunakan automasi. Singkatnya, hitung berapa banyak kata Coffee yang muncul, submit, dan lakukan lagi hingga nilai streak melebihi angka 1000. Berikut contoh code yang dapat digunakan.

    import requests
    
    URL = "http://localhost:8000/"
    
    s = requests.Session()
    for i in range(1001):
        res = s.get(URL)
        src = res.text
        num = src.count("Coffee") - 1
        is_correct = s.post(URL, data={"num": num})
        print(is_correct.text)

Jumlah kata **Coffee** harus dikurangi 1 karena kata **Coffee** yang terdapat dalam pertanyaan `How many "Coffee" are displayed below?`tidak dihitung.
