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

## Another explanation
In our project we built an automaton according to the requirements detailed in the exercise. In addition, we built a graphic configuration that shows the
The simulation clearly.<br /> We started with a number of creatures N, where the size of the automaton is 200 * 200. D is the percentage of patientst he first of the N creatures.
These creatures move randomly, so in each generation each creature can move to any of the 8 cells surrounding it or stay in place.
R percent of the creatures move faster than the other creatures and change their positions in 10 cells.
When an infected cell is adjacent to an uninfected cell, there is a probability P that the healthy cell will not become infected.
There are two levels of adhesion, low adhesion and high adhesion. When the percentage of patients is higher than T (Threshold),
People are more careful and the risk of infection decreases, and vice versa.
An infected cell remains infected and infectious for X generations, and in addition an infected cell will not become infected again during the simulation.
  
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

## The corona simulation
![b](https://github.com/sapirhender123/Corona-Virus-Simulation/blob/master/CoronaSimulation.PNG)
![c](https://github.com/sapirhender123/Corona-Virus-Simulation/blob/master/Corona2.PNG)

## Graph - the number of patients as a function of the time
We were looked for a combination of the details in which we can see the behavior of waves during the life of the simulation. We reached the following values:
N = 100, D = 0.5, T = 0.5, X = 5, R = 5
The following graph represents the number of patients (Y axis) in each wave, as a function of time (X axis).

Note that when the percentage of patients is higher than T, the risk of infection decreases, therefore the number of patients decreases, and vice versa.
Note that the larger X is, the longer a cell will remain diseased, and thus will be exposed to more creatures,
and cause more infection. That is, the higher X is, the higher the chance of infection and thus the number of patients.
Of course, the larger P (probability that a healthy cell will be infected) is, the less likely a cell will be infected. That is, there is an inverse relationship
between P and the patient group.
In the case where R is larger, more creatures will move faster and be in different areas of the automaton, since they move 10
steps at a time. Such a thing causes a wider and faster infection, and increases the percentage of patients, if the same cells
Rapids are infected cells or cells that are exposed to infected cells.
We note that our simulation simulates a period in which there is no vaccine, that is, there is no immune creature among the N creatures, and in addition there is no
Different variants of the disease, it is only one variety.
![a](https://github.com/sapirhender123/Corona-Virus-Simulation/blob/master/CoronaGraph.PNG)
