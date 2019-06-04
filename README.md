# demoqe-gui
MC9S08QE128 microcontroller Graphical User Interface 

## Requirements

- Python3
- PyQt5
- PySerial
- Matplotlib
- NumPy
	
## How to run

- For the purpose of using this GUI, it may be necessary to run as superuser as for opening USB ports
regular users might not have permissions to do so.In that case run the following sequence of commands.

```python

sudo su
python3 oscilloscope.py

```

## Issues

- For now it only works for Linux. We are making efforts to make it work on windows as well.
