# GP_scripts
A collection of scripts for Geo- and planetary physics 1

![Example image](Example.png)
Above is an example of some of the features included in the software.

## Installation
As usual, clone the software to your machine. Here's the procedure with github SSH keys.
```bash
git clone git@github.com:byggemandboesen/GP_scripts.git
```
If you're using HTTPS simply replace it with the required link
```bash
git clone https://github.com/byggemandboesen/GP_scripts.git
```
I suggest creating a virtual environment in the directory of the software.
```bash
python3 -m virtualenv venv
```
Activating virtual environtment on Linux
```bash
source venv/bin/activate
```
Windows:
```bash
venv\Scripts\activate
```
## Required packages
Installing the required packages will now be as simple as
```bash
pip install -r requirements.txt
```

# Running
Simply run the software like usual
```bash
python3 main.py
```

### TODO
* Fix spherical harmonic model simulation for varrying degree
* Maybe fix Dearpygui issues

### Notes
Please use the exact version of Dearpygui as earlier versions have issues with setting axis ticks while later versions brake some other stuff... I will maybe look into this at some point. <br>
