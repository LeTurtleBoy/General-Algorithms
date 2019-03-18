import pandas as pd
from math import pi


r = 0.8354926666
volumen = lambda h,r : h*(pi*(r)**2)
Aforo = [[h, volumen(h,r)] for h in range(0,2710,1)]

map(Aforo, zip(*Aforo))
AforoReal=pd.DataFrame(Aforo,columns = ['Medida [mm]','Volumen [l]'])
AforoReal.to_excel('AforoTanqueUrea.xlsx',index=False)