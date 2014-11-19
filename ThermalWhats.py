from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.debugger import Debugger

import threading,time, base64,os,sys
import subprocess
import urllib

from LibThermal import *
from PIL import Image

timeref = -120
printmode = 1

##Desconecting
def ondisconnected(error):
    time.sleep(2)
    methodsInterface.call("auth_login",("34668882592",base64.b64decode("aeZDgEteVv4J4Oi5RLfI3FHZYbg=")))
    methodsInterface.call("ready")
    methodsInterface.call("presence_sendAvailable")
    print "Reconnecting"

##Message delivered successfully
def onMessageDelivered(jid, messageId):
    methodsInterface.call("delivered_ack", (jid, messageId))

##Auth successfully
def onAuthSuccess(username):
    print "AUTH OK: " + username

##Receive message and print it
def onMessage(messageId,jid,content,timestamp,receiptRequested,name,b):
    global timeref
    global printmode
    methodsInterface.call("message_ack", (jid, messageId))

    if content == "END":
        t.printLines(2)
        t.cutPaper()
        return
    
    if content == "MODE1":
        printmode = 1
        methodsInterface.call("message_send", (jid, "Modo 1: impresion normal "))
        return
    elif content == "MODE2":
        printmode = 2
        methodsInterface.call("message_send", (jid, "Modo 2: impresion para iPhone"))
        return
    elif content == "MODE3":
        printmode = 3
        methodsInterface.call("message_send", (jid, "Modo 3: impresion larga"))
        return
    elif content == "MODE4":
        printmode = 4
        methodsInterface.call("message_send", (jid, "Modo 4: impresion completa (mucho gasto de papel)"))
        return
    
    if time.time() - timeref > 120:
        t.printLines(1)
        t.smallFont(1)
        t.textAling(1)
        t.println(time.strftime("%d/%m/%Y %H:%M:%S"))
        t.smallFont(0)
        t.textAling(0)
        timeref = time.time()
        #t.dotSeparator(0x08)

    t.emphatised(1)
    t.printnln(name+ ": ")
    t.emphatised(0)
    t.println(content)
    print name + ": " +content
    methodsInterface.call("message_send", (jid, "Recibido ;)"))

##Receive image and print it
def onimage_received(messageId,jid,preview,url,size,receiptRequested,a):
    urllib.urlretrieve (url, messageId + ".jpg")
    try:
        im = Image.open(messageId + ".jpg")
        #t.dotSeparator(0x08)
        t.println("Imagen recibida a: " + time.strftime("%d/%m/%Y %H:%M:%S"))
        t.println("Modo de impresion: " + str(printmode))
        #t.dotSeparator(0x08)
        t.cutPaper()
        
        if printmode == 1:
            t.printBitmap(im,1)
        elif printmode == 2:
            t.printiPhoneBitmap(im)
        elif printmode == 3:
            t.printLargeBitmap(im)
        elif printmode == 4:
            t.printCompleteBitmap(im)


        t.printLines(4)
        t.cutPaper()
        methodsInterface.call("message_send", (jid, "Foto imprimida. Gracias!"))
    except:
        methodsInterface.call("message_send", (jid, "Error en la foto!"))
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
        methodsInterface.call("message_ack", (jid, messageId))

##Audio receive and download
def onaudio_received(messageId,jid,url,size,receiptRequested,a):
    urllib.urlretrieve (url, messageId + ".acc")
    methodsInterface.call("message_ack", (jid, messageId))
    #avconv -i 1402571446-347.acc -ar 16000 out.flac
    #curl -X POST -H 'Content-Type:audio/x-flac; rate=16000' -T out.flac 'https://www.google.com/speech-api/v2/recognize?lang=es&maxresults=10&pfilter=0&key=AIzaSyCGRH-QgpLZyHy0SlIIJS30oolFCUXk5S0'


##Init Yowsup and Thermal Printer
t = Thermal("/dev/serial/by-id/usb-0d3a_0368-if00")
y = YowsupConnectionManager()
y.setAutoPong(True)
Debugger.enabled = False
methodsInterface = y.getMethodsInterface()
signalsInterface = y.getSignalsInterface()

##Regiter listeners
signalsInterface.registerListener("auth_success", onAuthSuccess)
signalsInterface.registerListener("message_received", onMessage)
signalsInterface.registerListener("disconnected", ondisconnected)
signalsInterface.registerListener("image_received", onimage_received)
signalsInterface.registerListener("audio_received", onaudio_received)
signalsInterface.registerListener("receipt_messageDelivered", onMessageDelivered)

##Auth
methodsInterface.call("auth_login", ("34668882592",base64.b64decode("aeZDgEteVv4J4Oi5RLfI3FHZYbg=")))
methodsInterface.call("ready")

##Profile photo and Status
methodsInterface.call("profile_setStatus",("Ticketing",))
#methodsInterface.call("profile_setPicture",("RaspiLogo.jpg",))
methodsInterface.call("presence_sendAvailable")

##Infinite loop
while True:
    try:
        s = raw_input()
        t.println("Operador: " + s)
    except KeyboardInterrupt:
        print "Saliendo..."
        t.cutPaper()
        t.close()
        sys.exit(0)

