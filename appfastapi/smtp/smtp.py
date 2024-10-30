import smtplib

class SMTPSender():
    _server: str
    _port: int
    _email: str
    _password: str

    def __init__(self, server: str, port: int, email: str, password: str):
        self._email = str(email)
        self._password = str(password)
        self._server = str(server)
        self._port = int(port)

    def sendmail(self, to_email: str, subject: str, message: str):
        with smtplib.SMTP(self._server, self._port) as mail_server:
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()
            mail_server.login(self._email, self._password)

            mail_server.sendmail(self._email, to_email, f"Subject: {subject}\n\n{message}".encode('utf-8'))