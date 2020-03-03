import datetime


class Lesson(object):

    def set_path(self, path):
        self.path = path

    def set_enrollment_date_and_time(self, year, month, day, hour, minute):
        self.enrollment_time = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute)
