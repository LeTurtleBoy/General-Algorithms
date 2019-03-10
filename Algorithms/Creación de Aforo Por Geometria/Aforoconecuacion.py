import pandas as pd
import numpy as np

Aforo = pd.read_excel("Manual_Diesel.xlsx",header=None)
Aforo.drop(Aforo.index[:1], inplace=True)
Aforo.columns = ['m','g']
print(Aforo.tail())
M = Aforo.m.tolist()
G = Aforo.g.tolist()

m=np.linspace(0,230,2301)
NuevoAforodf = pd.DataFrame(m,columns=['Medida [cm]']);

NuevoAforo = []
for elemento in range(len(G)-1):
	Ma = G[elemento+1]
	Me = G[elemento]	
	for u in range(0,10):
		delta = (((Ma - Me)/10)*u)
		NuevoAforo.append(Me+delta)
NuevoAforo.append(Ma)

NuevoAforodf['Galones'] = NuevoAforo
print(NuevoAforodf.head(), NuevoAforodf.tail())

NuevoAforodf.to_excel("Aforo_detallado_corriente.xlsx",index=False)