from datetime import datetime
from datetime import timedelta
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logdir = 'C://Flask' + '/logs/login'


# create a login with name, address, and status of whether login was successful
def create_log(name, address, status):
    current_time = datetime.now()
    timestamp = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(current_time.day, current_time.month, current_time.year, current_time.hour, current_time.minute)
    return "{} {} {} {}\n".format(timestamp, address, name, status)


# write the login into the login file.
def write_log(log, location):
    updating = True
    while updating:
        try:
            log_file = open(location, 'a')
            log_file.write(log)
            log_file.close()
            updating = False
        except IOError:
            time.sleep(1)


# update the login
# If the date file has not been created, it will create the file
def update_log(log):
    global logdir
    date = log.split()[0]
    location = logdir + '/{}.log'.format(date)
    if os.path.exists(location):
        write_log(log, location)
    else:
        open(location, 'x')
        write_log(log, location)


# retrieve all the access logs
def get_log():
    global logdir
    log_list = os.listdir(logdir)
    logs = []
    for log in log_list:
        log = open(logdir + '/' + log, 'r')
        raw_logs = log.readlines()
        for raw_log in raw_logs:
            processed_log = raw_log.strip('\n')
            processed_log = processed_log.split()
            logs.insert(0, processed_log)
        log.close()

    return logs


def check_log(filename):
    global logdir
    location = logdir + '/{}.log'.format(filename)
    if os.path.exists(location):
        return True
    else:
        return False


def send_log(filename):
    mail_content = 'Access logs for {}'.format(filename)

    # The mail addresses and password
    sender_address = 'dummypikachutest@gmail.com'
    sender_pass = 'Q@erty1234'
    receiver_address = 'dummypikachutest@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Access log for CB shop.'

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(open(logdir + '/{}.log'.format(filename), 'rb').read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment; filename="{}.log"'.format(filename))
    message.attach(attachment)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def multi_fail_log(address):
    mail_content = 'Multiple failed attempts from {}'.format(address)

    # The mail addresses and password
    sender_address = 'dummypikachutest@gmail.com'
    sender_pass = 'Q@erty1234'
    receiver_address = 'dummypikachutest@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Multiple failed attempts'

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def timeout():
    return datetime.now() + timedelta(minutes=5)


def time_clear(timeout):
    if datetime.now() > timeout:
        return True
    else:
        return False


