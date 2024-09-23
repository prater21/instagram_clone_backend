from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
import enum


# 유저
# id(int)
# email(varchar, 255)
# username(varchar, 30)
# pw(varchar, 255)
# name(varchar, 30)
# img_url(varchar, 255)
# description(varchar, 150)
# reg_date(datetime, deafult = now())


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    # name = Column(String(30))
    password = Column(
        String(255),
        nullable=False,
    )
    # profile_url = Column(String(255))
    description = Column(String(150))
    reg_date = Column(DateTime, default=datetime.datetime.now())

    post = relationship("Post", back_populates="user")
    comment = relationship("Comment", back_populates="user")
    like = relationship("Like", back_populates="user")

    follower = relationship(
        "Follow", back_populates="follower", foreign_keys="Follow.follow_id"
    )
    following = relationship(
        "Follow", back_populates="following", foreign_keys="Follow.user_id"
    )


# 게시글
# id(bigint)
# user_id(foreignkey(user.id))
# content(varchar(2000))
# reg_date(datetime, deafult = now())


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    content = Column(String(2000))
    reg_date = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", back_populates="post")
    comment = relationship("Comment", back_populates="post")
    like = relationship("Like", back_populates="post")
    image = relationship("Image", back_populates="post")
    # post_hashtag = relationship("PostHashtag", back_populates="post")


# 댓글
# id(bigint)
# user_id(foreignkey(user.id))
# post_id(foreignkey(post.id))
# content(varchar(2000))
# reg_date(datetime, deafult = now())


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    content = Column(String(255))
    reg_date = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")


# 게시글_좋아요
# id(bigint)
# user_id(foreignkey(user.id))
# post_id(foreignkey(post.id))
# reg_date(datetime, deafult = now())


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    reg_date = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", back_populates="like")
    post = relationship("Post", back_populates="like")


# 게시글_이미지
# id(bigint)
# post_id(foreignkey(post.id))
# url(varchar(255)))
# reg_date(datetime, deafult = now())


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    url = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False, default=1)
    reg_date = Column(DateTime, default=datetime.datetime.now())

    post = relationship("Post", back_populates="image")


# 해시태그
# id(bigint)
# name(varchar)


# class Hashtag(Base):
#     __tablename__ = "hashtag"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255))

#     post_hashtag = relationship("PostHashtag", back_populates="hashtag")


# 해시태그_게시글
# id(bigint)
# hashtag_id(foreignkey(hashtag.id))
# post_id(foreignkey(post.id))


# class PostHashtag(Base):
#     __tablename__ = "post_hashtag"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     hashtag_id = Column(Integer, ForeignKey("hashtag.id"))
#     post_id = Column(Integer, ForeignKey("post.id"))

#     post = relationship("Post", back_populates="post_hashtag")
#     hashtag = relationship("Hashtag", back_populates="post_hashtag")


# 팔로잉
# id(bigint)
# follower(foreignkey(user.id))
# followee(foreignkey(user.id))


class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    follow_id = Column(Integer, ForeignKey("user.id"))

    following = relationship("User", back_populates="following", foreign_keys=[user_id])
    follower = relationship("User", back_populates="follower", foreign_keys=[follow_id])


class AuthEmailStatus(enum.Enum):
    OK = "ok"
    READY = "ready"


class AuthEmail(Base):
    __tablename__ = "auth_email"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    auth_code = Column(String(6))
    auth_count = Column(String(20))
    status = Column(Enum(AuthEmailStatus))
    auth_date = Column(DateTime)
    expire_date = Column(DateTime)
