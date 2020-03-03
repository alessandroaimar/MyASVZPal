import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
log = logging.getLogger()

from worker import Worker
from lessons.lesson import Lesson as Lesson

#############################################
#### TODO REPLACE WITH USER CLASS
from users.Ale import Ale as User
############################################

user = User()
lesson = Lesson()

#############################################
# TODO Replace with link to the class to subscribe
#############################################
lesson.set_path("https://schalter.asvz.ch/tn/lessons/90878")

#############################################
# TODO Replace with the time of REGISTRATION to the class
lesson.set_enrollment_date_and_time(year=2020,
                                    month=3,
                                    day=2,
                                    hour=14,
                                    minute=15)
############################################

log.info("Starting enroller...")
lesson = Worker(lesson=lesson, user=user)

lesson.start()
