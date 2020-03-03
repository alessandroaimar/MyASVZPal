from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import logging

log = logging.getLogger()


class Worker(object):
    fail_delay = 60
    login_time_margin = 30
    wait_login_report_seconds_long = 600
    wait_login_report_seconds_short = 60
    wait_time_login_countdown = 15

    def __init__(self, lesson, user):

        self.lesson = lesson
        self.user = user

    def start(self):

        self.wait_login_time()
        log.info("Initializing web interface")

        self.open_web_interface()

        log.info("Starting login sequence")
        self.execute_login()

        self.wait_enrollment_time()
        log.info("Starting enroll sequence")
        self.execute_enroll()

        log.info("Enrollment completed")

    def wait_enrollment_time(self):
        now = datetime.datetime.now()
        wait_time = self.lesson.enrollment_time - now
        # +1 to be sure the website is ready
        wait_time_enroll_seconds = wait_time.total_seconds()

        if wait_time_enroll_seconds > 0:
            log.info("Waiting before enrollment for {:.0f} seconds".format(wait_time_enroll_seconds))
            time.sleep(wait_time_enroll_seconds)

    def wait_login_time(self):
        # just to start
        wait_time_login_seconds = 1

        while wait_time_login_seconds > 0:
            now = datetime.datetime.now()
            wait_time = self.lesson.enrollment_time - now
            wait_time_login_seconds = wait_time.total_seconds() - self.login_time_margin

            wait_time_minutes = wait_time_login_seconds // 60
            wait_time_minutes_seconds = int(wait_time_login_seconds) % 60

            if wait_time_minutes_seconds != 0 or wait_time_minutes == 0:
                if wait_time_minutes > 0:
                    log.info("Login countdown: {:.0f} minutes and {:.0f} seconds".format(wait_time_minutes, wait_time_minutes_seconds))
                else:
                    log.info("Login countdown: {:.0f} seconds".format(wait_time_minutes_seconds))

            else:
                log.info("Login countdown: {:.0f} minutes".format(wait_time_minutes))

            if wait_time_minutes <= 1:
                if wait_time_login_seconds - self.wait_login_report_seconds_short > self.wait_time_login_countdown:
                    wait_segment = min(wait_time_login_seconds, self.wait_login_report_seconds_short)
                else:
                    wait_segment = 1
            else:
                # We do the + to round up the log.info to be minutes only
                wait_segment = min(wait_time_login_seconds, self.wait_login_report_seconds_long + wait_time_minutes_seconds)

            time.sleep(wait_segment)

    def wait_load_and_click(self, xpath):
        try:
            waitElement = WebDriverWait(self.driver, self.fail_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            log.info("Warning: timeout occured while waiting")
        button = self.driver.find_element_by_xpath(xpath)
        button.click()

    def wait_and_return_text(self, xpath):
        try:
            waitElement = WebDriverWait(self.driver, self.fail_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            log.info("Warning: timeout occured while waiting")

        return self.driver.find_element_by_xpath(xpath).text

    def wait_load_and_insert(self, xpath, data):
        try:
            waitElement = WebDriverWait(self.driver, self.fail_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            log.info("Warning: timeout occured while waiting")

        field = self.driver.find_element_by_xpath(xpath)
        field.clear()
        field.send_keys(data)

    def open_web_interface(self):
        # Using Chrome to access web
        log.info("Setting up web interface (Chrome, headless)")
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Open the website
        self.driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
        self.driver.get(self.lesson.path)

    def execute_login(self):

        # We arent logged int
        log.info("Pressing ASVZ Lesson Login")
        sport_login_xpath = '/html/body/app-root/div/div[2]/app-lesson-details/div/div/app-lessons-enrollment-button/button'
        self.wait_load_and_click(sport_login_xpath)

        log.info("Selecting Switch Login mode")
        switch_button_xpath = '/html/body/div/div[5]/div[2]/div/div[2]/div/form/div/p/button'
        self.wait_load_and_click(switch_button_xpath)

        sel_uni_xpath = "/html/body/div/div/div[2]/form/div/div[1]/span/img"
        self.wait_load_and_click(sel_uni_xpath)

        if self.user.university.upper() == "UZH":
            log.info("University: UZH")
            uni_xpath = "/html/body/div/div/div[2]/form/div/div[1]/span/div/div[13]"

        elif self.user.university.upper() == "ETH":
            log.info("University: ETH")
            uni_xpath = "/html/body/div/div/div[2]/form/div/div[1]/span/div/div[5]"

        self.wait_load_and_click(uni_xpath)

        log.info("Inserting user data...")
        username_xpath = "/html/body/div/div[2]/form/div[1]/input"
        self.wait_load_and_insert(username_xpath, self.user.username)

        password_xpath = "/html/body/div/div[2]/form/div[2]/input"
        self.wait_load_and_insert(password_xpath, self.user.password)

        log.info("Confirming login...")
        switch_login_button_xpath = "/html/body/div/div[2]/form/div[4]/button"
        self.wait_load_and_click(switch_login_button_xpath)
        log.info("Login successful")

    def execute_enroll(self):
        log.info("Enrolling...")

        enroll_button_xpath = "/html/body/app-root/div/div[2]/app-lesson-details/div/div/app-lessons-enrollment-button/div[2]/div[1]/div/button"
        self.wait_load_and_click(enroll_button_xpath)

        enrollment_string_xpath = "/html/body/app-root/div/div[2]/app-lesson-details/div/div/app-lessons-enrollment-button/div[2]/div[1]/div/span"
        enrollment_string = self.wait_and_return_text(enrollment_string_xpath)
        enrollment_number = [int(s) for s in enrollment_string.split() if s.isdigit()][0]
        log.info("Successfully enrolled with number {}".format(enrollment_number))
