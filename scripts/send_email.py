# Chris Hambridge, project-koku/koku-report-emailer, (2021), GitHub repository
# https://github.com/project-koku/koku-report-emailer
import sys
import smtplib
import time
import ssl
from datetime import date, timedelta
# from email.encoders import encode_base64
# from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import Config
# from costemailer.rbac import get_access
# from costemailer.rbac import get_users
from jinja2 import Template
from postgres_interface import postgres_execute
from pandas import DataFrame

# PRODUCTION_ENDPOINT = "https://cloud.redhat.com"
REL_TEMPLATE_PATH = "CostEmailTemplate.html"
REL_LOGO_PATH = "Logo-Red_Hat-cost-management-RGB.png"
LOGO_PATH = Path(__file__).parent / REL_LOGO_PATH
EMAIL_TEMPLATE_PATH = Path(__file__).parent / REL_TEMPLATE_PATH
EMAIL_TEMPLATE_CONTENT = None
with open(EMAIL_TEMPLATE_PATH) as email_template:
    EMAIL_TEMPLATE_CONTENT = email_template.read()


def email(recipients, content=EMAIL_TEMPLATE_CONTENT, attachments=None, img=None):
    if not recipients:
        return
    gmail_user = Config.EMAIL_USER
    gmail_password = Config.EMAIL_PASSWORD
    context = ssl.create_default_context()
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    s.login(gmail_user, gmail_password)


    today = date.today().strftime("%Y-%m-%d")

    msg = MIMEMultipart()
    subject = f"Koku Metrics Report: {today}"
    msg_text = content
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = ",".join(recipients)
    if attachments is not None:
        for each_file_path in attachments:
            try:
                file_name = each_file_path.split("/")[-1]
                msgApp = MIMEApplication(open(each_file_path, "rb").read(), filename=file_name)
                msgApp.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(msgApp)
            except Exception as err:  # noqa: E722
                print(f"Could not attach file: {err}")
    if img is not None:
        img_count = 0
        for each_file_path in img:
            try:
                file_name = each_file_path.split("/")[-1]
                msgImage = MIMEImage(open(each_file_path, "rb").read(), filename=file_name)
                msgImage.add_header("Content-ID", f"<image{img_count}>")
                msg.attach(msgImage)
                img_count += 1
            except Exception as err:  # noqa: E722
                print(f"Could not attach file: {err}")
    msg.attach(MIMEText(msg_text, "html"))
    s.sendmail(gmail_user, recipients, msg.as_string())

if __name__ == "__main__":
    # email_list = []
    img_paths = [str(LOGO_PATH)]
    print(f"COST_MGMT_RECIPIENTS={Config.COST_MGMT_RECIPIENTS}")
    # account_users = get_users()
    # print(f"Account has {len(account_users)} users.")
    # for user in account_users:
    #     username = user.get("username")
    #     if username not in Config.COST_MGMT_RECIPIENTS.keys():
    #         print(f"User {username} is not in recipient list.")
    #     else:
    #         user_email = user.get("email")
    #         cc_list = Config.COST_MGMT_RECIPIENTS.get(username, {}).get("cc", [])
    #         print(f"User {username} is in recipient list with email {user_email} and cc list {cc_list}.")
    #         user_info = {"user": user, "cc": cc_list}
    #         email_list.append(user_info)
    try:
        freq = sys.argv[1]
    except IndexError:
        print('[ERROR] Need argument report frequency')
        exit(-1)
    midnight_today = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d") + ' 00:00:00+00'
    sql = '''
    select * from (select 
    namespace, 
    round(("pods_avg_usage_cpu_core_total[millicore]" / (select sum("pods_avg_usage_cpu_core_total[millicore]") from reports_human where interval_start = '{0}' and frequency = '{1}') * 100)::numeric, 2) as "pods_avg_usage_cpu_core_percentage[%]",
    "pods_avg_usage_cpu_core_total[millicore]", "pods_request_cpu_core_total[millicore]", "pods_limit_cpu_core_total[millicore]",
    round(("pods_avg_usage_memory_total[mb]" / (select sum("pods_avg_usage_memory_total[mb]") from reports_human where interval_start = '{0}' and frequency = '{1}') * 100)::numeric, 2) as "pods_avg_usage_memory_percentage[%]",
    "pods_avg_usage_memory_total[mb]", "pods_request_memory_total[mb]", "pods_limit_memory_total[mb]", frequency
    from reports_human 
    where interval_start = '{0}' and frequency = '{1}' and namespace <> '') as t
    ORDER BY (substring(namespace, E'openshift'), "pods_avg_usage_cpu_core_percentage[%]") desc
    '''.format(midnight_today, freq)
    free_cpu, free_memory = postgres_execute(
        "select 100-sum(\"pods_avg_usage_cpu_core_consumption_percentage[%]\"), 100-sum(\"pods_avg_usage_memory_consumption_percentage[%]\") from reports_percentage where interval_start = '{}' and frequency = '{}'".format(
            midnight_today, freq),
        result=True)[0]
    table = postgres_execute(
        sql, result=True, header=True)
    if len(table) <= 1:
        print('[INFO] empty result on {}, {}'.format(midnight_today, freq))
        exit(-1)
    table.append(['comment', '', 'sum of average cpu usages of each pod in namespace', 'sum of maximum cpu requested of each pod in namespace', 'sum of maximum cpu limit of each pod in namespace', '', 'sum of average memory usages of each pod in namespace', 'sum of maximum memory requested of each pod in namespace', 'sum of maximum memory limit of each pod in namespace'])
    table.append(['free resource summary'] + [free_cpu] + [''] * 3 + [free_memory])
    table = DataFrame(table[1:], columns=table[0])
    report_path = '/tmp/report-{}-{}.csv'.format(freq, midnight_today)
    table.to_csv(report_path)
    with open(report_path, 'r') as fd:
        if not fd.read():
            print('[INFO] empty report for {}'.format(report_path))
            exit(1)
    for curr_user_email, email_item in Config.COST_MGMT_RECIPIENTS.items():
        print(f"User info: {curr_user_email, email_item}.")
        # curr_user_email = email_item.get("user", {}).get("email")
        email_addrs = [curr_user_email] + email_item.get("cc", [])
        email_template = Template(EMAIL_TEMPLATE_CONTENT)
        template_variables = {"cost_timeframe": '{}-{}'.format(midnight_today, freq)}
        for img_path in img_paths:
            file_name = img_path.split("/")[-1]
            template_variables[file_name] = file_name
        email_msg = email_template.render(**template_variables)
        email(recipients=email_addrs, content=email_msg, attachments=[report_path], img=img_paths)
