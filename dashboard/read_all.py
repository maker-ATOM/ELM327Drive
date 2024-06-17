import serial
import time

serial_port = '/dev/ttyUSB0'
baud_rate = 38400
timeout = 3
buffer = 40

at_command = b'AT MA\r'
# at_command = b'AT Z\r'
# at_command = b'AT MT 10\r'
# at_command = b'01 01\r'
# at_command = b'AT RV\r'


with serial.Serial(serial_port, baudrate=baud_rate, timeout=timeout) as ser:

    ser.write(at_command)
    ser.flush()

    print(f"Sent command: {at_command}")

    response = ""
    start_time = time.time()

    while len(response) < buffer and (time.time() - start_time) < timeout:
        read_byte = ser.read()

        print(f"Read byte: {read_byte}")

        if read_byte != b'':
            if read_byte[0] > 127:
                pass
            elif read_byte != b'>':
                response += str(read_byte, 'utf-8')
        else:
            print("received none ..")


    if (time.time() - start_time) >= timeout:
        print("Timeout occurred while waiting for response.")

    if len(response) == buffer:
        print(f"More than {buffer} bytes received, discarding extra bytes.")

    print(f"Received response: {response}")
