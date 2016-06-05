from app import db

from app.models import Image, Article

__author__ = 'ramon'


def find_images(date_from, date_to):
    fromDate = date_from.data
    toDate = date_to.data
    # ipdb.set_trace()
    images = []

    articles = db.session.query(Article).filter(Article.date >= fromDate, Article.date <= toDate).all()
    # images = db.session.query(Image).with_parent(articles).all()
    for article in articles:
        found_images = (db.session.query(Image).with_parent(article).all())
        if len(found_images) > 0:
            images.extend(found_images)
    return images
