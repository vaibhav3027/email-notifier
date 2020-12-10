import os, json, time, socket, logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv


load_dotenv()
###########################################################

def notify_admin():
    while not is_connected():
        time.sleep(10)

    ALL_TO_EMAILS = json.loads(os.getenv('TO_EMAILS'))
    for to_email in ALL_TO_EMAILS:
        message = Mail(
            from_email=os.getenv('FROM_EMAIL'),
            to_emails=to_email,
            subject=os.getenv('EMAIL_SUBJECT'),
            html_content=os.getenv('EMAIL_CONTENT')
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            if response.status_code >= 200 and response.status_code <= 300:
                log_message("Email sent to %s" % to_email)
        except Exception as e:
            log_message("Email couldn't be sent to %s, erro : %s" % (to_email, e.message), True)
            print(e.message)
###########################################################

def is_connected():
    REMOTE_SERVER = 'one.one.one.one'
    try:
        host = socket.gethostbyname(REMOTE_SERVER) # see if we can resolve the host name -- tells us if there is a DNS listening
        s = socket.create_connection((host, 80), 2) # connect to the host -- tells us if the host is actually reachable
        s.close()
        return True
    except:
        pass
    return False
###########################################################

def log_message(msg, error=False):
    logging.basicConfig(filename='notification-email.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s , %(levelname)s : %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    if error:
        logging.error(msg)
    else:
        logging.info(msg)
###########################################################

if __name__ == '__main__':
    notify_admin()