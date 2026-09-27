from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """所有 ORM 数据表模型的共同基类。"""
    pass


class User(Base):
    """用户账号表。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="用户 ID",
    )

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        comment="登录用户名",
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        comment="密码哈希，绝不保存明文密码",
    )

    nickname: Mapped[str] = mapped_column(
        String(50),
        comment="对外展示昵称",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        comment="注册时间",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment="最后修改时间",
    )

    listings: Mapped[list[BookListing]] = relationship(
        back_populates="seller",
    )


class BookListing(Base):
    """一条二手教材发布帖。"""

    __tablename__ = "book_listings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="教材帖子 ID",
    )

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        comment="发布者用户 ID",
    )

    book_title: Mapped[str] = mapped_column(
        String(255),
        comment="教材书名",
    )

    author: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="作者",
    )

    edition: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="版次，例如第 4 版",
    )

    course_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
        comment="对应课程名称",
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        comment="售价",
    )

    book_condition: Mapped[str] = mapped_column(
        String(100),
        comment="成色和笔记情况",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="补充描述",
    )

    pickup_campus: Mapped[str] = mapped_column(
        String(20),
        comment="建议取书校区",
    )

    contact_info: Mapped[str] = mapped_column(
        String(100),
        comment="联系方式",
    )

    image_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="封面图片路径",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="on_sale",
        index=True,
        comment="状态：on_sale 或 sold",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        comment="发布时间",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment="最后修改时间",
    )

    seller: Mapped[User] = relationship(
        back_populates="listings",
    )