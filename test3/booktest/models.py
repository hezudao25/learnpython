from django.db import models
import hashlib  # hashlib 加密hashlib.sha1('xxx').hexdigest()

# Create your models here.
class UserInfo(models.Model):
    """会员"""
    username = models.CharField(verbose_name='用户名', max_length=20, unique=True)
    password = models.CharField(verbose_name='密码', max_length=124)
    add_time = models.DateField(verbose_name='添加时间', auto_now=True)
    remark = models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)
    BAOMI = 'N'
    NAN = 'M'
    NV = 'N'
    GENGER_CHOIES = ((BAOMI, '保密'), (NAN, '男'), (NV, '女'))
    gener = models.CharField(verbose_name='性别', max_length=1, choices=GENGER_CHOIES, default=BAOMI,)
    areas = models.ForeignKey('AreaInfo', verbose_name='地区', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = '会员'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.password = hashlib.sha1((self.password + self.username).encode('utf-8')).hexdigest()
        super(UserInfo, self).save(*args, **kwargs)



# 自定义管理器
# 作用1：修改原有方法
# 作用2，添加新方法
class BookInfoManager(models.Manager):
    """自定义管理器"""
    # 1.改变查询的结果集
    def all(self):
        books = super().all()
        books = books.filter(id__gt=0)
        return books

    # 2. 封装函数：操作模型类对应的数据库（增删改查）
    def create_book(self, btitle, bpub_date):
        class_model = self.model
        #book = BookInfo()
        book = class_model()
        book.btitle = btitle
        book.bpub_date = bpub_date
        book.save()
        return book


#图书类
class BookInfo(models.Model):
    """图书模型类"""
    btitle = models.CharField(max_length=20, db_column='title')
    bpub_date = models.DateField()
    pic = models.ImageField(upload_to='book', null=True, blank=True, default=None)

    objects = BookInfoManager()

    def __str__(self):
        return self.btitle


    class Meta:
        db_table = 'books'



class HeroInfo(models.Model):
    """英雄任务模型类"""
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=False)
    hcomment = models.CharField(max_length=128)
    #关系属性
    hbook = models.ForeignKey('BookInfo', on_delete=models.CASCADE,)


    def __str__(self):
        return self.hname


    class Meta:
        db_table = 'heros'


class AreaInfo(models.Model):
    atitle = models.CharField(verbose_name='名称', max_length=20)
    aparent = models.ForeignKey('self', verbose_name='父类', null=True, blank=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.atitle

    class Meta:    # 元类，指定表名
        db_table = 'areas'
        verbose_name = '地区'
        verbose_name_plural = verbose_name



