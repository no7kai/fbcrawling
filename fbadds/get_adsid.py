from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import logging
import requests


def get_adsid(pageid):

    def fb_login():
        driver.get('https://www.facebook.com')
        username = driver.find_element_by_id('email')
        password = driver.find_element_by_id('pass')
        username.send_keys('tiffany.msutton@yahoo.com')
        password.send_keys('buithai2019')
        driver.find_element_by_id('loginbutton').click()
        time.sleep(2)

    today = time.strftime('%Y-%m-%d')

    # csv_file = open(f'../log/{today}_ads.csv', 'w')
    # csv_writer = csv.writer(csv_file)
    # csv_writer.writerow(['Page', 'adsId'])

    logger = logging.getLogger('FB_ads')
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    f_handler = logging.FileHandler('/media/no7kai/JAV/Django_friststep/fbcrawling/log/{}_ads.log'.format(today))
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    c_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(firefox_options=options, executable_path='/media/no7kai/JAV/Django_friststep/fbcrawling/geckodriver')
    # # Get list of accounts
    # user_ls = []
    # with open('user_list.txt') as f:
    #     for line in f:
    #         line = line.strip('\n')
    #         user_ls.append(line.split())
    # # Pick a account
    # user, pws = user_ls.pop()

    # Open and login to Facebook
    fb_login()
    # Check if account logs in successfully 
    if driver.current_url != 'https://www.facebook.com/':
        logger.warning('Failed to login, try another account!')
        exit()
        # try:
        #     user, pws = user_ls.pop()
        #     fb_login()
        # except IndexError:
        #     raise Exception('There is no more account to log in.')
    logger.info('Logging in successful.')

    # Open list 50 Beauty pages
    list_id = []
    url = 'https://www.facebook.com/{}/ads'.format(pageid)
    res = requests.get(url)
    if res.status_code != 200:
        return "Oops! Page isn't available or bad connection. Please check again."

    # Open url again, click to "Ads" tab then load page
    driver.get(url)
    time.sleep(5)
    # Get rid of fucking blocks again
    try:
        driver.find_element_by_xpath("//*[contains(@class, 'uiHeaderImage')]")
        logger.info('This page is not available.')
        exit()
    except Exception as e:
        logger.error(e)
        pass
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//*[contains(@class, 'autofocus layerCancel')]").click()
    except Exception as e:
        logger.error(e)
        pass
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//*[@class='_3ixn']").click()
    except Exception as e:
        logger.error(e)
        pass
    # Scroll 5 times to get more ads
    for i in range(7):
        # execute script to scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep for 9s
        time.sleep(8)

    results = driver.find_elements_by_xpath("//*[contains(@class,'_1dwg _1w_m _q7o')]")

    # Log result of getting ads
    if len(results) == 0:
        logger.info("Page hasn't run any ads")
        exit()
    else:
        logger.info("Got {} ads from Page".format(len(results)))

    # Find id of ads
    for result in results:
        ads = result.find_element_by_xpath(".//div[@class='_6a _5u5j _6b']")
        ads_id = ads.find_element_by_tag_name('div').get_attribute('id')
        ads_id = ads_id.split('_')[2]
        if ':' in ads_id:
            ads_id = ads_id.split(':')[0]
            adsId = '{}_{}'.format(pageid, ads_id)
        elif ';' in ads_id:
            ads_id = ads_id.split(';')[:2]
            adsId = '_'.join(ads_id)
        list_id.append(adsId)

    driver.quit()
    logger.info('Finish crawling Fb ads from input page!')
    return list_id
