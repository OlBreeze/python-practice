from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()


@router.get("/posts", response=List[PostOut])
def list_posts(request):
    return Post.objects.all()


@router.post("/posts", response=PostOut)
def create_post(request, payload: PostIn):
    post = Post.objects.create(user=request.user, **payload.dict())
    return post


@router.get("/posts/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    return get_object_or_404(Post, id=post_id)


@router.put("/posts/{post_id}", response=PostOut)
def update_post(request, post_id: int, payload: PostIn):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post


@router.delete("/posts/{post_id}")
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return {"success": True}


@router.post("/posts/{post_id}/comments", response=CommentOut)
def add_comment(request, post_id: int, payload: CommentIn):
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(post=post, user=request.user, **payload.dict())
    return comment


@router.post("/tags", response=TagOut)
def create_tag(request, payload: TagIn):
    tag = Tag.objects.create(**payload.dict())
    return tag


@router.post("/posts/{post_id}/tags/{tag_id}")
def add_tag_to_post(request, post_id: int, tag_id: int):
    post = get_object_or_404(Post, id=post_id)
    tag = get_object_or_404(Tag, id=tag_id)
    tag.posts.add(post)
    return {"success": True}
