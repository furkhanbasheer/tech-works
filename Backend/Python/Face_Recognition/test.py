import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test message from Smart Attendance System")
msg['Subject'] = "Test Mail"
msg['From'] = "furkhanbasheer001@gmail.com"
msg['To'] = "furkhanhtc1@gmail.com"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("furkhanbasheer001@gmail.com", "zfiq bvil jvqw nhoz")  # Your App Password here
server.send_message(msg)
server.quit()

print("✅ Test mail sent")
