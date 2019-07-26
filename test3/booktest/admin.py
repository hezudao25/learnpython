from django.contrib import admin
from booktest.models import UserInfo, BookInfo, HeroInfo, AreaInfo
# Register your models here.


class BookInfoAdmin(admin.ModelAdmin):
    """图书模型管理类"""
    list_display = ['id', 'btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = ['id', 'hname', 'hbook', 'hcomment']


class AreaStackedInline(admin.StackedInline):
    model = AreaInfo
    extra = 2


class AreaTabularInline(admin.TabularInline):
    model = AreaInfo  #多类的
    extra = 2


class AreaInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = ['atitle', 'aparent']
    list_per_page = 10 # 没有显示10条
    search_fields = ['atitle']
    fieldsets = (
        ('基本', {'fields':['atitle']}),
        ('高级', {'fields':['aparent']})
    )
    #inlines = [AreaStackedInline]
    inlines = [AreaTabularInline]


class UserInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = ['username', 'gener', 'areas', 'add_time']


# 注册模型类
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(UserInfo, UserInfoAdmin)