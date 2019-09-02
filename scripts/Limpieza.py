import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb
from matplotlib.pyplot import *
import collections, numpy
from pylab import *
import glob

#---------------------------------------------------READ THE FILES---------------------------------------------------------
datos=pd.read_csv('Data.csv',header =0,na_values=np.nan)
est=[' Carvajal - Sevillana ',' Centro de Alto Rendimiento ',' Fontibon ',' Guaymaral ',' Kennedy  ',' Las Ferias ',' MinAmbiente ',' Puente Aranda ',' San Cristobal ',' Suba     ',' Tunal    ',' Usaquen ']
estacion=pd.DataFrame(datos[' Fecha y Hora              '])
horas=[' 1:00',' 2:00',' 3:00',' 4:00',' 5:00',' 6:00',' 7:00',' 8:00',' 9:00',' 10:00',' 11:00',' 12:00',' 13:00',' 14:00',' 15:00',' 16:00',' 17:00',' 18:00',' 19:00',' 20:00',' 21:00',' 22:00',' 23:00',' 00:00']
cont=1

for n in est:
	#----------------------------------------------Replace the values with NaN (<5)------------------------------------------------- 
	datos[n]= datos[n].astype(float)
	estacion=estacion.join(datos[n])
	for i in estacion[n]:
		if i <=5:
			estacion[n]=estacion[n].replace([i], [np.nan])
	#--------------------------------------------Calculate the hourly average, it's std and replace------------------------------------------------------
	mean=[]
	corre=pd.DataFrame()
	desup=[]
	desdo=[]
    
	for i in horas:
		df=estacion[estacion[' Fecha y Hora              '].str.contains(i)==True]
		prom=np.nanmean(df[n])
		df[n]=df[n].replace(np.nan,prom)
		mean.append(prom)
		des=np.std(df[n])
		dup=prom+des
		ddo=prom-des
		desup.append(dup)
		desdo.append(ddo)
		corre=corre.append(df)
	
	#------------------------------------Create a new Data Frame with the hourly average per station-------------------------------
	frame=pd.DataFrame(np.column_stack((horas, mean)))
	frame.columns=['HORA',n]
	frame.to_csv('promhora/Promedio_horario'+n+'.csv')
    #----------------------------------------Create a new Data Frame with the corrected data per station--------------------------------
	corre[' Fecha y Hora              ']= pd.to_datetime(corre[' Fecha y Hora              '])
	corre.index=corre[' Fecha y Hora              ']
	corre=corre.sort_index()
	corre.drop(corre.columns[0],axis=1,inplace=True)
	corre[n].to_csv('Datos_Corregidos'+n+'.csv',header=True)
    #-----------------------------------------Plot the hourly average per station without std-------------------------------------------------------
	#plt.figure(figsize=(13,7))
	#plt.plot(horas,mean,color='darkcyan',linewidth=2.5)
	#plt.axhline(y=25,xmin=0,xmax=1,color='k',linestyle=':',)
	#plt.title('Promedio horario (2013-2019)'+n)
	#plt.xlabel('Hora')
	#plt.xticks(rotation='vertical')
	#plt.ylabel('Concentracion[ug/m3]') 
	#plt.grid(linewidth=0.3,color='k',linestyle=':')
	#plt.tight_layout()
	#plt.savefig('plots/sin_std/promedio_horario'+n+'.png')
	#plt.show()
    
    #---------------------------------------- Plot the hourly average per station with std-------------------------------------------------
	#plt.figure(figsize=(13,7))
	#plt.plot(horas,mean,color='darkcyan',linewidth=2.5)
	#plt.plot(horas,desup,'--',color='r')
	#plt.axhline(y=25,xmin=0,xmax=1,color='k',linestyle=':',)
	#plt.plot(horas,desdo,'--',color='r')
	#plt.title('Promedio horario (2013-2019)'+n)
	#plt.xlabel('Hora')
	#plt.xticks(rotation='vertical')
	#plt.ylabel('Concentracion[ug/m3]') 
	#plt.grid(linewidth=0.3,color='k',linestyle=':')
	#plt.legend(('Promedio','Desviacion','Norma'))
	#plt.tight_layout()
	#plt.savefig('plots/std/promedio_horario_std'+n+'.png')
	#plt.show()
    
    #-----------------------------------------Plot the hourly average per station in a subplot-------------------------------------------
	plt.subplot(3,4,cont)
	plt.plot(horas,mean,color='darkcyan',linewidth=2.5)
	plt.plot(horas,desup,'--',color='r',linewidth=0.5)
	plt.axhline(y=25,xmin=0,xmax=1,color='k',linestyle=':',)
	plt.plot(horas,desdo,'--',color='r',linewidth=0.5)
	plt.xticks(fontsize=6)
	if cont <9:
		plt.xticks(horas,visible=False)
	if cont in [1,5,9]:
		plt.ylabel('Concentracion[ug/m3]')
	else:
		plt.yticks(visible=False)
	if cont >8:
		plt.xlabel('Hora')
	if cont ==4:
		plt.legend(('Promedio','Desviacion','Norma'))
	plt.suptitle('Promedio horario (2013-2019)')
	plt.title(n)
	plt.ylim(0,45)
	plt.xticks(rotation='vertical')
	plt.grid(linewidth=0.3,color='k',linestyle=':')
	plt.subplots_adjust(wspace=0)

	cont=cont+1

plt.show()

#--------------------------------------------Join the csv's with the corrected data in a csv--------------------------------------------
datos_corregidos= pd.DataFrame()
frames=[]

for f in glob.glob('Datos_Corregidos*'):
    csv = pd.read_csv(f)
    frames.append(csv)
datos_corregidos=pd.concat(frames,axis=1)
datos_corregidos=datos_corregidos.T.drop_duplicates().T
datos_corregidos.to_csv('Datos_Corregidos_totales.csv')

#------------------------------------------Join the csv's with the hourly average in a csv----------------------------------------------
Promedio_horario= pd.DataFrame()
frames2=[]

for g in glob.glob('promhora/Promedio_horario*'):
    csv2 = pd.read_csv(g)
    frames2.append(csv2)
Promedio_horario=pd.concat(frames2,axis=1)
Promedio_horario=Promedio_horario.T.drop_duplicates().T
Promedio_horario.to_csv('promhora/Promedio_horario_total.csv')


