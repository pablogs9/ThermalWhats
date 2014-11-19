import serial
import time
from math import ceil
from math import floor
from numpy import matrix
from PIL import Image

class Thermal:
    """ThermalPrinter Controller Class"""
    
    def __init__(self, device):
        self.ser = serial.Serial(port=device,
                                 baudrate=115200,
                                 bytesize=8,
                                 parity="N",
                                 stopbits=1,
                                 timeout=0.1,
                                 xonxoff=0,
                                 rtscts=0,
                                 dsrdtr=1,
                                 interCharTimeout=0.01
                                 )
        self.ser.write([0x1B,0x52,0x07])


    def close(self):
        self.ser.flush()
        self.ser.close()
    
    def writeBytes(self,bytes):
        self.ser.write(bytes)
        self.ser.flush()

    def emphatised(self,value):
        if value == 1:
            self.ser.write([0x1B,0x45,0x01])
        
        else:
            self.ser.write([0x1B,0x45,0x00])
        self.ser.flush()

    def cutPaper(self):
        self.ser.write([0x1D,0x56,0x00])
        self.ser.flush()

    def println(self,s):
        self.ser.write(s + "\n")
        self.ser.flush()
    
    def printnln(self,s):
        self.ser.write(s)
        self.ser.flush()
    
    def printLines(self,n):
        self.ser.write([0x1B,0x64,n])
    
    
    def underline(self,value):
        if value == 1:
            self.ser.write([0x1B,0x2D,0x01])
        else:
            self.ser.write([0x1B,0x2D,0x00])
        self.ser.flush()
    
    def textAling(self,value):
        if value == 1:
            self.ser.write([0x1B,0x61,0x01])
        elif value == 2:
            self.ser.write([0x1B,0x61,0x02])
        else:
            self.ser.write([0x1B,0x61,0x00])
        self.ser.flush()

    def smallFont(self,value):
        if value == 1:
            self.ser.write([0x1B,0x4D,0x01])
        else:
            self.ser.write([0x1B,0x4D,0x00])
        self.ser.flush()

    def textOrientation(self,value):
        if value == 1:
            self.ser.write([0x1B,0x54,0x01])
        elif value == 2:
            self.ser.write([0x1B,0x54,0x02])
        elif value == 3:
            self.ser.write([0x1B,0x54,0x03])
        else:
            self.ser.write([0x1B,0x54,0x00])
        self.ser.flush()

    def rotation(self,value):
        if value == 1:
            self.ser.write([0x1B,0x56,0x01])
        else:
            self.ser.write([0x1B,0x56,0x00])
        self.ser.flush()

    def reversePrinting(self,value):
        if value == 1:
            self.ser.write([0x1B,0x7B,0x01])
        else:
            self.ser.write([0x1B,0x7B,0x00])
        self.ser.flush()

    def charSize(self,h,v):
        h = h % 8;
        v = v % 8;
        size = ((h << 4) & 0xF0) | (v & 0x0F)
        self.ser.write([0x1D,0x21,size])
        self.ser.flush()

    def invert(self,value):
        if value == 1:##;
            self.ser.write([0x1B,0x42,0x01])
        else:
            self.ser.write([0x1B,0x42,0x00])
        self.ser.flush()

    ## Separators 0x80 -> top
    def separator(self,value):
        self.ser.write([0x1D,0x2A,0x20,0x1])
        self.ser.flush()
        self.ser.write([value & 0xFF]*256)
        self.ser.flush()
        self.ser.write([0x1D,0x2F,0x03])
        self.ser.flush()

    def dotSeparator(self,value):
        self.ser.write([0x1D,0x2A,0x20,0x1])
        self.ser.flush()
        self.ser.write([value & 0xFF,0x0]*128)
        self.ser.flush()
        self.ser.write([0x1D,0x2F,0x03])
        self.ser.flush()

    def printBitmap(self,im,value):
        w, h = im.size
        if w > 256 and h > 256:
            if w > h:
                im = im.crop(((w-h)/2,0,h+(w-h)/2,h))
            elif h > w:
                im = im.crop((0,(h-w)/2,w,w+(h-w)/2))
            
            im = im.resize((256,256))
        elif w > 256 or h > 256:
            im.thumbnail((256,256),Image.ANTIALIAS)
        
        im = im.convert('1')
        w, h = im.size

        self.ser.write([0x1D,0x2A,int(ceil(w/8.0)),int(ceil(h/8.0))])
        self.ser.flush()
        for j in range(int(ceil(w/8.0))*8):
            for i in range(0,int(ceil(h/8.0))*8,8):
                data = 0
                desp = 7
                for p in range(8):
                    try:
                        if im.getpixel((j,p+i)) == 0:
                            data |= 1 << desp
                    except:
                        data |= 0 << desp
                    desp = desp - 1
                self.ser.write([data])
        self.ser.flush()
        
        if value == 1:
            self.ser.write([0x1D,0x2F,0x03])
        else:
            self.ser.write([0x1D,0x2F,0x00])
        self.ser.flush()

    def printLargeBitmap(self,im):
        w, h = im.size
        if w > 256:
            im = im.crop(((w-256)/2,0,256+(w-256)/2,h))
        
        im = im.convert('1')
        w, h = im.size
        
        hAux = h
        
        k = 0
        while hAux > 0:
            if hAux > 256:
                imaux = im.crop((0,k*256,w,k*256+256))
                hAux = hAux - 256
            #print "Corto e imprimo de " + str((0,k*256)) + " a " + str((w,k*256+256)) + " filas: 256"
            else:
                imaux = im.crop((0,k*256,w,k*256+hAux))
                #print "Corto e imprimo de " + str((0,k*256)) + " a " + str((w,k*256+hAux)) + " filas: " + str(hAux)
                hAux = 0
            k = k + 1
            self.printBitmap(imaux,1)
            self.ser.flush()

    def printCompleteBitmap(self,im):
        im = im.convert('1')
        w, h = im.size
        #print "Imagen de " + str(w) + " por " + str(h)
        im = im.crop((0,0,int(floor(w/256.0))*256,h))
        
    
        w, h = im.size
        #print "Imagen de " + str(w) + " por " + str(h)
        wc = int(ceil(w/256.0))
        hc = int(ceil(h/256.0))
        #print "Tiras de papel: " + str(wc)
        #print "Cuadrados por tira: " + str(hc)
        
        for i in range(wc):
            hAux = h
            self.textAling(1)
            self.println("Tira " + str(i+1) + " de " + str(wc))
            self.printLines(1)
            self.textAling(0)
            self.cutPaper()
            for j in range(hc):
                if hAux > 256:
                    #print "Imprimiendo " + str(j) + "/" + str(i)
                    #print str(i*256) + "," + str(j*256) + " " + str(i*256+256) + "," + str(j*256+256)
                    imaux = im.crop((i*256,j*256,i*256+256,j*256+256))
                    hAux = hAux - 256
                else:
                    #print "Imprimiendo " + str(j) + "/" + str(i)
                    #print str(i*256) + "," + str(j*256) + " " + str(i*256+256) + "," + str(j*256+hAux)
                    imaux = im.crop((i*256,j*256,i*256+256,j*256+hAux))
                    hAux = 0
                self.printBitmap(imaux,1)
            self.printLines(4)
            self.cutPaper()

    def printiPhoneBitmap(self,im):
        w, h = im.size
        if w > 256:
            im.thumbnail((256,h*int(ceil(256.0/w))),Image.ANTIALIAS)
        im = im.convert('1')
        w, h = im.size
        
        hAux = h
        
        k = 0
        while hAux > 0:
            if hAux > 256:
                imaux = im.crop((0,k*256,w,k*256+256))
                hAux = hAux - 256
            #print "Corto e imprimo de " + str((0,k*256)) + " a " + str((w,k*256+256)) + " filas: 256"
            else:
                imaux = im.crop((0,k*256,w,k*256+hAux))
                #print "Corto e imprimo de " + str((0,k*256)) + " a " + str((w,k*256+hAux)) + " filas: " + str(hAux)
                hAux = 0
            k = k + 1
            self.printBitmap(imaux,1)
