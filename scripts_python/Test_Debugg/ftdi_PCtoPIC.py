from serial import Serial

ser = Serial("/dev/ttyUSB0", 115200)
ser.write((255).to_bytes())
ser.write((255).to_bytes())
