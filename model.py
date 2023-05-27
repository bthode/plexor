import enum

from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class VideoStatus(enum.Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    FAILED = 'Failed'
    DELETED = 'Deleted'
    COMPLETE = 'Complete'


class Retention(enum.Enum):
    DATE_BASED = 'Date Based'


class Policy(Base):
    __tablename__ = 'policy'
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    type = Column(Enum(Retention), default=Retention.DATE_BASED)
    days_to_retain = Column(Integer, default=7)
    subscription = relationship('Subscription', back_populates='policy')


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    url = Column(String)
    title = Column(String)
    status = Column(Enum(VideoStatus))
    subscription = relationship('Subscription', back_populates='videos')
    created_at = Column(DateTime, nullable=False)
    download_attempts = Column(Integer)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    rss_feed_url = Column(String)
    last_queried = Column(DateTime)
    videos = relationship('Video', back_populates='subscription')
    policy = relationship('Policy', back_populates='subscription', uselist=False)
