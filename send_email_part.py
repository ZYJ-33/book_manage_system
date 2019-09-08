from config import auth
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import smtplib


from_addr = 'book_manage@163.com'
smtp_server = 'smtp.163.com'

def send_email(to_addr, bookname):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    password = auth
    msg = MIMEText("您好， 您订阅的{}已经有库存， 请到订阅系统中申请订阅".format(bookname), 'plain', 'utf-8')
    msg['From'] = _format_addr('{}'.format(from_addr))
    msg['To'] = _format_addr('{}' .format(to_addr))
    msg['Subject'] = Header('到货通知', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__ == "__main__":
    send_email("jobsera@163.com", "Hello World")