from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.debugger import Debugger

import threading,time, base64,os
import subprocess
import urllib

from LibThermal import *
from PIL import Image

##Desconecting
def ondisconnected(error):
	methodsInterface.call("auth_login",("",base64.b64decode(""))) #Use here your whatsapp credentials
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
    methodsInterface.call("message_ack", (jid, messageId))
    if content == "END":
        t.printLines(2)
        t.cutPaper()
        return
    t.emphatised(1)
    t.printnln(name+ ": ")
    t.emphatised(0)
    t.println(content)
    print name + ": " +content
    methodsInterface.call("message_send", (jid, "Recibido ;)"))

##Receive image and print it
def onimage_received(messageId,jid,preview,url,size,receiptRequested,a):
    urllib.urlretrieve (url, messageId + ".jpg")
    im = Image.open(messageId + ".jpg")
    t.cutPaper()
    t.printBitmap2(im,1)
    t.printLines(4)
    t.cutPaper()
    methodsInterface.call("message_ack", (jid, messageId))
    methodsInterface.call("message_send", (jid, "Foto imprimida. Gracias!"))

##Audio receive and download
def onaudio_received(messageId,jid,url,size,receiptRequested,a):
    urllib.urlretrieve (url, messageId + ".acc")
    methodsInterface.call("message_ack", (jid, messageId))

##Init Yowsup and Thermal Printer
t = Thermal("/dev/serial/by-id/usb-0d3a_0368-if00"); #Use here you own thermal printer mount point
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
methodsInterface.call("auth_login", ("",base64.b64decode(""))) #Use here your whatsapp credentials
methodsInterface.call("ready")

##Profile photo and Status
methodsInterface.call("profile_setStatus",("Ticketing",))
#methodsInterface.call("profile_setPicture",("RaspiLogo.jpg",))
methodsInterface.call("presence_sendAvailable")

##Infinite loop
while True:
    s = raw_input()
