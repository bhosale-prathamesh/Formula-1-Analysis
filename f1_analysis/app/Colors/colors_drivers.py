f = open('f1_analysis/app/Colors/2011_Drivers.txt','w')
d = {'VET':dict(color='#004c6c',dash='solid'),
                           'WEB':dict(color='#004c6c',dash='dash'),
                           
                           'HAM':dict(color='#FF8700',dash='solid'),
                           'BUT':dict(color='#FF8700',dash='dash'),
                           
                           'ALO':dict(color='#C00000',dash='solid'),
                           'MAS':dict(color='#C00000',dash='dash'),
                           
                           'ROS':dict(color='#00D2BE',dash='solid'),
                           'MSC':dict(color='#00D2BE',dash='dash'),
                           
                           'HEI':dict(color='#FFF500',dash='solid'),
                           'SEN':dict(color='#FFF500',dash='dash'),
                           'PET':dict(color='#FFF500',dash='dashdot'),
                           
                           'BAR':dict(color='#0082FA',dash='solid'),
                           'MAL':dict(color='#0082FA',dash='dash'),
                           
                           'SUT':dict(color='#F596C8',dash='solid'),
                           'DIR':dict(color='#F596C8',dash='dash'),
                           
                           'KOB':dict(color='#960000',dash='solid'),
                           'PER':dict(color='#960000',dash='dash'),
                           'DLR':dict(color='#960000',dash='dashdot'),
                           
                           'BUE':dict(color='#011AE3',dash='solid'),
                           'ALG':dict(color='#011AE3',dash='dash'),
                           
                           'KOV':dict(color='#000000',dash='solid'),
                           'TRU':dict(color='#000000',dash='dash'),
                           'CHA':dict(color='#000000',dash='dashdot'),
                           
                           'KAR':dict(color='#5d4b25',dash='solid'),
                           'RIC':dict(color='#5d4b25',dash='dash'),
                           'LIU':dict(color='#5d4b25',dash='dashdot'),
                           
                           'GLO':dict(color='#ff2e15',dash='solid'),
                           'DAM':dict(color='#ff2e15',dash='dash')
                          }
f.write(str(d))
f.close()

f = open('f1_analysis/app/Colors/2011_Constructors.txt','r')
data = f.read()
f.close()
print(eval(data))