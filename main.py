
import sys
import time

from PyQt5.QtWidgets import QMainWindow, QApplication 
from PyQt5.QtCore import QTimer
import qtmodern
from qtmodern import styles
from qtmodern import windows

import ELM327
import dashboard_ui


class OBDSniffGUI(QMainWindow, dashboard_ui.Ui_MainWindow):

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# self.showMaximized()

		self.connectButton.clicked.connect(self.connect)
		self.disconnectButton.clicked.connect(self.disconnect)
		self.startButton.clicked.connect(self.start)
		self.stopButton.clicked.connect(self.stop)

		self.elm327 = ELM327.ELM327()

		self.timer = QTimer(self)

		self.timer.timeout.connect(self.getDataStream)
  
	def getDataStream(self):
		infograph_data = self.elm327.getData()

		self.throttle.setValue(infograph_data["throttle_pos"] * 10)

		self.rpm.setValue(int((infograph_data["rpm"] * 1000) / 12000))

		self.speed.setValue(infograph_data["speed"])

		self.air_fuel_ratio.setText(str(infograph_data["air_fuel_ratio"]))
		self.fuel_inj.setText(str(infograph_data["fuel_inj"]))
		self.battery.setText(str(infograph_data["battery"]))
		self.load.setText(str(infograph_data["load"]))
		self.air_temp.setText(str(infograph_data["air_temp"]))
		self.air_press.setText(str(infograph_data["air_press"]))
		self.air_flow_rate.setText(str(infograph_data["air_flow_rate"]))
		self.coolant_temp.setText(str(infograph_data["coolant_temp"]))

	def start(self):
		self.timer.start(50)
		self.log_view.addItem(f"=> Fetching data ...")
		self.stopButton.setEnabled(True)

	def stop(self):
		self.timer.stop()
		self.log_view.addItem(f"=> Stopped fetching ...")


	def connect(self):

		self.log_view.clear()

		port_name = self.port_name.text()
		baud_rate = self.baud_rate.text()

		if port_name == "":
			self.log_view.addItem(f"=> Using default port")
			port_name = self.port_name.placeholderText()

		if baud_rate == "":
			self.log_view.addItem(f"=> Using default rate")
			baud_rate = self.baud_rate.placeholderText()

		self.log_view.addItem(f"=> Port Name: {port_name}")
		self.log_view.addItem(f"=> Baud Rate: {baud_rate}")

		connection_result = self.elm327.connect(port_name, baud_rate)

		if connection_result == ELM327.CONNECT_SUCCESS:
			self.log_view.addItem(f"=> ELM327 Connected")
			self.log_view.addItem(f"=> OBD Connected")
			self.startButton.setEnabled(True)
			self.disconnectButton.setEnabled(True)
			self.conn_status.setText("Connected")
		elif connection_result == ELM327.CONNECT_ELM327_FAIL:
			self.log_view.addItem(f"=> ELM327 connection failed")
			self.conn_status.setText("Disconnected")
		elif connection_result == ELM327.CONNECT_CAN_BUS_FAIL:
			self.log_view.addItem(f"=> ELM327 Connected")
			self.log_view.addItem(f"=> OBD connection failed")
			self.conn_status.setText("Disconnected")


	def disconnect(self):

		self.timer.stop()
		self.log_view.clear()
		self.elm327.disconnect()
		self.log_view.addItem(f"=> ELM327 Disconnected")
		self.conn_status.setText("Disconnected")

def main():

	app = QApplication(sys.argv)
	gui = OBDSniffGUI()

    # Applying dark theme
	qtmodern.styles.dark(app)
	darked_gui = qtmodern.windows.ModernWindow(gui)
	
	darked_gui.show()
	app.exec_()

if __name__ == '__main__':
	main()