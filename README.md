# Corona Simulation

Our project is simulate the corona virus spreading as a function of time by an Cellular automaton.<br />
When the number of patient is high, peoples are being more careful and then the number of the patient goes down.<br />
<br />
As required in the exercise:<br />
N - number of the creatures<br />
D - initial percentage of patients<br />
R - percentage of the creature that moving fast<br />
X - number of generation until recovery<br />
P - the probability to infect<br />
T - the threshold for changing P<br />

  
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cv2, matplotlib, numpy, tkinter and PIL.

```bash
pip install cv2
```
```bash
pip install numpy
```
```bash
pip install matplotlib
```
```bash
pip install PIL 
```
```bash
pip install tkinter 
```

## Usage

Just clone the project (make sure you have all the images in images directory), and run main.py.
If you press "submit" with no parameters in the GUI, then it will run in default parameters:<br />
N = 400, D = 0.5, T = 2, X = 50, R = 5
In order to exit the simulation you need to press ESC and then the graph will show.