ThermalWhats
============

Just a Raspi connected to Whatsapp and to a thermal printer. 

This project uses a Raspberry Pi as a Whatsapp client (using Yowsup library) and thermal printer controller. 
For this second purpose I have developed a little ESC/POS python library which implements the main commands 
of this protocol. Nowadays you can text it and the system will print your text next to your Whatsapp nickname, 
and you also can send any image. It will process the image using python Image library in order to adjust size 
and apply some 1 bit dithering.

Really fun as cheap dirty photo printer or living room message system.

- I have copied Yowsup library in order to make things easier.
- LibThermal.py is the thermal library which implements ESC/POS commands.
- ThermalWhats.py is the main program that connects to the servers and to the printer. Here is where you have to COMPLETE your CREDENTIALS and the THERMAL PRINTER SERIAL ADDRESS. See Yowsup library to learn how to get your credentials.

Thermal Library
==============

The Thermal Library is implements lots of commands according to the ESC/POS standart:

- Start the serial connection with the printer
- Format text: emphatise, underline, align, character size, text rotation, inverted colors (white text and black background).
- Change between small or standard font size
- Resize and print bitmaps given as a arbitrary image format (JPEG,PNG...)

