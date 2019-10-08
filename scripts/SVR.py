import csv
import pdb
import pandas as pd
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
import skill_metrics as sm

fechas = []
pm_25 = []

def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader) # Omitir Nombres de Columna
        for row in csvFileReader:
            fechas.append(int(row[0].split('-')[0]))
            pm_25.append(float(row[1]))
    return

get_data('Tun.csv')

######## Febrero 
fechas = np.reshape(fechas,(len(fechas), 1))
fecha = np.arange(53402,53450)
real = pm_25[3402:3450]
fecha = np.reshape(fecha,(len(fecha), 1))
svr_rbf = SVR(kernel= 'rbf', C= 1e5, gamma= 0.1)
svr_rbf.fit(fechas, pm_25)
test = svr_rbf.predict(fecha)

######## Prueba
#fechprue = np.arange(57648,57660)
#fechprue = np.reshape(fechprue,(len(fechprue), 1))
#plt.plot(fechprue, svr_rbf.predict(fechprue))
#plt.show()

####### Noviembre
fechanov = np.arange(51626,51674)
realn = pm_25[1626:1674]
fechan = np.reshape(fechanov,(len(fechanov), 1))
testn = svr_rbf.predict(fechan)

####### Plot Feb
plt.scatter(fecha, real, color= 'black', label= 'Data') # datos iniciales 
plt.plot(fecha, test, color= 'red', label= 'Modelo RBF')# RBF kernel
plt.title('Tunal (Feb 14 y 15)')
#plt.plot(fechas,svr_lin.predict(fechas), color= 'green', label= 'Modelo Lineal') # lineal kernel
#plt.plot(fechas,svr_poly.predict(fechas), color= 'blue', label= 'Modelo Polinomial') # Polinomial kernel
plt.xlabel('Horas')
plt.ylabel('Concentracion de PM_25')
plt.legend()
plt.savefig('Tun_Feb_14-15.png')
plt.show()
plt.close()

####### Plot Nov
plt.scatter(fechan, realn, color= 'black', label= 'Data') # datos iniciales
plt.plot(fechan, testn, color= 'red', label= 'Modelo RBF')# RBF kernel
plt.title('Tunal (Nov 22 y 23)')
#plt.plot(fechas,svr_lin.predict(fechas), color= 'green', label= 'Modelo Lineal') # lineal kernel
#plt.plot(fechas,svr_poly.predict(fechas), color= 'blue', label= 'Modelo Polinomial') # Polinomial kernel
plt.xlabel('Horas')
plt.ylabel('Concentracion de PM_25')
plt.legend()
plt.savefig('Tun_Nov_22-23.png')
plt.show()
plt.close()

print('------ Febrero 14 y 15 de 2019 ------')
print(np.corrcoef(real,test))
print(sm.rmsd(test,np.array(real)))
print(sm.bias(test,np.array(real)))

print('------ Noviembre 22 y 23 de 2018 ------')
print(np.corrcoef(realn,testn))
print(sm.rmsd(testn,np.array(realn)))
print(sm.bias(testn,np.array(realn)))


##### Create files
## Feb
soda = {'SVR_tun':test.tolist()}
df = pd.DataFrame(soda, columns = ['SVR_tun'])
df.to_csv('tun_feb_svr.csv')

## Nov
soda = {'SVR_tun':test.tolist()}
df = pd.DataFrame(soda, columns = ['SVR_tun'])
df.to_csv('tun_nov_svr.csv')


