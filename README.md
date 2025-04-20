
<h1 align="center">
<img src="./img/SIMPLY LOVELY.png" width=100%>
</h1>

# Traktor

Traktor is a discord bot developed in python that uses the [Fastf1](https://docs.fastf1.dev/) package to deliver the latest and past seasons data in discord.

## Commands
* 🏎️ ***Balls*** 🏎️
* 🏎️ ***Printer*** 🏎️
* 🏎️ ***Drivers*** 🏎️
* 🏎️ ***Driverinfo*** 🏎️
* 🏎️ ***Constructors*** 🏎️
* 🏎️ ***Gpinfo*** 🏎️
* 🏎️ ***Gpresults*** 🏎️
* 🏎️ ***Seasonschedule***🏎️
* 🏎️ ***Calendar*** 🏎️
* 🏎️ ***Simplylovely*** 🏎️


## How to Run
### Docker (Recommended)
1- execute ``` docker build -t traktor-app . ``` to build the image, you can rename your image by replacing the `traktor-app` which is the default
2- Run the image built in last step with ```docker run -d --rm --name traktor traktor-app```
3- To stop the container use ``` docker stop traktor ```

### Locally
if in **vscode** by pressing the ```play``` button it fails, you can also Execute ``` python -m main.py ``` inside the project in your terminal and it will work perfectly fine

