from lib2to3.pgen2 import driver
from selenium import webdriver
import io, base64
from PIL import Image
import pytesseract
import time
from selenium.webdriver import ActionChains
import re
import string


ROOTMECHALLENGE_URL = 'http://challenge01.root-me.org/programmation/ch8/'
driver = webdriver.Firefox()
running = True

while running:
    driver.get(ROOTMECHALLENGE_URL)

    # get all the cookie from the GET METHOD
    cookies = driver.get_cookies()

    #get captcha image url
    img_src = images = driver.find_elements_by_tag_name('img')
    for image in img_src:
        string_img_url = image.get_attribute('src')
    img_url = string_img_url.replace('data:image/png;base64,', '')

    #convert the captcha image url to an image
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(img_url, "utf-8"))))
    img.save(r'/Users/ryzwannjohn/Documents/RootMeChallenges/challenge_CAPTCHA/captcha_img.jpeg')

    char_whitelist = string.digits
    char_whitelist += string.ascii_lowercase
    char_whitelist += string.ascii_uppercase

    img_value = str(pytesseract.image_to_string(r'captcha_img.jpeg', lang='fra', config="-c tessedit_char_whitelist=%s_-." % char_whitelist))
    print(list(img_value))
    captcha_val = str(re.sub('[-!@#$._]', '', img_value)).rstrip('\n')
    print(captcha_val)
    cametu_field = driver.find_element_by_name("cametu")
    cametu_field.send_keys(captcha_val)
    print('tring with:', list(captcha_val))
    submit_button = driver.find_element_by_xpath("//input[@value='Try']")
    submit_button.click()
    html_form = str(driver.page_source)
    print(html_form)
    if html_form.find('again') < 0:
        running = False
        
flag = html_form.replace('<html><head></head><body><link rel="stylesheet" property="stylesheet" id="s" type="text/css" href="/template/s.css" media="all"><iframe id="iframe" src="https://www.root-me.org/?page=externe_header"></iframe><p></p><p>', '').replace('</p><p></p><br></body></html>', '')
print(flag)