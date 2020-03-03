import logging
log = logging.getLogger()


class User(object):

    def __init__(self):

        if self.university != "UZH" and self.university != "ETH":
            raise ValueError("Invalid University field {}".format(self.university))

        log.info("User {} ({}) created".format(self.username, self.university))

