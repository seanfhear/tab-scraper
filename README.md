# tab-scraper

An interface for downloading guitar tabs from Ultimate Guitar. Please check the news at the bottom.

![ui-image](screens/ui-screen.png)

Get screenshots of Guitar Chords, Tabs, Bass Tabs and Ukulele Chords with no clutter.

|               Chords               | Tab                           |
| :---------------------------------: | :---------------------------- |
| ![chords](screens/feather-chords.png) | ![tab](screens/sultans-tab.png) |

You can also download GuitarPro and PowerTab files. `<br>`
All files are sorted into directories for quick and easy access.

### Prerequisites

1. Firefox Web Browser

### Running the Program

#### Executable

1. Download an executable version [here](https://github.com/Sean-Hassett/tab-scraper/releases).
2. Follow instructions in the readme.txt provided.

#### Command Line

1. Open settings.cfg and enter in the root directory where you would like all tabs to be stored e.g. `<i>`username/Music/Tabs/ `</i>`
2. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) and put the geckodriver executable into the `<i>`src`</i>` directory.
3. Run `pip install -r requirements.txt`
4. run `python tab_scraper.py` from `<i>`src`</i>` directory.

### Built With

- Python 3
- [PyQT5](https://pypi.org/project/PyQt5/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)

### News

I am assuming the original author has given up on this project, as I myself forked it and began working on it over a year ago (and also promptly disappeared from the project) and there have been no updates since. I'll do my best to get this working again on all platforms, but I cannot make any promises. I'll likely take the existing GUI and rebuild it using libraries I'm familiar with, and build new logic to go in the back end as well. Keep an eye out for updates.
