from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BlockedIPSMiddleware(MiddlewareMixin):
    """中间件类"""
    BLOCK_IP_LIST = ['192.168.1.151']

    # 作用在调用视图之前
    def process_view(self, request, view_func, *args, **kwargs):
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.BLOCK_IP_LIST:
            return HttpResponse("<h1>Forbindden</h1>")

