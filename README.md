# **Friday**
**_A Virtual assistant made in python_**

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0c6126d536c945948453e260220927d6)](https://app.codacy.com/gh/Krrishdhaneja/Friday?utm_source=github.com&utm_medium=referral&utm_content=Krrishdhaneja/Friday&utm_campaign=Badge_Grade)
<!-- [![Build Status](https://travis-ci.com/Krrishdhaneja/Friday.svg?branch=master)](https://travis-ci.com/Krrishdhaneja/Friday) -->
<!-- [![Build Status](https://dev.azure.com/krrish21march/krrish21march/_apis/build/status/Krrishdhaneja.Friday%20(1)?branchName=master)](https://dev.azure.com/krrish21march/krrish21march/_build/latest?definitionId=3&branchName=master) -->
![Python package](https://github.com/Krrishdhaneja/Friday/workflows/Python%20package/badge.svg)

![CodeQL](https://github.com/Krrishdhaneja/Friday/workflows/CodeQL/badge.svg)

# **Installation**
_User must have a Python version>=3.6, versions below this aren't supported_
## **On Linux**

### **On Debian based systems(like Ubuntu, Linux Mint)**

     sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 libespeak1
   
     sudo apt-get install ffmpeg espeak
   
     pip3 install pyaudio
   
     pip3 install -r requirements.txt
   
### **On Arch Linux based systems(Like Manjaro)**
    sudo pacman -S ffmpeg espeak

    sudo pacman -S python-pyqt5 python-pyqtwebengine
    
    pip3 install pyaudio

    pip3 install -r requirements.txt

## **Experimental on fedora based till now, So don't try it now!**
### **On Fedora based systems(like CentOS, RHEL etc.)**
    sudo yum install epel-release
    
    sudo yum install dnf
    
    pip3 install --upgrade pip
    
    sudo dnf install portaudio-devel redhat-rpm-config
## **On Windows**
In Order to run this on Windows run this->
First open CMD or powershell then->
     
     pip install pipwin

     pipwin install pyaudio

     pip install -r requirements.txt


# **Running this Program**
 1. To run WolframAlpha in this program, just head over to [WolframAlpha](https://wolframalpha.com) and create an account there and go to your profile > then my api > then sign up to get an API

 2. To get the weather info, go to [OpenWeatherMap](https://openweathermap.org) > then click on Sign in and if you are having an account log in with it there or create a new one > then after creating an account a verification link would be sent to your account just click on that > after clicking your email would be verified and another mail would be sent to you in which you will find the API key
 
Create a file called `api_config.txt` in the project's root directory, and paste the API keys there. 
The file must look like this (white spaces do not matter):
```
weather_api_key = xxx
wolframalpha_api_key = xxx
```
# **Contributors** 
<a href="https://github.com/Krrishdhaneja/Friday/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Krrishdhaneja/Friday" />
</a>

# **Reporting Issue**
 If you found any vulnerability or if something is not working just click [here](https://github.com/Krrishdhaneja/Friday/issues) and open a new issue.
