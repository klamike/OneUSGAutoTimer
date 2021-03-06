# OneUSGAutoTimer

Functionally this script is almost the same as [Shaun-Regenbaum/OneUSGAutomaticClock](https://github.com/Shaun-Regenbaum/OneUSGAutomaticClock) except:
- This version can be run on a headless Raspberry Pi so you don't need to keep your computer on all day
- This version relies on an external installation of `chromedriver` for Raspberry Pi support
- This version has [healthchecks.io](https://healthchecks.io) integration for success/failure pinging and [touchbar status](https://github.com/klamike/btt-healthchecks).
- Check out the [multijob](https://github.com/klamike/OneUSGAutoTimer/tree/multijob) branch if you work multiple jobs through OneUSG at the same time.
- Some of the logic is slightly modified for clarity/function.

### USE AT YOUR OWN RISK
___

## Installation

1. Clone this repo
    - `git clone https://github.com/klamike/OneUSGAutoTimer.git`
2. Install dependencies
    - [Python 3.7+](https://www.python.org/downloads/)
    - chromedriver
      - `sudo apt install chromium-chromedriver` on Raspberry Pi
      - `brew install chromedriver` on MacOS
    - Requests, Selenium using `pip install -r requirements.txt`
3. Set environment variables
    - Edit `config_example.py` with your information and rename it to `config.py`
4. Run the script using `python oneusg.py`

___

## Usage

### CLI usage

1. Run the script using `python oneusg.py`
   - If you need to stop the script early, make sure to manually clock out.
   - If you want to close your SSH connection and keep the script running you can use `nohup`/`screen`/`tmux`

### Crontab usage

1. Set an alarm on your phone for 8:58am to make sure you can do the Duo authentication
2. Edit the crontab using `crontab -e` and add the line below to run the script at 9:00am every weekday:

`0 9 * * 1-5 cd /PATH/TO/OneUSGAutoTimer; python3 oneusg.py`
