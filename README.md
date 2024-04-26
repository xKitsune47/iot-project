# IoT - Temperature and humidity sensor

The project was made using Raspberry Pi 4, DHT11 sensor, Flask, JavaScript and HTML.

It consists of 2 main parts: RPi4 with DHT11 sensor and a separate computer. Python script on Pi handles reading data from the sensor as well as writing it into a .txt file. On the computer side, there's a server with Flask which reads data from that file and sends it in real time to the site that the user is currently on. The data is displayed in a chart.

This is a project for one of the subjects that I have at the university. Hope I'm gonna pass it with this.

## Deployment

Firstly create and share a folder in your local network, create "temp-humid-data.txt" file. 

The connection type that you want to use is up to you. This project was made with direct connection between the RPi4 and server using Ethernet cable.

### Raspberry Pi 4
```sensor_reading``` branch

Create a folder with a sub-folder within it.
Then you have to mount the shared folder to that sub-folder:
```
    mount -t cifs -o guest,user=foo "PATH/TO/SHARED" "PATH/TO/SUBFOLDER"
```

Next step is to create virtual environment and install requirements:
```
    python -m venv .venv
    pip install -r requirements.txt
```
If your folders aren't named accordingly to mine, then you have to change Python script paths correspondingly.

### Server side
```master``` branch

Create a virtual environment in chosen folder and install requirements:
```
    python -m venv .venv
    pip install -r requirements.txt
```

Then copy files from ```master``` branch.
To run the server you have to open the terminal and type in this command:
```
    python .\sensor_app.py
```
