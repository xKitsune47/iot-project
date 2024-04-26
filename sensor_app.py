from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime, timedelta

filePath = '//DESKTOP-RQ7D7A8/iot/temp-moist-data.txt'

# background thread
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


# current date and time
def get_current_datetime(reading_date):
    now = datetime.fromisoformat(reading_date)
    return now.strftime("%m/%d/%Y %H:%M:%S")


# sending data to socket
def background_thread():
    while True:
        sensor_readings = open(filePath, 'r')
        lines = sensor_readings.readlines()
        reading_date, readings = lines[-1].split(',')
        temperature, humidity = readings.split('-')
        sensor_readings.close()
        socketio.emit('updateSensorData',
                      {'tvalue': temperature, 'mvalue': humidity, "date": get_current_datetime(reading_date)})
        socketio.sleep(1)


# homepage
@app.route('/')
def index():
    return render_template('index.html')


# socket connect
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


# socket disconnect
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)


# parse temperature readings
def parseTemperatures(file_path):
    temperatures = []
    with open(file_path, 'r') as readings:
        for line in readings:
            timestamp_str, data_str = line.strip().split(',')
            data_str = data_str.split('-')[0]
            timestamp = datetime.fromisoformat(timestamp_str)
            temperature = float(data_str)
            temperatures.append((timestamp, temperature))
        readings.close()
    return temperatures


# parse moisture readings
def parseMoistures(file_path):
    moistures = []
    with open(file_path, 'r') as file:
        for line in file:
            timestamp_str, data_str = line.strip().split(',')
            data_str = data_str.split('-')[1]
            timestamp = datetime.fromisoformat(timestamp_str)
            moisture = float(data_str)
            moistures.append((timestamp, moisture))
    return moistures


# calculate data average over parsed time
def calcAverage(data, time_delta):
    current_time = datetime.now()
    timeRange = (current_time - time_delta).replace(microsecond=0)

    dataOverTime = [temp for temp in data if temp[0] >= timeRange]
    print(time_delta, dataOverTime)
    print(timeRange.replace(microsecond=0))
    if not dataOverTime:
        return None

    total_temperature = sum(temp[1] for temp in dataOverTime)
    averageData = total_temperature / len(dataOverTime)
    return round(averageData, 1)


# subpage with averages
@app.route('/averages')
def average():
    temperatureData = parseTemperatures(filePath)
    moistureData = parseMoistures(filePath)

    averageTemps = [calcAverage(temperatureData, timedelta(hours=1)),
                    calcAverage(temperatureData, timedelta(days=1)),
                    calcAverage(temperatureData, timedelta(days=7))]
    averageMoist = [calcAverage(moistureData, timedelta(hours=1)),
                    calcAverage(moistureData, timedelta(days=1)),
                    calcAverage(moistureData, timedelta(days=7))]

    for element in enumerate(averageTemps):
        if element[1] is None:
            averageTemps[element[0]] = 'N/A'
        else:
            averageTemps[element[0]] = round(element[1], 2)

    for element in enumerate(averageMoist):
        if element[1] is None:
            averageMoist[element[0]] = 'N/A'

    print(averageTemps, averageMoist)
    return render_template('averages.html', temp=averageTemps, moist=averageMoist)


# run apps
if __name__ == '__main__':
    socketio.run(app)
