
from z3 import *
import hashlib

len = 0x25
s = Solver()
vec = ""
for i in xrange(0, len):
    vec += "pw[{}] ".format(i)

m = BitVecs(vec, 8)
for i in range(len):
    s.add(m[i] >= 0x20)
    s.add(m[i] <= 0x7F)


s.add(m[3] == m[8])
s.add(m[29] == m[26])
s.add(m[35]-48 + m[36] - 48 == m[19] - 48+1)
s.add((m[36]-48) - (m[25]- 48) == 0)
s.add((m[6]) - (m[2]) == 0)
s.add(m[0] == m[13])
s.add(m[12] == m[8])
s.add(m[16] == m[26])
s.add(m[3] == m[26])
s.add(m[3] == 95)
s.add(m[30] == m[27])
s.add(m[0] == 84)
s.add(m[4] + m[5] == 188)
s.add(m[0] + m[1] == 188)
s.add(m[7] == 103)
s.add(m[9]+1 == m[7])
s.add(m[9]+12 == m[11])
s.add(m[14] == 49)
s.add(m[15] == 36)
s.add(m[17] == 67)
s.add(m[18] == 104)
s.add(m[23] == m[31])
s.add(m[31] - m[30] == 61)
s.add(m[7] == m[24])
s.add(m[28] == 122)
s.add(m[32] == 68)
s.add(m[33] == 48)
s.add(m[34] == 77)


#Koreksi
s.add(m[2]==ord('3'))
s.add(Or(m[10]==ord('o'), m[10]==ord('0')))
s.add(m[19]==ord('4'))
s.add(m[4]==ord('P'))
s.add(m[20] == m[21])
s.add(Or(m[20]==ord('1'), m[20]==ord('l')))
s.add(m[10] == ord('0'))
s.add(m[25]==ord('3'))
s.add(m[27] == ord('1'))
s.add(m[28] == ord('z'))
s.add(m[22] == ord('4'))
while s.check() == sat:
    model = s.model()
    out = ""
    nope = []
    for i in m:
        if str(i):
            out += chr(model[i].as_long())
        nope.append(i!=model[i])
    
    s.add(Or(nope[:-1]))
    # s.add(Th3_Pl3g_f0r_T1$_Ch4114ng3_1z_1nD0M13)
    print out
    if hashlib.md5(out).hexdigest() == 'b7575a9d0a6bc912480b28ef3597c444':
        print("[found] %s"%out)
        exit()