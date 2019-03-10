@echo off
echo .-.       .-----.         .-. .-.        .---.             
echo : :       `-. .-'        .' `.: :        : .; :            
echo : :    .--. : :.-..-..--.`. .': :   .--. :   .' .--. .-..-.
echo : :__ ' '_.': :: :; :: ..': : : :_ ' '_.': .; :' .; :: :; :
echo :___.'`.__.':_;`.__.':_;  :_; `.__;`.__.':___.'`.__.'`._. ;
echo                                                       .-. :
echo                                                       `._.'
echo  .--.        .--. .-.                            
echo : .--'      : .-'.' `.                           
echo `. `.  .--. : `; `. .'.-..-..-. .--.  .--.  .--. 
echo  _`, :' .; :: :   : : : `; `; :' .; ; : ..'' '_.'
echo `.__.'`.__.':_;   :_; `.__.__.'`.__,_;:_;  `.__.'
echo                                                  
                                               
echo Hola, procederemos a generar los elementos necesarios para la puesta a punto del sofwtare
start python-3.5.0-amd64.exe
echo Presione Enter cuando el elemento este instalado
pause
start PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe
echo Asegurese de tener internet para el proximo paso, en caso de fallar ejecute solo el archivo Preliminares_2
pause 
start Preliminares_2.bat