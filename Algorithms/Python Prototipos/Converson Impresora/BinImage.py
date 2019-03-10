from PIL import Image

foto=Image.open('Imagen.bmp')
if foto.mode != 'L':
    foto=foto.convert('L')

umbral=70 #0 y 100%

#0% todo Blanco
#100% todo Negro

umbral = (umbral/100)*256
datos=foto.getdata()
datos_binarios=[]

for x in datos:
    if x<umbral:
        datos_binarios.append(0)
        continue
    datos_binarios.append(1)

nueva_imagen=Image.new('1', foto.size)
nueva_imagen.putdata(datos_binarios)
nueva_imagen.save('ImagenConvertida.bmp')

nueva_imagen.close()
foto.close()