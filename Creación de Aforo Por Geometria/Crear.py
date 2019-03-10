import pandas as pd
import numpy as np

def Volumen(i):
	return (i/1000)*1000*np.pi*(0.8354926666)**2

x = [0,0]
i = 0

Aforo = []
for i in range(0,2710,1):
	Aforo.append([i, Volumen(i)])
map(Aforo, zip(*Aforo))

AforoReal=pd.DataFrame(Aforo,columns = ['Medida [mm]','Volumen [l]'])
print(AforoReal.head())
AforoReal.to_excel('AforoTanqueUrea.xlsx',index=False)