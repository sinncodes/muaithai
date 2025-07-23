An AI-assisted Muay Thai training app

Main Requirements
- Python 3.10 or later (recommend using a virtual environment)
- Camera
- OS: Windows (not tested on Linux, may work)

Clone or download this repository:
bash
cd rxg046-main

Create and activate a virtual environment (Recommended)

python -m venv venv
venv\Scripts\activate - windows 
source venv/bin/activate - linux 

pip install -r requirements.txt

python main.py

Known issues:

    Initial run of the application will take a longer time

    Lighting conditions and camera angle can affect detection accuracy.

    Only tested on windows.

    Please be patient, sometimes the GUI might take some time to load features

    May require a restart ocasionally

    "Q" can be pressed to exit the camera view

    Custom Combo Ui requires at least one strike to be selected/saved before back button can be pressed