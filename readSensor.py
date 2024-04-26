import time
import board
import adafruit_dht
import datetime

sensor = adafruit_dht.DHT11(board.D20)

last_temperature = 0
last_humidity = 0

while True:
	save_data = open("iot_share/temp-moist-data.txt","a")
	now = datetime.datetime.now().replace(microsecond=0).isoformat()
	try:
		temperature = last_temperature = sensor.temperature
		humidity = last_humidity = sensor.humidity
		print(f"{now}: {temperature}°C, {humidity}%")
	except RuntimeError:
		print(f"{now}: {temperature}°C, {humidity}%")
	save_data.write(f"{now},{last_temperature}-{last_humidity}\n")
	save_data.close()
	time.sleep(1)
