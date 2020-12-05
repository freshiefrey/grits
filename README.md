# GRITS
Gesture Recognition Integrated System

## Current best: [W = 100, overlap = 50]
- Training_acc = 0.9933
- Test_acc = 0.96762

## Project Demonstration
Download and watch 'CS3237 Demo.mp4' to see demonstration of project.

## TODO:
Nothing, project completed!

## Get Started Guide:
This project runs on Linux and AWS Ubuntu 20.04.1 LTS T2.micro Server as the following dependencies do not work on Windows:
bluepy for TI CC2650 SensorTag,
paho-mqtt & mosquitto for MQTT.

### Install additional dependencies
```python
pip3 install requirements.txt
```

```
sudo apt-get install mosquitto mosquitto-clients
pip3 install paho-mqtt
```

https://github.com/IanHarvey/bluepy
Follow the instructions for installation of library and bluepy package. To be used on the device acting as Gateway between SensorTag and Cloud.

### Pre-processing of data
*Unzip the ready_data.zip* for processed data.

or

*Run the notebook window-mod.ipynb*
- this processes the raw_data and generates output onto your local repo
    - I have excluded them from our online repo as file is too big (>300MB)

### Train the model
*Run lstm.py*:
```python
python3 lstm.py
```
This extracts the process data and trains the model

## Processed data:
- ready_data folder 

You can open the data via the numpy or text file format, make sure to unroll to get original dimensions

## Extra
- Just extra workbooks for debugging and processing steps
model.ipynb
