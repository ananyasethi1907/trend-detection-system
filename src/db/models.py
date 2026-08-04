from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Boolean,
    Integer,
    BigInteger,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class Account(Base):

    __tablename__ = "accounts"

    account_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True
    )

    account_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    followers_count: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Post(Base):

    __tablename__ = "posts"

    post_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True
    )

    account_id: Mapped[str] = mapped_column(
        ForeignKey(
            "accounts.account_id"
        ),
        nullable=False
    )

    content_type: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    caption: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    likes: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    comments: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    views: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    shares: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    saves: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=True
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=True
    )

    region: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    geotag_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Topic(Base):

    __tablename__ = "topics"

    topic_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True
    )

    canonical_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    category_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    parent_topic_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    first_detected: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    last_active: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    inactive_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )


class PostTopicMap(Base):

    __tablename__ = "post_topic_map"

    post_id: Mapped[str] = mapped_column(
        ForeignKey(
            "posts.post_id"
        ),
        primary_key=True
    )

    topic_id: Mapped[str] = mapped_column(
        ForeignKey(
            "topics.topic_id"
        ),
        primary_key=True
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    entity_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

class TrendScore(Base):

    __tablename__ = "trend_scores"

    trend_score_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    topic_id: Mapped[str] = mapped_column(
        ForeignKey(
            "topics.topic_id"
        ),
        nullable=False
    )

    window: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    cycle_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    trend_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    trend_status: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    score_delta: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    growth_rate: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    momentum_score: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    velocity: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    source: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="instagram"
)