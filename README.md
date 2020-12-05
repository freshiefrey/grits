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

### Install additional dependencies on both Gateway and Cloud
A virtual environment is recommended to prevent clashes or overwriting of your main installation.
```python
pip3 install requirements.txt
```

```
sudo apt-get install mosquitto mosquitto-clients
pip3 install paho-mqtt
```

https://github.com/IanHarvey/bluepy  
Follow the instructions for installation of library and bluepy package. To be used on the device acting as Gateway between SensorTag and Cloud.

## 1. The project can be run using the provided files and dependencies directly on Gateway and Device:
Gateway: user_sensor.py for recording SensorTag and sending data, MQTT_gesture.py for monitoring Cloud output  
Cloud: MQTT_classifier.py, lstm_model_100_50

Change the IP address and MQTT authorization to your server in the above 3 python files, SensorTag BLE Address and my_sensor in main of user_sensor.py.

## 2. Alternatively you can do the following and customize the code to fit your needs:
### Pre-processing of data
*Unzip the ready_data.zip* for our processed data.

or

1. *Run sensor.py* within deprecated to record your own data, change Sensortag Address and filename.
2. Combine your recorded data into a single .csv per gesture. Put them in raw_data.
3. Edit *window-mod.ipynb* to fit your parameters, gestures and .csv files.
4. *Run the notebook window-mod.ipynb*
- This processes the raw_data and generates output onto your local repo
    - We have excluded them from our online repo as uncompressed files is too big (>600MB)

### Processed data:
- ready_data folder 

You can open the data via the text files, make sure to unroll to get original dimensions

### Train the model
*Run lstm_csv.ipynb*  
This extracts the processed data and trains the model, saving it into lstm_models folder, showing the model performance and accuracy over the epochs. The model is then evaluated using the test data and outputs the incorrect classifications into a output.csv for further analysis by you.

*Run the Test code to test any model*  
You can also change the model_name to test any other model again and get the output. Run the first 3 cells to import the test data if needed.



## Extra
Just extra workbooks for debugging and processing steps  
- plot.ipynb: For visualising the recorded raw data  
- performance_figures: Performance difference between 100_50 and 50_25 (window_overlap) performance, and the error output of different models for analysis. Can be seen that Crank gesture causes a lot of misclassifications, hence our decision to drop it.  
- android: Code base to develop and use the app shown in the Demo.  
- esp32_mqtt_aws_direct: Code used to program the ESP32 for our Demo purposes, also as an example of how to connect ESP32 to AWS over MQTT with the correct baud rate and setup.  
- helper-code: bluepy and miscelleanous code.