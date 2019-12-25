from datetime import datetime
import logging
import asyncio

from bs4 import BeautifulSoup
import requests
from pypika import PostgreSQLQuery as Query

from appfollow_test.storage.db import db, posts
from appfollow_test import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _get_hn_page():
    logger.info('Requesting HN page...')

    r = requests.get(config.HN_URL)

    return r.text


async def parse_hn():
    logger.info('Started parsing.')

    hn_page = _get_hn_page()

    soup = BeautifulSoup(hn_page, 'html.parser')

    post_list = []

    logger.info('Parsing posts...')

    for item in soup.select('tr.athing'):
        item_id = item.get('id')

        link = item.select('td.title > a')[0]
        url = link.get('href')
        title = str(link.string)

        # case when post doesn't have external URL and is HN discussion thread instead
        if 'http' not in url:
            url = f'{config.HN_URL}/{url}'

        post_list.append({
            'id': item_id,
            'title': title,
            'url': url,
        })

    if not post_list:
        logger.info('No posts found, finished parsing')
        return

    logger.info(f'Found {len(post_list)} posts')

    created = datetime.now().isoformat()

    insert_q = (
        Query.into(posts)
        .columns(
            posts.id,
            posts.title,
            posts.url,
            posts.created,
        )
        .insert(
            *[
                (
                    post['id'],
                    post['title'],
                    post['url'],
                    created,
                )
                for post in post_list
            ]
        )
        .on_conflict('id')
        .do_nothing()
    )

    logger.info('Inserting posts to DB...')

    await db.execute(insert_q)

    logger.info('Finished parsing.')


async def start_db():
    logger.info('Starting DB...')

    await db.start()


async def start():
    await start_db()

    while True:
        await parse_hn()
        await asyncio.sleep(config.HN_PARSE_INTERVAL)


async def stop():
    await db.close()

    logger.info('Closing DB...')
