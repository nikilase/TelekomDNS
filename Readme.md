# Python Telekom Homepagecenter Letsencrypt Bot

***STILL WORK IN PROGRESS!***

Python Script to do some basic usage of the Telekom Homepagecenter using selenium.

Implemented mainly to make Letsencrypt DNS01 Challenge easier.

Tested with Python 3.11 but *should* work with any other current version of python.
Tested with the Edge Browser on Windows 10, but *should* also work with other Browsers and Operating Systems.

**Warning:** For better stability make sure to always have the browser in the foreground as I experienced some erroneous
behaviour when the browser was minimized!

### Usage
For now there is a configuration file you need to create under ***conf/config.toml*** with your Login Credentials and 
the domain records you want to set.
You can also supply this information on execution of the script via the CLI.

It is preferred to use a virtual environment!
Be sure to install all requirements before running the script!


To run the letsencrypt script use:
```
python main.py
```
### Not yet implemented!
or:
```
python main.py -l
```
<br>

To check if an edit is completed use: 

```
python main.py -c
```
<br>

For the help function use: 

```
python main.py -h
```
<br>

You can also run both the check and letsencrypt script, whereas the check will execute before letsencrypt, using: 

```
python main.py -c -l
```
