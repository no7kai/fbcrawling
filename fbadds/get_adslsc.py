import requests
import os
import time
import logging
from .models import Page


def get_adslsm(pageid, list_adsid):

    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=50)
    s.mount('https://', adapter)

    # Get token from .evn file
    token = os.environ['TOKEN']

    today = '2019-05-01'

    # start logging
    logger = logging.getLogger('FB_posts')
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('/media/no7kai/Data/Django/dOne/fbcrawling/log/{}_ads.log'.format(today))
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    # Create new page in database
    url = 'https://graph.facebook.com/v2.1/{}/?access_token={}'.format(pageid, token)
    res = s.get(url)
    r = res.json()

    # Checking status code
    if res.status_code != 200:
        if r['error']['code'] == 190:
            logger.warning('Token is invalidated')
        else:
            logger.warning('Cannot find the page at the moment')
        exit()

    # Try create page if not exist
    try:
        Page.objects.create(name=r['name'], pageid=pageid)
    except Exception:
        pass

    page = Page.objects.get(pageid=pageid)

    for ads_id in list_adsid:
        url = 'https://graph.facebook.com/v2.1/{}/?access_token={}'.format(ads_id, token)
        res = s.get(url)
        r = res.json()
        # while res.status_code != 200:
        #     print(res.status_code)
        #     if r['error']['code'] == 190:
        #         print('yes')
        #         logger.warning(f"{token} - This token is invalidated")
        #         try:
        #             token = tokens.pop(0)
        #         except IndexError:
        #             logger.exception("Out of token!")
        #             raise Exception("Out of token!")
        #         url = f'https://graph.facebook.com/v2.1/{ads_id}/?access_token={token}'
        #         res = s.get(url)
        #         r = res.json()
        #     break

        # Checking status code
        if res.status_code != 200:
            if r['error']['code'] == 190:
                logger.warning('Token is invalidated')
            else:
                logger.warning('Cannot find the ads {} at the moment'.format(ads_id))
            continue

        # Get Ads attributes
        try:
            time = r['created_time']
        except KeyError:
            logger.exception('Cannot find created time - {}'.format(ads_id))
            time = None
        try:
            like = r['likes']['count']
        except KeyError:
            logger.exception('Cannot find likes - {}'.format(ads_id))
            like = None
        try:
            share = r['shares']['count']
        except KeyError:
            logger.exception('Cannot find shares - {}'.format(ads_id))
            share = None
        try:
            comment = r['comments']['count']
        except KeyError:
            logger.exception('Cannot find comments - {}'.format(ads_id))
            comment = None
        try:
            content = r['message']
        except KeyError:
            logger.exception('Cannot find content - {}'.format(ads_id))
            content = None

        # Create Ads, if exists update instead
        try:
            page.adds_set.create(addid=ads_id,
                                 content=content,
                                 created_time=time,
                                 likes=like,
                                 shares=share,
                                 comments=comment)
        except Exception:
            ads = page.adds_set.get(addid=ads_id)
            ads.content = content
            ads.created_time = time
            ads.likes = like
            ads.shares = share
            ads.comments = comment
            ads.save()

    logger.info('Finish crawling Ads')
