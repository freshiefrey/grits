# grits
Gesture Recognition Integrated System

## Current best:
- Training_acc = 0.9933
- Test_acc = 0.626
Severe overfitting, need to fine tune

## TODO:
- TUNE Hyper parameters in the files
    - remember to change the model name lstm_model so to not overide if u want to keep a good model
## Get Started Guide:

### Install additional dependencies
```python
pip3 install requirements.txt
```
### Preprocess data
*Run the notebook window.ipynb*
- this processes the data and generates output onto your local repo
    - I have excluded them from our online repo as file is too big

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
