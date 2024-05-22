import serial
import time

SERIAL_PORT_TIME_OUT = 5

CONNECT_SUCCESS = 0
CONNECT_ELM327_FAIL = 1
CONNECT_CAN_BUS_FAIL = 2

ELM_RESET_PERIOD = 1

class ELM327:

	def __init__(self):
		pass

	def connect(self, port_name, buad_rate):
		try:
			self.serial_instance = serial.Serial(port_name, buad_rate)
			self.serial_instance.timeout = SERIAL_PORT_TIME_OUT
			self.serial_instance.write_timeout = SERIAL_PORT_TIME_OUT

			# reset device
			Response = self.GetResponse(b'AT Z\r')

			time.sleep(ELM_RESET_PERIOD)

			# Echo Off, for faster communications.
			Response = self.GetResponse(b'AT E0\r')
			
			# Linefeed off, for faster communications.
			Response = self.GetResponse(b'AT L0\r')

			# Responses on, for format recognition.
			Response = self.GetResponse(b'AT R1\r')

			# Headers off, for format recognition.
			Response = self.GetResponse(b'AT H0\r')

			# Set CAN communication protocol to ISO 9141-2 or auto detect on fail.
			# Response = self.GetResponse(b'AT SP A3\r')

			# Set CAN Baud to high speed.
			# Response = self.GetResponse(b'AT IB 10\r')


		except Exception as e:
			return CONNECT_ELM327_FAIL

		# get any packet to connection with obd
		Response = self.GetResponse(b'0101\r')
		
		if Response.find("UNABLE TO CONNECT") != -1:
			return CONNECT_CAN_BUS_FAIL

		return CONNECT_SUCCESS

	def disconnect(self):

		self.serial_instance.close()

	def GetResponse(self, Data):

		self.serial_instance.write(Data)
		Response = ""
		ReadChar = 1
		while ReadChar != b'>' and ReadChar != b'' and ReadChar != 0:
			ReadChar = self.serial_instance.read()
			if ReadChar[0] > 127:
				pass
			elif ReadChar != b'>':
				Response += str(ReadChar, 'utf-8')

		# print(f"\n{Data}")
		# print(f"{Response}")
		
		# Result = Response.replace('\r', '\n').replace('\n\n', '\n').replace('NO DATA', '00000000000000')
		# if Result[-1:] != '\n':
		# 	Result += '\n'

		return Response

	def getData(self):

		infograph_data = dict()

		# Throttle percentage
		throttle_pos = self.GetResponse(b'01 11\r')
		throttle_pos_val = int(int(throttle_pos.split()[2], 16) * 0.39)
		infograph_data["throttle_pos"] = throttle_pos_val

		# Engine RPM
		rpm = self.GetResponse(b'01 0C\r')
		a = int(rpm.split()[2], 16)
		b = int(rpm.split()[3], 16)
		rpm_val = (256 * a + b) / 4
		infograph_data["rpm"] = rpm_val

		# Speed
		speed = self.GetResponse(b'01 0D\r')
		speed_val = int(speed.split[2], 16)
		infograph_data["speed"] = speed_val

		# Eng Oil Temp
		eng_oil_temp = self.GetResponse(b'01 5C\r')
		eng_oil_temp_val = int(eng_oil_temp.split[2], 16) - 40
		infograph_data["eng_oil_temp"] = eng_oil_temp_val

		# Air Fuel Ratio
		air_fuel_ratio = self.GetResponse(b'01 44\r')
		a = int(rpm.split()[2], 16)
		b = int(rpm.split()[3], 16)
		air_fuel_ratio_val = 0.0078125 * a + 0.000030518 * b
		infograph_data["air_fuel_ratio"] = air_fuel_ratio_val

		# Fuel Rate
		fuel_rate = self.GetResponse(b'01 5E\r')
		a = int(rpm.split()[2], 16)
		b = int(rpm.split()[3], 16)
		fuel_rate_val = 12.8 * a + 0.05 * b
		infograph_data["fuel_rate"] = fuel_rate_val

		# Fuel Injection Timing
		fuel_inj = self.GetResponse(b'01 5D\r')
		a = int(rpm.split()[2], 16)
		b = int(rpm.split()[3], 16)
		fuel_inj_val = (2 * a + 0.0078125 * b) - 210
		infograph_data["fuel_inj"] = fuel_inj_val 

		# Fuel Pressure 
		fuel_pres = self.GetResponse(b'01 0A\r')
		fuel_pres_val = 3 * int(fuel_pres.split()[2], 16)
		infograph_data["fuel_pres"] = fuel_pres_val

		# Battery
		battery = self.GetResponse(b'AT RV\r')
		infograph_data["battery"] = int(battery)

		# Engine Load
		load = self.GetResponse(b'01 04\r')
		infograph_data["load"] = 0.0078125 * int(load.split()[2])

		# Engine Torque
		torque = self.GetResponse(b'01 61\r')
		infograph_data["torque"] = int(torque.split()[2], 16) - 125

		# Air Temp
		air_temp = self.GetResponse(b'01 0F\r')
		infograph_data["air_temp"] = int(air_temp.split()[2], 16) - 40

		# Air pressure
		air_press = self.GetResponse(b'01 0B\r')
		infograph_data["air_press"] = int(air_press.split()[2], 16)

		# Air Flow rate
		air_flow_rate = self.GetResponse(b'01 10\r')
		a = int(air_flow_rate.split()[2], 16)
		b = int(air_flow_rate.split()[3], 16)
		air_flow_rate_val = 2.56 * a + 0.01 * b
		infograph_data["air_flow_rate"] = air_flow_rate_val

		# Coolant temp
		coolant_temp = self.GetResponse(b'01 05\r')
		infograph_data["coolant_temp"] = int(coolant_temp.split()[2], 16) - 40


		return infograph_data

def main():
    pass

if __name__ == '__main__':
    main()