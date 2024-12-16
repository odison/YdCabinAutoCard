import configparser
from PIL import Image
# 读取配置文件
from common.ocr import ocr_img_region_baidu

CONFIG = configparser.ConfigParser()
CONFIG.read('./config/configure-dev.conf', encoding='utf-8')
LOGIN_REGION = CONFIG.get('login', 'region')

if __name__ == '__main__':
    image = Image.open("./screenshot.png")
    ocr = ocr_img_region_baidu(image, CONFIG, LOGIN_REGION)
    print(ocr)