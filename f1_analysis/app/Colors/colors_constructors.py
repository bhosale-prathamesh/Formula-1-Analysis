f = open('f1_analysis/app/Colors/2011_Constructors.txt','w')
d = {'Red Bull':dict(color='#004c6c'),
                    'McLaren':dict(color='#FF8700'),
                    'Ferrari':dict(color='#C00000'),
                    'Mercedes':dict(color='#00D2BE'),
                    'Renault':dict(color='#FFF500'),
                    'Williams':dict(color='#0082FA'),
                    'Toro Rosso':dict(color='#011AE3'),
                    'Force India':dict(color='#F596C8'),
                    'Lotus':dict(color='#000000'),
                    'Sauber':dict(color='#960000'),
                    'HRT':dict(color='#5d4b25'),
                    'Virgin':dict(color='#ff2e15')
                   }
f.write(str(d))
f.close()

f = open('f1_analysis/app/Colors/2011_Constructors.txt','r')
data = f.read()
f.close()
print(eval(data)['McLaren'])