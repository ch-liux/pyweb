from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# 获取图片验证码
class CaptchaUtil(object):
    
    def captcha(self):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return captcha


# 定义公共返回结果
class ResultView(object):

    def __init__(self):
        self.r = {
            "code":0,
            "msg":"",
            "data":[],
            "exec":""
        }
