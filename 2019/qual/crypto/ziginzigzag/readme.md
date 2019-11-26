### Zig in ZigZag


<p align="center">
<img src="https://github.com/EternalBeats/cscctf/blob/master/Screenshot/ZigInZigZag/enc_flag.png">
</p>


Diberikan sebuah encrypted string, juga ada chall desc


> Zig lost his partner in a room with X x Y unit. Zag is at the botom right of the room. Follow Zig's journey of finding his partner Zag, and Zig will tell you the secret 
>
> flag format = CCC{flag}


Diberitahu kita membuat sebuah segi-empat dengan ukuran X dan Y. Dan juga karena ini zigzag (turun naik), dicobalah kita buat string itu menjadi kotak dengan ukuran X & Y. Di ukuran 16 x 15 terdapat sesuatu yang menarik.
<p align="center">
<img src="https://github.com/EternalBeats/cscctf/blob/master/Screenshot/ZigInZigZag/pattern.png">
</p>


[**'W'**, 'b', 'i', 'u', 's', 'h', 'C', 'T', 'n', 'e', 'o', 'e', 'b', 'F', 'p']


['p', **'e'**, 'l', 'p', 'A', 'H', 'i', 'a', 'o', 'd', 'M', 'd', 't', 'i', 'l']


['a', 'e', **'l'**, 'e', 'h', 's', 'a', 's', 'n', 'D', 'O', 'a', 's', 'h', 'n']


['e', 'g', 'r', **'c'**, 'm', 'e', 'T', 'v', 'K', 'Y', 'e', 'f', 't', 'A', 'o']


['d', 'd', 'Z', 'I', **'o'**, 'W', 'r', 'h', 'e', 'i', 'o', 'c', 'Q', 'h', 'n']


['d', 'H', 'S', 'i', 's', **'m'**, 'h', 'I', 'e', 'T', 'n', 'u', 'i', 'u', 'e']


['m', 'A', 'a', 'o', 'p', 'N', **'e'**, 'e', 's', 'C', 'o', 'd', 'F', 'p', 'e']


['s', 'a', 'l', 'v', 'H', 'p', 'o', **'T'**, 'r', 'U', 'o', 'D', 'O', 'i', 'h']


['e', 't', 't', 'g', 'e', 'e', 'i', 't', **'o'**, 'e', 's', 'm', 'e', 'f', 'n']


['d', 'r', 'i', 'i', 'o', 'T', 'r', 'n', 'T', **'T'**, 'Z', 'e', 'p', 'c', 'P']


['r', 'O', 'T', 'o', 'c', 'r', 'o', 'e', 'g', 'o', **'h'**, 'i', 'd', 'e', 'i']


['p', 'o', 'u', 'h', 'n', 's', 'i', 'B', 'I', 'T', 'o', **'i'**, 'g', 'A', 't']


['i', 'h', 'b', 't', 'i', 'W', 'M', 't', 'e', 's', 'h', 'H', **'s'**, 'Z', 'n']


['d', 't', 'e', 'l', 'H', 's', 'h', 'e', 'h', 'C', 'T', 'e', 'a', **'P'**, 'a']


['g', 'Y', 'o', 'r', 'e', 'o', 'K', 'e', 't', 'm', 'o', 'h', 'Z', 'r', **'r'**]


[**'o'**, 'C', 'o', 'r', 'T', 'm', 'w', 'i', 'r', 'h', 'M', 'm', 'e', 'i', 'd']


Terlihat ada tulisan WelcomeToThis... dan lanjutannya ada di bawah kiri, bila lanjut dilihat lanjutannya lagi ada di bagian atas posisi kedua, jadi bisa di umpamakan seperti...

> bila tembus kanan, goto kiri
>
> bila tembus bawah, goto atas

dengan logic diatas kita bisa mengambil string nya...

<p align="center">
<img src="https://github.com/EternalBeats/cscctf/blob/master/Screenshot/ZigInZigZag/flag.png">
</p>

Flag :


`CCC{ZippingTheZipperIsNotTooHard}` (intended)


`CCC{WelcomeToThisProblemWhereZigZagCipherIsUsedAndYouAsTheCompetitorsHaveToDecipherThisKindOfProblemCanYouFindOutHowToDecipherThisKindOfQuestionWhereMathematicsMethodsAndAlgorithmMethodHaveToBeCombinedSoHereIsTheFlagZippingTheZipperIsNotTooHard}` (unintended)
