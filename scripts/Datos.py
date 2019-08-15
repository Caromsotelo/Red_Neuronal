import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb
from matplotlib.pyplot import *
import collections, nump

#---------------------------------------------------READ THE FILES---------------------------------------------------------
datos=pd.read_csv('Data.csv',header =0,na_values='NaN')
carvajal=datos[[' Fecha y Hora              ',' Carvajal - Sevillana ']]

#-------------------------------------------Replace values less than 5 with NaN---------------------------------------------
for i in carvajal:
	if i <=5:
		carvajal=carvajal.replace([i], ['NaN'])
#---------------------------------------------Calculate the hourly average----------------------------------------------------
horas=['1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','00:00']
mean=[]
for i in horas:
	df=carvajal[carvajal[' Fecha y Hora              '].str.contains(i)==True]
	prom=np.nanmean(df[' Carvajal - Sevillana '])
	mean.append(prom)

#------------------------------------------------Plot the hourly average----------------------------------------------------
plt.figure(figsize=(13,7))
plt.plot(horas,mean,color='darkcyan',linewidth=2.5)
plt.title('Promedio horario de PM2.5 (2013-2019)',fontsize=18)
plt.xlabel('Hora',fontsize=16)
plt.xticks(rotation='vertical')
plt.ylabel('Concentracion[ug/m3]',fontsize=16) 
plt.grid(linewidth=0.3,color='k',linestyle=':')
plt.tight_layout()
plt.savefig('plots/promedio_horario.jpg')
plt.show()
