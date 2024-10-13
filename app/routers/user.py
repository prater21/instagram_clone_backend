from collections import defaultdict
from fastapi import APIRouter, status, HTTPException, Request

from app.utils.authUtils import hash_pw, verify_pw
from app.schemas import (
    ChangePasswordBase,
    FollowBase,
    Message,
    ResetPasswordBase,
    UserInfoEditBase,
    UserResponseBase,
    ChangeProfileImg,
)
from app.models import Follow, User
from app.database import db_dependency
from app.utils.logger import log_request, log_request_auth
from app.utils.common import raise_error
from app.oauth2 import user_dependency

router = APIRouter()

# api list
# password reset
# update description
# update profile img


# 프로필 조회(팔로우 수, 팔로잉 수, 게시물 조회, 소개글, 이미지)
# 팔로우 조회, 팔로잉 조회
# 팔로우(등록, 취소)

# 프로필 사진 수정
# 유저네임 수정


@router.post("/password/reset", status_code=status.HTTP_200_OK, response_model=Message)
async def reset_password(
    db: db_dependency,
    request: Request,
    user_info: ResetPasswordBase,
):
    """
    reset password
    """
    log_request(request.url.path, request.method, user_info)
    user = db.query(User).filter(User.email == user_info.email).first()

    if user is None:
        raise_error(request.url.path, request.method, 406, "Invalid user info")

    user.password = hash_pw(user_info.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return Message(message="Password reset was successful")


@router.post("/password/change", status_code=status.HTTP_200_OK, response_model=Message)
async def change_password(
    db: db_dependency,
    request: Request,
    user_info: user_dependency,
    psw_info: ChangePasswordBase,
):
    """
    change password
    """
    log_request_auth(request.url.path, request.method, user_info.id, psw_info)

    if not verify_pw(psw_info.password, user_info.password):
        raise_error(request.url.path, request.method, 403, "Invalid Credentials")

    user_info.password = hash_pw(psw_info.new_password)
    db.add(user_info)
    db.commit()
    db.refresh(user_info)

    return Message(message="Password change successful")


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserResponseBase)
async def get_profile_info(
    db: db_dependency, request: Request, user_info: user_dependency, user_id: int
):
    """
    get user profile
    """
    # username, description, img, posts, following, follower
    log_request_auth(
        request.url.path,
        request.method,
        user_info.id,
        {"user_id": user_id},
    )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise_error(request.url.path, request.method, 404, "Not found user info")

    follower = [follower.user_id for follower in user.follower]
    following = [following.follow_id for following in user.following]
    my_following = []
    comment = []
    like = defaultdict(list)

    if user_info.id != user_id:
        my = db.query(User).filter(User.id == user_info.id).first()
        my_following = [following.follow_id for following in my.following]

    for post in user.post:
        for cmt in post.comment:
            comment.append(cmt.user_id)
        for li in post.like:
            like[post.id].append(li.user_id)

    user_ids = [
        *follower,
        *following,
        *comment,
        *my_following,
        *sum(like.values(), []),
    ]
    other_users = (
        db.query(User)
        .with_entities(User.id, User.username, User.profile_img)
        .filter(User.id.in_(set(user_ids)))
        .all()
    )

    follower_info = []
    following_info = []
    comment_info = {}
    like_info = defaultdict(list)
    is_follow = user_id in following
    if user_info.id == user_id:
        is_follow = None

    for other in other_users:
        other_info = {
            "id": other.id,
            "username": other.username,
            "profile_img": other.profile_img,
        }
        is_me = user_info.id == user_id
        if is_me:
            flag = other.id in following
        else:
            flag = other.id in my_following
        if other.id == user_info.id:
            flag = None

        if other.id in follower:
            follower_info.append({"flag": flag, **other_info})
        if other.id in following:
            following_info.append({"flag": 1 if is_me else flag, **other_info})
        if other.id in comment:
            comment_info[other.id] = other_info

    for id, users in like.items():
        for other in other_users:
            other_info = {
                "id": other.id,
                "username": other.username,
                "profile_img": other.profile_img,
            }
            is_me = user_info.id == user_id
            if is_me:
                flag = other.id in following
            else:
                flag = other.id in my_following
            if other.id == user_info.id:
                flag = None
            if other.id in users:
                like_info[id].append({"flag": flag, **other_info})

    user_likes = [like.post_id for like in user.like]
    ret = {
        "email": user.email,
        "username": user.username,
        "description": user.description,
        "profile_img": user.profile_img,
        "is_follow": is_follow,
        "post": [
            {
                "id": post.id,
                "username": user.username,
                "content": post.content,
                "reg_date": post.reg_date,
                "comment": [
                    {"content": comment.content, **comment_info[comment.user_id]}
                    for comment in post.comment
                ],
                "like": like_info[post.id],
                "like_flag": post.id in user_likes,
                "image": [img.url for img in sorted(post.image, key=lambda x: x.order)],
            }
            for post in sorted(user.post, key=lambda x: x.reg_date)
        ],
        "follower": follower_info,
        "following": following_info,
    }

    return UserResponseBase(**ret)


@router.post(
    "/profile_img/change", status_code=status.HTTP_200_OK, response_model=Message
)
async def change_profile_img(
    db: db_dependency,
    request: Request,
    user_info: user_dependency,
    profile_img: ChangeProfileImg,
):
    log_request_auth(request.url.path, request.method, user_info.id, profile_img)

    user = db.query(User).filter(User.id == user_info.id).first()

    if profile_img.flag:
        user.profile_img = None
    else:
        user.profile_img = profile_img.url

    db.add(user)
    db.commit()
    db.refresh(user)
    return Message(message="Profile image change successful")


@router.post("/follow", status_code=status.HTTP_200_OK, response_model=Message)
async def post_user_follow(
    db: db_dependency,
    request: Request,
    user_info: user_dependency,
    follow_info: FollowBase,
):
    log_request_auth(request.url.path, request.method, user_info.id, follow_info)

    if follow_info.flag:
        new_follow = Follow(user_id=user_info.id, follow_id=follow_info.follow_id)
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)

    else:
        follow_info = db.query(Follow).filter(
            Follow.user_id == user_info.id,
            Follow.follow_id == follow_info.follow_id,
        )
        if follow_info.first() is None:
            raise_error(request.url.path, request.method, 404, "Not found follow info")

        follow_info.delete()
        db.commit()

    return Message(message="Follow status changed successful")


@router.post("/profile/edit", status_code=status.HTTP_200_OK, response_model=Message)
async def edit_user_profile(
    db: db_dependency,
    request: Request,
    user_info: user_dependency,
    edit_user: UserInfoEditBase,
):
    log_request_auth(request.url.path, request.method, user_info.id, edit_user)

    username_dup = db.query(User).filter(User.username == edit_user.username).first()
    if username_dup:
        raise_error(request.url.path, request.method, 406, "Invalid username")

    user = db.query(User).filter(User.id == user_info.id).first()
    user.username = edit_user.username
    user.description = edit_user.description
    db.add(user)
    db.commit()
    db.refresh(user)

    return Message(message="profile edit successful")
