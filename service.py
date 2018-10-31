# -*- coding: utf-8 -*-
import requests
from bs4 import UnicodeDammit
from lxml import etree
from datetime import date
from team_members import team_members

iron_man_start_date = date(2018, 10, 16)
expected_post_count = (date.today() - iron_man_start_date).days + 1


def generate_base_url(number):
    return 'https://ithelp.ithome.com.tw/ironman/signup/team/50?page={0}'.format(number)


def iron_man_id_from_url(url):
    return url.split('/')[-1]

team_member_ids = [i['iron_man_id'] for i in team_members]

page1_url = generate_base_url(1)
page2_url = generate_base_url(2)
page3_url = generate_base_url(3)

pages = [
    requests.get(page1_url).content,
    requests.get(page2_url).content,
    requests.get(page3_url).content
]


def decode_html(html_string):
    converted = UnicodeDammit(html_string)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.tried_encodings))
    return converted.unicode_markup


def is_today(html_object):
    topic_date = html_object.xpath('div[@class="ir-list__info"]/text()')[1].strip().split(' ')[1]
    result = str(date.today()) == topic_date
    return result

def convert_html_to_dict(html_object):
    link = html_object.xpath('div[@class="ir-list__group"]/div[@class="ir-list__group-topic"]/a/@href')[0]
    post_count = int(html_object.xpath('div[@class="ir-list__group"]/div[@class="ir-list__group-topic"]/span[@class="ir-list__group-topic-num"]/text()')[0].strip())
    iron_man_id = iron_man_id_from_url(link)
    return {
        'username': html_object.xpath('div[@class="ir-list__info"]/a[@class="ir-list__user"]/@href')[0].split('/')[-1],
        'link': html_object.xpath('div[@class="ir-list__group"]/div[@class="ir-list__group-topic"]/a/@href')[0],
        'title': html_object.xpath('div[@class="ir-list__group"]/div[@class="ir-list__group-topic"]/a/text()')[0],
        'topic_id': iron_man_id,
        'posts': post_count,
        'name': next(
            i['slack_handle'] for i in team_members if i['iron_man_id'] == iron_man_id
        )
    }


parser = etree.HTMLParser(recover=True)
pages = [etree.fromstring(decode_html(i), parser) for i in pages]
posts = [i.xpath('//li[@class="ir-list"]') for i in pages]
posts = [i for i in [*posts[0], *posts[1], *posts[2]] if is_today(i)]
result = [convert_html_to_dict(i) for i in posts]


def get_all_not_completed():
    today_ironman_ids = [i['topic_id'] for i in result]
    print(today_ironman_ids)
    not_completed = list(filter(lambda i: i['iron_man_id'] not in today_ironman_ids, team_members))
    print(not_completed)
    if len(not_completed) == 0:
        print('all finished')
        return False
    prefix = '目前仍未完成貼文的：'
    return '{0}{1}'.format(prefix, ''.join(['<@{0}>  '.format(i['slack_handle']) for i in not_completed]))


def post_slack():
    if not get_all_not_completed():
        return
    payload = {
        'channel': '#iron-man',
        'username': '催文機',
        'icon_emoji': ':truck:',
        'text': get_all_not_completed()
    }
    requests.post('https://hooks.slack.com/services/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', json=payload)


def handler(event, context):
    post_slack()
    return
