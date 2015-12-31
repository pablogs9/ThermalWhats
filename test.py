from LibThermal import *
t = Thermal("/dev/serial/by-id/usb-0d3a_0368-if00")
t.println("Normal")
t.cutPaper()
for i in range(256):
	t.writeBytes([i])
t.cutPaper()
