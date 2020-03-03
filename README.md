# MyASVZPal

Quick Start Guide

Preparation procedure
1) Inside the folder /users/, create a copy of  user_example.py and rename it as <your name>.py (e.g. Ale.py)
2) Open the new file and set the username, password and university to match yours
3) Open main.py and replace 
          from users.Ale import Ale as User
   with the created user class
   
   
   
Run procedure:
1) In the main file:
    - change the URL of course to the desired one (note: it changes every day/week)
                lesson.set_path("https://schalter.asvz.ch/tn/lessons/90878")
                
    - change the registration time for the class. Note this is the REGISTRATION time, not the class time
                lesson.set_enrollment_date_and_time(year=2020,
                                                    month=3,
                                                    day=2,
                                                    hour=14,
                                                    minute=15)
                                                    
2) Ensure your computer time is in sync - even few seconds delay may mess up the enrollment
3) Press start
4) Go to ASVZ


Notes:
Current version works only for Windows as OS and ETH/UZH as universities
    
