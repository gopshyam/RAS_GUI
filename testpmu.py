from pypmu.pdc import Pdc
from pypmu.frame import CommonFrame
import time
import struct
import math
import numpy

IP = "192.168.1.111"
PORT = 4742
ID = 4

HARD_IP = "192.168.1.51"
HARD_PORT = 5011
HARD_ID = 11
#IP = "127.0.0.1"
#PORT = 1420

ref_pdc = Pdc(pmu_ip = IP, pmu_port = 4712, pdc_id = 1)
mpdc = Pdc(pmu_ip = IP, pmu_port = PORT, pdc_id = ID)
#pdc_one = Pdc(pmu_ip = HARD_IP, pmu_port = HARD_PORT, pdc_id = 11)
pdc_one = Pdc(pmu_ip = IP, pmu_port = PORT, pdc_id = 4)

mpdc.run()
ref_pdc.run()
print("FIRST PMU")
pdc_one.run()
print("RUNNING")


config = mpdc.get_config()
print(config)

ref_pdc.start()
mpdc.start()
pdc_one.start()

data = "Not Connected"


print("Connected")

for i in range(10):
	ref_data = ref_pdc.get()
	data = mpdc.get()
	data_one = pdc_one.get()
	print(len(data))
	print(len(data_one))
#	print("PMU1")
#	print(data_one)
#	print("PMU3")
#	print(data)

	ref_angle = struct.unpack('>f', ref_data[20:24])[0]

	print("\n\nParsing Hardware PMU:")
	print(struct.unpack('>f', data_one[16:20]))
	print(struct.unpack('>f', data_one[20:24]))
	vmag1 = struct.unpack('>f', data_one[16:20])[0]
	vang1 = struct.unpack('>f', data_one[20:24])[0]
	print(struct.unpack('>f', data_one[24:28]))
	print(struct.unpack('>f', data_one[28:32]))
	imag1 = struct.unpack('>f', data_one[24:28])[0]
	iang1 = struct.unpack('>f', data_one[28:32])[0]
#	print(struct.unpack('>f', data_one[32:36]))
#	print(struct.unpack('>f', data_one[36:40]))
	v_ang = vang1 - ref_angle
	i_ang = iang1 - ref_angle
	v_vect = (vmag1 * math.cos(v_ang)) + (vmag1 * math.sin(v_ang) * 1j)
	i_vect = (imag1 * math.cos(i_ang)) + (imag1 * math.sin(i_ang) * -1j)
	res1 = v_vect * i_vect * 3
	print(res1)



	print("\nParsing Software PMU:")
	print(struct.unpack('>f', data[16:20]))
	print(struct.unpack('>f', data[20:24]))
	vmag3 = struct.unpack('>f', data[16:20])[0]
	vang3 = struct.unpack('>f', data[20:24])[0]
	imag3 = struct.unpack('>f', data[24:28])[0]
	iang3 = struct.unpack('>f', data[28:32])[0]
	print(imag3)
	print(iang3)

	v_ang = vang3 - ref_angle
	i_ang = iang3 - ref_angle
	v_vect = (vmag3 * math.cos(v_ang)) + (vmag3 * math.sin(v_ang) * 1j)
	i_vect = (imag3 * math.cos(i_ang)) + (imag3 * math.sin(i_ang) * -1j)

	res3 = v_vect * i_vect * 3
#	print(vmag3, v_ang, imag3, i_ang, v_vect, i_vect)

	print(res3)

#	print(struct.unpack('>f', data[24:28]))
#	print(struct.unpack('>f', data[28:32]))
#	print(struct.unpack('>f', data[32:36]))
#	print(struct.unpack('>f', data[36:40]))
	time.sleep(3)
