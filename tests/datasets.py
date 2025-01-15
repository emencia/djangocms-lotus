import datetime
from zoneinfo import ZoneInfo

import pytest

from lotus.choices import STATUS_DRAFT
from lotus.factories import ArticleFactory, CategoryFactory, TagFactory


class LotusDatasetBase:
    """
    Create Lotus contents with model object providers.
    """
    PROVIDER_NAMES = ["dates"]

    def __init__(self, autoboot=True):
        self.utc = ZoneInfo("UTC")

        if autoboot:
            self.boot()

    def boot(self, providers=None):
        if providers is None:
            providers = self.PROVIDER_NAMES

        for item in self.PROVIDER_NAMES:
            name = "provide_" + item
            if hasattr(self,  name):
                getattr(self, name)()

    def utc_datetime(self, *args, **kwargs):
        return datetime.datetime(*args, **kwargs).replace(tzinfo=self.utc)

    def provide_dates(self):
        self.date_now = self.utc_datetime(2012, 10, 15, 10, 00)
        self.date_yesterday = self.utc_datetime(2012, 10, 14, 10, 0)
        self.date_tomorrow = self.utc_datetime(2012, 10, 16, 10, 0)
        self.date_past_hour = self.utc_datetime(2012, 10, 15, 9, 00)
        self.date_next_hour = self.utc_datetime(2012, 10, 15, 11, 00)


class LotusAdvancedDataset(LotusDatasetBase):
    """
    Dataset with many contents to cover corner cases.
    """
    PROVIDER_NAMES = LotusDatasetBase.PROVIDER_NAMES + [
        "authors",
        "albums",
        "categories",
        "tags",
        "articles",
    ]

    def provide_categories(self):
        self.cat_foo = CategoryFactory(title="foo")
        self.cat_bar = CategoryFactory(title="bar")

    def provide_tags(self):
        self.tag_ping = TagFactory(name="ping")
        self.tag_pong = TagFactory(name="pong")

    def provide_articles(self):
        self.art_draft_yesterday = ArticleFactory(
            title="01. draft yesterday",
            publish_date=self.date_yesterday.date(),
            publish_time=self.date_yesterday.time(),
            status=STATUS_DRAFT,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_published_yesterday = ArticleFactory(
            title="02. published yesterday",
            publish_date=self.date_yesterday.date(),
            publish_time=self.date_yesterday.time(),
            fill_categories=[self.cat_foo, self.cat_bar],
            fill_tags=[self.tag_ping, self.tag_pong],
        )
        self.art_published_yesterday_ended = ArticleFactory(
            title="03. published yesterday, ended one hour ago",
            publish_date=self.date_yesterday.date(),
            publish_time=self.date_yesterday.time(),
            publish_end=self.date_past_hour,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_published_past_hour = ArticleFactory(
            title="04. published past hour",
            publish_date=self.date_past_hour.date(),
            publish_time=self.date_past_hour.time(),
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_pinned_published_past_hour = ArticleFactory(
            title="05. pinned, published past hour",
            publish_date=self.date_past_hour.date(),
            publish_time=self.date_past_hour.time(),
            pinned=True,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_featured_published_past_hour = ArticleFactory(
            title="06. featured, published past hour",
            publish_date=self.date_past_hour.date(),
            publish_time=self.date_past_hour.time(),
            featured=True,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_private_published_past_hour = ArticleFactory(
            title="07. private, published past hour",
            publish_date=self.date_past_hour.date(),
            publish_time=self.date_past_hour.time(),
            private=True,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_publish_past_hour_end_next_hour = ArticleFactory(
            title="08. published past hour, end next hour",
            publish_date=self.date_past_hour.date(),
            publish_time=self.date_past_hour.time(),
            publish_end=self.date_next_hour,
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_ping],
        )
        self.art_publish_next_hour = ArticleFactory(
            title="09. publish next hour",
            publish_date=self.date_next_hour.date(),
            publish_time=self.date_next_hour.time(),
            fill_categories=[self.cat_foo],
            fill_tags=[self.tag_pong],
        )
        self.art_publish_next_hour_end_tomorrow = ArticleFactory(
            title="10. publish next hour, end tomorrow",
            publish_date=self.date_next_hour.date(),
            publish_time=self.date_next_hour.time(),
            publish_end=self.date_tomorrow,
            fill_categories=[self.cat_foo, self.cat_bar],
            fill_tags=[self.tag_ping, self.tag_pong],
        )


@pytest.fixture(scope="function")
def lotus_advanced_dataset(db):
    return LotusAdvancedDataset()
