# depth_meter_test.py

from pymodbus.client import ModbusSerialClient as ModbusClient
import time

# Modbus RTU client setting
client = ModbusClient(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8)
  
initial_dip = 0 # flag for initial dipping
gain = 0 # gain value to adjust sensor's value

if client.connect():
    print('Connected successfully')
    try:
        while True:
            # from address 4, read 2 register
            response = client.read_holding_registers(address=4, count=1, slave=1)
            print(response)
            
            # time.sleep(0.1)
                
            if not response.isError():
                depth_of_water = response.registers[0]
                if initial_dip == 0 and depth_of_water > 0: # activated only when it is an initial dip and the value is more than 0
                    gain = depth_of_water
                    initial_dip = 1
                    
                print(f"depth of water : {depth_of_water - gain}cm", end='\r')
            else:
                print("Error reading registers at address 4", end='\r')
                
            # time.sleep(1)
    finally:
        client.close()
else:
    print("Failed to connect to the sensor")
