from PIL import Image
# from common import ocr
from common.methods import *
from threading import Thread
import time
import random
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import logging
from colorama import init, Fore
import re
# from common.work import Work
from common.ocr import ocr_img_region_baidu
from common.phone import Android
from common.phone import Simulator
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

#
init(autoreset=True)

logger = logging.getLogger(__name__)

from log import mylogging

# 读取配置文件
CONFIG = configparser.ConfigParser()
CONFIG.read('./config/configure.conf', encoding='utf-8')
# CONFIG.read('./config/configure-dev.conf', encoding='utf-8')
# 全局变量
# 每天班次list
WORKS = []

MORNING = 0
AFTERNOON = 0
#
REST_REGION = CONFIG.get('work', 'rest_region')
REST_TEXT = CONFIG.get('work', 'rest_text')

LOGIN_REGION = CONFIG.get('login', 'region')
LOGIN_TEXT = CONFIG.get('login', 'text')

USE_SIMULATOR = int(CONFIG.get('simulator', 'use'))

TAP_POSITION_X = int(CONFIG.get('position', 'x'))
TAP_POSITION_Y = int(CONFIG.get('position', 'y'))


SKIP_POSITION_X = int(CONFIG.get('update', 'x'))
SKIP_POSITION_Y = int(CONFIG.get('update', 'y'))

TODAY_REST = 0
# REFRESH_RUNNING = 0
# CLEAR_RUNNING = 0
# CHECK_RUNNING = 0

SCREEN_FILE = 'screenshot.png'

android = Android(SCREEN_FILE)
simulator = Simulator(CONFIG.get('simulator', 'name'), CONFIG.get('simulator', 'path'))


def is_mail_config_passed():
    config = CONFIG
    host = config.get("mail", "host")
    port = config.get('mail', 'port')

    receiver = config.get('mail', 'receiver')
    sender = config.get('mail', 'sender')

    username = config.get('mail', 'username')
    password = config.get('mail', 'password')
    # print(len(host))
    # print(len(port))
    if len(host) == 0 \
            or len(port) == 0 \
            or len(receiver) == 0 \
            or len(sender) == 0 \
            or len(username) == 0 \
            or len(password) == 0:
        return False
    return True


def is_ocr_config_passed():
    config = CONFIG
    APP_ID = config.get('baidu_api', 'APP_ID').replace(' ', '').strip()
    API_KEY = config.get('baidu_api', 'API_KEY').replace(' ', '').strip()
    SECRET_KEY = config.get('baidu_api', 'SECRET_KEY').replace(' ', '').strip()
    # print(APP_ID)
    # print(len(APP_ID))
    if len(APP_ID) == 0 \
            or len(API_KEY) == 0 \
            or len(SECRET_KEY) == 0:
        return False
    return True


def init_simulator():
    # if USE_SIMULATOR != 1:
    #     android.connect('127.0.0.1:21503')
    #     return
    print(Fore.MAGENTA+"初始化模拟器")
    simulator.reopen()
    print(Fore.MAGENTA+"连接模拟器")
    android.connect('127.0.0.1:21503')
    print(Fore.GREEN+"初始化模拟器完成\n")


def check_work():
    global MORNING, AFTERNOON
    now = time.localtime(time.time())

    if now.tm_hour <= 12:
        return MORNING
    if now.tm_hour > 12:
        return AFTERNOON


def set_work():
    global MORNING, AFTERNOON
    now = time.localtime(time.time())

    if now.tm_hour <= 12:
        MORNING = 1
    if now.tm_hour > 12:
        AFTERNOON = 1


def clear_work():
    global MORNING, AFTERNOON
    print(Fore.CYAN + "开始清空当日班次..")
    if MORNING == 1:
        MORNING = 0
    if AFTERNOON == 1:
        AFTERNOON = 0
    # init_simulator()


def check_login():
    image = Image.open(SCREEN_FILE)
    text = ocr_img_region_baidu(image, CONFIG, LOGIN_REGION)
    print(text)
    if not text:
        print(Fore.RED + "ocr 返回为空")
        return
    if LOGIN_TEXT in text[0]:
        print(Fore.GREEN + "ocr 识别到 " + LOGIN_TEXT )
        set_work()
    else:
        print(Fore.RED + "ocr 未识别出 " + LOGIN_TEXT)


def heart():
    # close
    android.close_yd()
    # open app
    android.open_yd()


def go_check():

    print(Fore.CYAN + "\n" + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + " 开始例行检查")

    if check_work():
        heart()
        print(Fore.CYAN + "当前时间段已经有执行记录，跳过")
        return

    random_sleep = random.randint(60, 100)
    # print_works()
    print(Fore.CYAN + "随机等待 %d s" % random_sleep)
    time.sleep(random_sleep)

    if not android.check_devices():
        print(Fore.RED + "模拟器故障，重启模拟器，跳过本次检查")
        logger.error("模拟器故障，重启模拟器，跳过本次检查")
        init_simulator()
        return
    # 网络故障
    if not send_http_packet('www.baidu.com'):
        print(Fore.RED+"网络故障，跳过本次检查")
        logger.error("网络故障，跳过本次检查")
        return

    now = time.localtime(time.time())

    # close
    android.close_yd()
    # open app
    android.open_yd()
    # card
    # android.tap_postion(x, y)

    # 停留10s
    print(Fore.WHITE + "停留 100 s" )
    time.sleep(100)
    android.tap_postion(SKIP_POSITION_X, SKIP_POSITION_Y)
    print(Fore.WHITE + "停留 5 s,跳过更新")
    time.sleep(5)
    android.tap_postion(TAP_POSITION_X, TAP_POSITION_Y)
    print(Fore.WHITE + "停留 30 s,检测登录状态")
    time.sleep(30)
    android.screen_cap()


    check_login()

    if check_work() == 1:
        # send mail
        title = '%s 省区经营管家 [%d-%d-%d %d:%d:%d]' % (
            'open',
            now.tm_year, now.tm_mon, now.tm_mday,
            now.tm_hour, now.tm_min, now.tm_sec
        )
        # 成功之后发邮件
        send_email(SCREEN_FILE, title, CONFIG)
    # set_work()
    print(Fore.GREEN + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + " 本次检查完成\n")




if __name__ == '__main__':
    print(Fore.CYAN + "开始检查运行环境")

    # init_simulator()
    android.connect('127.0.0.1:21503')

    if not android.check_devices():
        print(Fore.RED + "adb 未检测到 设备，无法继续运行")
        input("\n输入任意键退出...\n")
        exit(1)
    else:
        print(Fore.GREEN + "设备检查通过")

    if not is_mail_config_passed():
        print(Fore.RED + "邮箱配置检查失败，无法继续运行")
        input("\n输入任意键退出...\n")
        exit(1)
    else:
        print(Fore.GREEN + "邮箱配置检查通过")

    if not is_ocr_config_passed():
        print(Fore.RED + "百度OCR配置检查失败，无法继续运行")
        input("\n输入任意键退出...\n")
        exit(1)
    else:
        print(Fore.GREEN + "百度OCR配置检查通过")
    go_check()

    scheduler = BlockingScheduler()
    scheduler.add_job(go_check, CronTrigger(
        day="*", hour="9-11", minute="*/10"
    ))
    scheduler.add_job(go_check, CronTrigger(
        day="*", hour="14-16", minute="*/10"
    ))

    scheduler.add_job(heart, CronTrigger(
        day="*", hour="17-23", minute="*/10"
    ))
    scheduler.add_job(heart, CronTrigger(
        day="*", hour="0-8", minute="*/10"
    ))
    # scheduler.add_job(go_check, CronTrigger(
    #     day="*", hour="10-16", minute="*"
    # ))
    scheduler.add_job(clear_work, CronTrigger(
        day="*", hour="21-23"
    ))
    print(Fore.GREEN + "调度器开始运行..")
    scheduler.start()
    # go_check()