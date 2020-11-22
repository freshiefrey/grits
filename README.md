# GRITS
Gesture Recognition Integrated System

## Current best: [W = 100, overlap = 50]
- Training_acc = 0.9933
- Test_acc = 0.96762

## TODO:
Nothing, project completed!

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
