# ScrollPHat-Clock
A simple clock made with the ScrollPHat kit. This clock display time but also weather info from [OpenWeatherMap](http://openweathermap.org/)

## Installation
You need to install scrollphathd from [Pimonori installation](https://github.com/pimoroni/scroll-phat-hd#full-install-recommended).  
You also need requests, which you can install using `pip install requests`

To launch the program, you need to set two environment variables: **ScrollPHatClockAPIKEY**, the API key from OpenWeatherMap and **ScrollPHatClockCITYID**, the ID of the city that you want the temperature from.

To simplify the process, you can start your program using this example bash script:

```
#!/bin/bash

ScrollPHatClockAPIKEY="{Your API key}"; export ScrollPHatClockAPIKEY
ScrollPHatClockCITYID="{Your city ID}"; export ScrollPHatClockCITYID

python3 clock.py
```
