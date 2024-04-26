import time
import board
import adafruit_dht
import datetime

sensor = adafruit_dht.DHT11(board.D20)

last_temperature = 0
last_humidity = 0
save_data = open("iot_share/temp-moist-data.txt", "a")
while True:
	settings_file = open("iot_share/settings.txt", "r")
	lines = settings_file.readlines()
	wait_time = float(lines[0].split(' ')[1])
	if wait_time < 1:
		print("Time between measurements cannot be lower than 1 second")
		exit()

	now = datetime.datetime.now().replace(microsecond=0).isoformat()
	try:
		temperature = last_temperature = sensor.temperature
		humidity = last_humidity = sensor.humidity
		print(f"{now}: {temperature}°C, {humidity}%")
	except RuntimeError:
		print(f"{now}: {temperature}°C, {humidity}%")

	save_data.write(f"{now},{last_temperature}-{last_humidity}\n")
	save_data.flush()
	settings_file.close()
	time.sleep(wait_time)
