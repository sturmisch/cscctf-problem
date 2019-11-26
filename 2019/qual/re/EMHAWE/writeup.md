# EMHAWE
This is a  EMHAWE writeup from CTF CSC 2019
 ```
  _____ __  __   _   _    ___        _______ 
| ____|  \/  | | | | |  / \ \      / / ____|
|  _| | |\/| | | |_| | / _ \ \ /\ / /|  _|
| |___| |  | | |  _  |/ ___ \ V  V / | |___
|_____|_|  |_| |_| |_/_/   \_\_/\_/  |_____|
```
Pada soal ini kita diberikan sebuah rar berisikan file .jar dan run bat nya. 
Kemudian kita menggunakan online tools Java Decompilers (www.javadecompilers.com) untuk membuka file jar tersebut. 
```
|--EMHAWE
  |-- character
  |-- ctfcsc
```
Didapatkan 2 buah package java yang berisi class yang sudah didecompile di dalamnya, 
```
|-- character
  |-- Inventory.java
|-- ctfcsc
  |-- Dragon.java
  |-- ElderDragon.java
  |-- Main.java
  |-- Monster.java
  |-- MonsterLibrary.java
  |-- SmallMonster.java
 ``` 
 
Kemudian kita lakukan Analisa dari Main.java di package ctfcsc. 
```java
if (choose == 1) {
                header(Main.health, Main.attack);
                System.out.println("Choose your monster:");
                System.out.println("1. Small Monster");
                System.out.println("2. Dragon");
                System.out.println("3. Elder Dragon");
                System.out.println("4. Back to menu");
                System.out.print(">> ");
                choice = Main.scan.nextInt();
                Main.scan.nextLine();
                if (choice != 4) {
                    MonsterLibrary.generateMonster(choice);
                    this.result = Monster.fighting(Main.health, Main.attack, choice);
                    if (this.result > 0) {
                        System.out.println("Mission Clear");
                        Main.scan.nextLine();
                        if (Inventory.randomDrop(choice) != 0) {
                            Inventory.printDrop(choice);
                        }
                    }
                    else {
                        System.out.println("Mission Failed");
                        Main.scan.nextLine();
                    }
                    MonsterLibrary.monsLib.clear();
                }
            }
```
Pada Main.java kita dapat mengetahui bahwa ada item yang seharusnya di dapatkan pada game ini, 
yang di proses pada class Inventory, sehingga kita akan melakukan Analisa pada Inventory.java .
  
Dari class Inventory terdapat function Scroll Generate yang didalamnya terdapat sesuatu variable yang dilakukan pengolahan, 
yang bisa jadi merupakan flag yang kita cari.

```java
public static int scrollGenerate(final int scroll) {
        if (scroll == 1) {
            final String scrollSmall = SmallMonster.scrollSmall;
        }
        else if (scroll == 2) {
            for (int i = 0; i < 1; ++i) {
                for (int j = 0; j < Dragon.Dragoon.length; ++j) {
                    Dragon.Dragoon[j] = Dragon.Dragoon[j];
                }
                for (int j = 0; j < Dragon.Dragoon.length; ++j) {
                    ElderDragon.elderr[j] = ElderDragon.elderr[j];
                }
            }
        }
        else if (scroll == 3) {
            for (int k = 0; k < Dragon.Dragoon.length; ++k) {
                Monster.monss[k] ^= 0x3;
            }
            for (int k = 0; k < Dragon.Dragoon.length; ++k) {
                MonsterLibrary.monslibb[k] ^= 0x1;
            }
            for (int k = 0; k < Dragon.Dragoon.length; ++k) {
                Main.flagg[k] ^= 0x7A69;
            }
        }
        return scroll;
    }
```
Oleh dari itu kita membuat solver menggunakan python seperti ini. 

```python
flagg = [31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31285, 31286, 31285, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31253, 31286, 31286, 31286, 31286, 31286, 31253, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31253, 31286, 31286, 31286, 31286, 31286, 31253, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31253, 31286, 31286, 31286, 31286, 31286, 31253, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31305, 31253, 31286, 31286, 31286, 31302, 31305, 31305, 31305, 31305, 31305, 31305, 31302, 31286, 31302, 31305, 31305]
dragoon = [32, 32, 32, 95, 95, 95, 32, 95, 95, 95, 32, 95, 95, 95, 32, 47, 32, 47, 95, 95, 32, 47, 32, 95, 32, 92, 32, 32, 95, 95, 124, 32, 124, 95, 95, 95, 32, 47, 32, 32, 95, 95, 124, 32, 124, 32, 95, 95, 32, 32, 32, 32, 32, 32, 95, 47, 32, 124, 32, 124, 95, 124, 32, 124, 95, 95, 32, 32, 32, 32, 32, 32, 32, 32, 124, 32, 124, 124, 32, 124, 124, 32, 124, 95, 95, 32, 32, 32, 95, 95, 95, 95, 32, 95, 32, 32, 32, 32, 124, 32, 124, 32, 124, 124, 32, 124, 32, 32, 95, 32, 95, 95, 32, 32, 47, 32, 95, 95, 95, 124, 95, 32, 32, 32, 95, 32, 32, 95, 95, 32, 95, 32, 32, 95, 95, 32, 95, 124, 95, 95, 95, 32, 47, 92, 32, 92, 32 ]
elder = [32, 32, 47, 32, 95, 95, 47, 32, 95, 95, 47, 32, 95, 95, 124, 32, 47, 32, 95, 95, 124, 32, 124, 32, 124, 32, 124, 47, 32, 95, 96, 32, 124, 32, 124, 95, 32, 92, 32, 47, 32, 95, 96, 32, 124, 32, 92, 32, 92, 32, 47, 92, 32, 47, 32, 47, 32, 124, 32, 95, 95, 124, 32, 39, 95, 32, 92, 32, 32, 32, 32, 95, 32, 32, 124, 32, 124, 124, 32, 124, 124, 32, 124, 92, 32, 92, 32, 47, 32, 47, 32, 95, 96, 32, 124, 32, 32, 32, 124, 32, 124, 32, 124, 124, 32, 124, 95, 124, 32, 39, 95, 32, 92, 124, 32, 124, 32, 32, 95, 124, 32, 124, 32, 124, 32, 124, 47, 32, 95, 96, 32, 124, 47, 32, 95, 96, 32, 124, 32, 124, 95, 32, 92, 32, 124, 32, 124, 32 ]
monss = [35, 127, 35, 43, 92, 127, 35, 43, 92, 127, 35, 43, 92, 63, 35, 63, 35, 43, 92, 92, 127, 35, 127, 92, 127, 35, 127, 35, 43, 92, 127, 35, 127, 92, 92, 92, 42, 35, 127, 35, 43, 92, 127, 35, 127, 35, 35, 95, 35, 85, 35, 35, 85, 35, 44, 127, 35, 127, 35, 127, 92, 127, 35, 127, 35, 127, 35, 127, 35, 35, 127, 35, 127, 92, 127, 35, 127, 127, 92, 92, 35, 35, 35, 92, 95, 35, 85, 35, 44, 35, 43, 92, 127, 35, 127, 35, 35, 35, 127, 35, 127, 92, 92, 35, 35, 35, 92, 127, 35, 127, 35, 127, 35, 127, 35, 127, 92, 127, 35, 127, 35, 127, 92, 127, 35, 127, 35, 43, 92, 127, 35, 127, 35, 43, 92, 127, 35, 127, 92, 92, 92, 42, 35, 127, 35, 61, 35, 61 ]
monslib = [33, 33, 93, 94, 94, 94, 93, 94, 94, 94, 93, 94, 94, 94, 125, 33, 93, 94, 94, 94, 125, 93, 94, 94, 94, 46, 33, 93, 94, 94, 45, 94, 125, 94, 94, 94, 94, 46, 33, 93, 94, 94, 45, 94, 125, 94, 94, 94, 93, 94, 46, 93, 94, 46, 33, 125, 94, 125, 93, 94, 94, 125, 94, 125, 33, 125, 94, 125, 94, 94, 94, 93, 94, 94, 94, 46, 33, 33, 33, 33, 125, 94, 125, 33, 33, 93, 94, 46, 33, 93, 94, 94, 45, 94, 125, 94, 94, 94, 125, 94, 125, 33, 33, 125, 94, 125, 33, 125, 94, 125, 33, 125, 94, 125, 93, 94, 94, 94, 94, 125, 93, 94, 94, 45, 94, 125, 93, 94, 94, 45, 94, 125, 93, 94, 94, 45, 33, 125, 94, 94, 94, 94, 46, 33, 125, 33, 125, 33]
small = "                __    ___      _ _____     _            _ _   _            _  _  _                 _ _  _          ____                   _______   "

print(small)
for i in dragoon: 
    print(chr(i),end="")
print("")
for i in elder:
    print(chr(i),end="")
print("")
for i in monss:
     print(chr(i^3),end="")
print("")
for i in monslib:
     print(chr(i^1),end="")
print("")
for i in flagg:
    print(chr(i^0x7A69),end="")

```
Dan Hasilnya adalah
```
                __    ___      _ _____     _            _ _   _            _  _  _                 _ _  _          ____                   _______
   ___ ___ ___ / /__ / _ \  __| |___ /  __| | __      _/ | |_| |__        | || || |__   ____ _    | | || |  _ __  / ___|_   _  __ _  __ _|___ /\ \
  / __/ __/ __| / __| | | |/ _` | |_ \ / _` | \ \ /\ / / | __| '_ \    _  | || || |\ \ / / _` |   | | || |_| '_ \| |  _| | | |/ _` |/ _` | |_ \ | |
 | (_| (_| (_< < (__| |_| | (_| |___) | (_| |  \ V  V /| | |_| | | |  | |_| ||__   _\ V / (_| |   | |__   _| | | | |_| | |_| | (_| | (_| |___) | > >
  \___\___\___| \___|\___/ \__,_|____/ \__,_|___\_/\_/ |_|\__|_| |_|___\___/    |_|  \_/ \__,_|___|_|  |_| |_| |_|\____|\__,_|\__,_|\__, |____/ | |
               \_\                         |_____|                |_____|                    |_____|                                |___/      /_/
```
Flag is CCC{c0d3d_w1th_J4va_l4nGuag3}
