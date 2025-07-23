An AI-assisted Muay Thai training app

Main Requirements
- Python 3.10 or later (recommend using a virtual environment)
- Camera
- OS: Windows, Linux (not tested on Linux, should work)

Create and activate a virtual environment (Recommended)

python -m venv venv
venv\Scripts\activate - windows 
source venv/bin/activate - linux 

pip install -r requirements.txt

python main.py

"Q" can be pressed to exit the camera view

Known issues:

    Initial run of the application will take a longer time

    Lighting conditions and camera angle can affect detection accuracy

    GUI might take some time to load features

    May require a restart ocasionally

    Custom Combo Ui requires at least one strike to be selected/saved before back button can be pressed
