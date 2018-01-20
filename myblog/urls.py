from django.conf.urls import url
from .views import index, about_me, user_login, user_logout, user_register, article_detail, create_code_img, archive,comment_post, link_detail

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'me$', about_me, name='about'),
    url(r'^login$', user_login, name='login'),
    url(r'^logout$', user_logout, name='logout'),
    url(r'^register$', user_register, name='register'),
    url(r'^detail/(\d+)/$', article_detail, name='detail'),
    url(r'^create_code_img$', create_code_img),
    url(r'^archive$', archive, name='archive'), # 归档信息
    url(r'^comment_post$', comment_post, name='comment_post'), # comment_post
    url(r'^link_detail/(\d+)/$', link_detail, name='link_detail'), # comment_post
]
