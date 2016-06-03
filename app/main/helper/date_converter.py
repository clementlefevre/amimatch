import datetime
from flask import flash
from sqlalchemy.exc import IntegrityError
from app import db

__author__ = 'ramon'

import re


def update_article(article):
    article.date = date_converter(article.article_date)
    persist_date(article)


def date_converter(url):
    date = re.split('-', url)[-3:]
    date = [int(dt) for dt in date]
    date = tuple(date[::-1])

    return datetime.date(*date)


def persist_date(article):
    try:
        db.session.add(article)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('Could not save this article : id:{} : url:{}'.format(article.id, article.article_link))
