import logging
from django.db.models import Count
from io import BytesIO
from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from myblog.models import Article, User, Tag, Links, Comment
from .forms import RegisterForm, LoginForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
# 将check_code包放在合适的位置，导入即可，我是放在utils下面
from utils import check_code


logger = logging.getLogger('blog.views')

# 分页的抽象类
def get_page(request, article_list, per_page_num):
    paginator = Paginator(article_list, per_page_num)
    # 获取当前页数
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 若不是整数，就第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 若是空页面，就最后一页
        contacts = paginator.page(paginator.num_pages)

    return contacts


def index(request):
    articles = Article.objects.all()
    # 文章归档数据
    archive_list = Article.objects.distinct_date()
    # 标签
    tags = Tag.objects.all()
    # 友情链接
    links = Links.objects.all()
    # 按照评论进行排行
    comment_count_list =  Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = []
    for comment in comment_count_list:
        if comment['article']:
            # 由于取出来是list所以要取
            article_comment_list.append(Article.objects.get(pk=comment['article']))
    # 浏览量排行
    archive_click_list = Article.objects.order_by('click_count')
    # 按照是否推荐排行
    arts = Article.objects.filter(is_recommend=True)[:5]

    # 每页展示的数目
    per_page_num = 8
    # 分页
    cont = get_page(request, articles, per_page_num)
    context = {'context': cont, 'archive_list': archive_list, 'tags': tags, 'links':links,
               'article_comment_List':article_comment_list, 'archive_click_list':archive_click_list,
               'arts':arts
               }
    return render(request, 'myblog/index.html', context)


# 文章归档
def archive(request):
    # 获得传过来的year, month
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    # 按照年月过滤出文章
    article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
    # article_list = Article.objects.filter(date_publish__icoantains= year + '-' + month)
    # 分页
    # 每页数据
    per_page_num = 8
    cont = get_page(request, article_list, per_page_num)
    context = {'context': cont}
    return render(request, 'myblog/archive.html', context)

# 链接详情
def link_detail(request, id):
    links_detail = Links.objects.get(id=id)

    return render(request, 'myblog/link_detail.html', locals())


#详情页
def article_detail(request, id):
    try:
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
            # print(article)
            # 获取评论信息
            comments = Comment.objects.filter(article=article).order_by('id')
            # print(comments)
            comment_list = []
            for comment in comments:
                print(comment)
                # 判断是否有子评论
                for item in comment_list:
                    if not hasattr(item, 'children_comment'):
                        setattr(item, 'children_comment', [])
                    # 把子评论添加到评论
                    if comment.pid == item:
                        item.children_comment.append(comment)
                        break
                if comment.pid is None:
                    comment_list.append(comment)
            # 评论表单
            comment_form = CommentForm()

        except Article.DoesNotExist:
            return render(request, 'myblog/failure.html', {'reason': '没有找到对应的文章'})
    except Exception as e:
        logger.error(e)
    return render(request, 'myblog/detail.html', locals())

# 评论
def comment_post(request):
    # 获得form表单数据
    comment_form = CommentForm(request.POST)
    # 验证表单数据
    if comment_form.is_valid():
        # 写入数据库
        comment = Comment.objects.create(
            content= comment_form.cleaned_data['content'],
            # user = request.session.username,
            # article_id=comment_form.cleaned_data['comment'],
        )
        comment.save()
    else:
        return render(request, 'myblog/failure.html', {'reason': comment_form.errors})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# 关于我
def about_me(request):
    return render(request, 'myblog/aboutme.html')


# 生成验证码
def create_code_img(request):
    f = BytesIO()
    img, code = check_code.create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    # 定义cont_type相应内容为
    return HttpResponse(f.getvalue(), 'image/png')

# 登陆
def user_login(request):
    if request.method == 'POST':
        errors = {}
        obj = LoginForm(request.POST)
        print(obj)
        if obj.is_valid():
            post_check_code = request.POST.get('check_code')
            # print(post_check_code)
            session_check_code = request.session['check_code']
            # print(session_check_code)
            if post_check_code.lower() == session_check_code.lower():

                if request.POST.get('auto_login'):
                    # 会话有效期14天
                    request.session.set_expiry(60*60*24*14)
                    # print(request.session)
                else:
                    # 删除cookies
                   del request.COOKIES
                # 记住用户登陆状态
                request.session['is_login'] = True
                request.session['username'] = request.POST.get('name')
                return HttpResponseRedirect('/myblog/index')
            else:
                errors['check_code'] = '请输入正确的验证码！'
                return render(request, 'myblog/login.html', {'form': obj, 'errors': errors})
    else:
        obj = RegisterForm()
    return render(request,'myblog/login.html', {'form': obj})

# 注销
def user_logout(request):
    # 清楚会话
    request.session.flush()
    # 跳转到首页
    return HttpResponseRedirect('index')

# 注册
def user_register(request):
    if request.method == 'POST':
        # 获得注册form表单数据
        obj = RegisterForm(request.POST)
        print(obj)
        # 对注册表单的数据进行验证，返回验证后的数据，验证后的数据为cleaned——data
        if obj.is_valid():
            User.objects.create(
                name=obj.cleaned_data['name'],
                pwd =obj.cleaned_data['pwd'],
                Email = obj.cleaned_data['Email'],
                mobile = obj.cleaned_data['mobile'],
            )
            return HttpResponseRedirect('login')
    else:
        obj = RegisterForm()
    return render(request,'myblog/register.html', {'form':obj})







