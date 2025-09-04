# smtplib 用于邮件的发信动作
import smtplib, os
# email 用于构建邮件内容
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# 构建邮件头
from email.header import Header

# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = os.environ.get("USER_EMAIL")
password = os.environ.get("USER_PASSWORD")
get_trends_str = os.environ.get("GET_TRENDS")
print(get_trends_str)
# 收信方邮箱
to_addr = from_addr
# 发信服务器
smtp_server = 'smtp.qq.com'
exec(get_trends_str)
trend_list = eval('get_trends()')
# 用trend_list拼接一个html邮件内容
email_content = "<h2>GitHub 热榜:</h2><br>"
for trend in trend_list:
    email_content += f"<b>语言:</b> {trend['language']}<br><b>标题:</b> {trend['title']}<br><b>链接:</b> <a href='{trend['link']}'>{trend['link']}</a><br><b>概览:</b> {trend['description']}<br><br>"

# 创建一个实例msg
msg = MIMEMultipart()
msg['From'] = f'"xujianjun" <{from_addr}>'  # 发送者
msg['To'] = Header('到点就困告')  # 接收者
subject = "Github热榜"
msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
# 邮件正文内容
msg.attach(MIMEText(email_content, 'html', 'utf-8'))

try:
    smtpobj = smtplib.SMTP_SSL(smtp_server)
    smtpobj.connect(smtp_server, 465)  # 建立连接--qq邮箱服务和端口号
    smtpobj.login(from_addr, password)  # 登录--发送者账号和口令
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("无法发送邮件:", e)
finally:
    # 关闭服务器
    smtpobj.quit()
