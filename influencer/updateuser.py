import requests
# import time
# import csv
# import logging
import os
from .models import User


def updateuser(uid, from_date, to_date):
    # today = time.strftime('%Y-%m_%d')

    # logger = logging.getLogger('FB_ads')
    # logger.setLevel(logging.INFO)
    # c_handler = logging.StreamHandler()
    # c_handler.setLevel(logging.INFO)
    # f_handler = logging.FileHandler(f'{today}_posts_log.log')
    # f_handler.setLevel(logging.INFO)
    # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # f_handler.setFormatter(f_format)
    # c_handler.setFormatter(f_format)
    # logger.addHandler(f_handler)
    # logger.addHandler(c_handler)

    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=50)
    s.mount('https://', adapter)

    token = os.environ['TOKEN']

    # today = time.strftime('%Y-%m-%d')

    # csv_file = open(f'{today}_posts.csv', 'w')
    # csv_writer = csv.writer(csv_file)
    # csv_writer.writerow(['uid', 'follwers', 'post', 'post_id', 'created_time', 'likes', 'comments', 'shares', 'hashtag', 'link'])

    # logger.info('Start logging!')

    url = f'https://graph.facebook.com/{uid}/?fields=subscribers,posts.since({from_date}).until({to_date})&access_token={token}'
    name_url = f'https://graph.facebook.com/{uid}/?access_token={token}'
    res = s.get(name_url)
    r = res.json()
    name = r['name']
    user = User.objects.create(name=name, uid=uid)
    user.save()
    res = s.get(url)
    r = res.json()

    # while res.status_code != 200:
    #     if r['error']['code'] == 190:
    #         # logger.info(f'{token} is invalidated')
    #         try:
    #             token = tokens.pop(0)
    #         except IndexError:
    #             # logger.exception("Out of token!")
    #             raise Exception("Out of token!")
    #         url = f'https://graph.facebook.com/{uid}/?fields=subscribers,posts.since({today})&access_token={token}'
    #         res = s.get(url)
    #         r = res.json()
    #     break

    try:
        followers = r['subscribers']['summary']['total_count']
        user.followers = followers
        user.save()
        posts = r['posts']['data']
        for post in posts:
            message = post['message']

            list_hashtag = [wor for tok in message.split('\n') for wor in tok.split(' ') if wor.startswith('#')]
            hashtag = ', '.join(list_hashtag)
            post_id = post['id']
            created_time = post['created_time']
            likes = post['likes']['count']
            comments = post['comments']['count']
            if 'shares' in post:
                shares = post['shares']['count']
            else:
                shares = 0
            user.post_set.create(message=message,
                                 postid=post_id,
                                 created=created_time,
                                 likes=likes,
                                 comments=comments,
                                 shares=shares,
                                 hashtag=hashtag)
            user.save()
    except KeyError:
        r['posts'] = []
        pass
        # logger.info(f"{uid} This user has no post!")
        # continue

    while 'paging' in r['posts']:
        if 'next' in r['posts']['paging']:
            r = s.get(r['posts']['paging']['next']).json()
            try:
                posts = r['posts']['data']
                for post in posts:
                    message = post['message']

                    list_hashtag = [wor for tok in message.split('\n') for wor in tok.split(' ') if wor.startswith('#')]
                    hashtag = ', '.join(list_hashtag)
                    post_id = post['id']
                    created_time = post['created_time']
                    likes = post['likes']['count']
                    comments = post['comments']['count']
                    if 'shares' in post:
                        shares = post['shares']['count']
                    else:
                        shares = 0
                    user.post_set.create(message=message,
                                         postid=post_id,
                                         created=created_time,
                                         likes=likes,
                                         comments=comments,
                                         shares=shares,
                                         hashtag=hashtag)
                    user.save()
            except KeyError:
                break

    # csv_file.close()
    # logger.info(f'Finish crawling FB posts {today}')


if __name__ == "__main__":
    updateuser()
