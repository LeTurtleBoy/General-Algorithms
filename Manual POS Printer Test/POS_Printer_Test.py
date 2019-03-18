#!/usr/bin/python3
import serial as ps

puerto = ps.Serial(port='COM6', baudrate=115200, bytesize=ps.EIGHTBITS,
                   parity=ps.PARITY_NONE, stopbits=ps.STOPBITS_ONE, xonxoff=True)
begin = b'\x1C\x70\x01\n'
end = b'\n\n\n\n\n\x1D\x56\x31'
try:
    puerto.write(begin)
    message = \
        "! \" # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ " \
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \\ ] ^ _ ` a b " \
        "c d e f g h i j k l m n o p q r s t u v w x y z { | } ~".encode()
    puerto.write(message)
    puerto.write(end)

except ps.SerialException:
    print('Port is not available') 


print("Final")
print(puerto.get_settings())
puerto.close()
