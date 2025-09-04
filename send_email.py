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
# 收信方邮箱
to_addr = from_addr
# 发信服务器
smtp_server = 'smtp.qq.com'


def get_trends():
    import requests

    headers = {
        "accept": "text/html, application/xhtml+xml",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN, zh; q=0.9, en; q=0.8",
        "cache-control": "no-cache",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    response = requests.get('https://github.com/trending')
    # 解析热榜项目链接和摘要
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    repo_list = soup.find_all('article', class_='Box-row')
    trends = []
    for repo in repo_list:
        title_tag = repo.h2.a
        title = title_tag.get_text(strip=True).replace('\n', '').replace(' ', '')
        link = 'https://github.com' + title_tag['href']
        description_tag = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
        description = description_tag.get_text(strip=True) if description_tag else 'No description'
        # 获取语言标签
        language_tag = repo.find('span', itemprop='programmingLanguage')
        language = language_tag.get_text(strip=True) if language_tag else 'No language'
        trends.append({'title': title, 'link': link, 'description': description, 'language': language})
    return trends


trend_list = get_trends()
# 用trend_list拼接一个html邮件内容
email_content = "<h2>GitHub Trending Repositories:</h2><br>"
for trend in trend_list:
    email_content += f"<b>Language:</b> {trend['language']}<br><b>Title:</b> {trend['title']}<br><b>Link:</b> <a href='{trend['link']}'>{trend['link']}</a><br><b>Description:</b> {trend['description']}<br><br>"
    

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
