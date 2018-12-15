# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.five import readimg, input
from wechatsogou.filecache import WechatCache
from wechatsogou.exceptions import WechatSogouVcodeOcrException

ws_cache = WechatCache()

###########################################
def get_verify_code(im, typeid):

    verify_code = '****'
    url = 'http://api.ruokuai.com/create.json'
    params = {
        'typeid': typeid,
        'timeout': 60,
        'username': 'qili_spring',  # 用户名
        'password': 'liu19981124',  # 密码
        'softid': '117460',  # 软件Id
        'softkey': '375e3ded6ed74def977e6504284a5ab5'  # 软件Key
    }
    files = {
        'image': ('a.jpg', im)
    }
    headers = {
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'User-Agent': 'ben'
    }
    try:
        resp = requests.post(url, data=params, files=files, headers=headers)
    except Exception as e:
        print
        'get_verify_code error: ', e
        return verify_code
    try:
        verify_code = resp.json().get('Result', '')
    except Exception as e:
        print
        'get_verify_code failed: ', e
        return verify_code
    if not verify_code:
        try:
            print
            resp.text
        except:
            print
            'verify code resp is None'

    return verify_code


def identify_image_callback(self, img):
    code = get_verify_code(img, 3060)
    return code
###############################################

def identify_image_callback_by_hand(img):
    """识别二维码

    Parameters
    ----------
    img : bytes
        验证码图片二进制数据

    Returns
    -------
    str
        验证码文字
    """
    # im = readimg(img)
    # im.show()
    code = get_verify_code(img, 3060)
    return code


def unlock_sogou_callback_example(url, req, resp, img, identify_image_callback):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        验证码页面 之前的 url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    resp : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据
    identify_image_callback : callable
        处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

    Returns
    -------
    dict
        {
            'code': '',
            'msg': '',
        }
    """
    # no use resp
    url_quote = url.split('weixin.sogou.com/')[-1]
    unlock_url = 'http://weixin.sogou.com/antispider/thank.php'
    data = {
        'c': identify_image_callback(img),
        'r': '%2F' + url_quote,
        'v': 5
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + url_quote
    }
    r_unlock = req.post(unlock_url, data, headers=headers)
    if not r_unlock.ok:
        raise WechatSogouVcodeOcrException(
            'unlock[{}] failed: {}'.format(unlock_url, r_unlock.text, r_unlock.status_code))
	print(data)
	print(r_unlock.json())
    return r_unlock.json()


def unlock_weixin_callback_example(url, req, resp, img, identify_image_callback):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        验证码页面 之前的 url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    resp : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据
    identify_image_callback : callable
        处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

    Returns
    -------
    dict
        {
            'ret': '',
            'errmsg': '',
            'cookie_count': '',
        }
    """
    # no use resp

    unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
    data = {
        'cert': time.time() * 1000,
        'input': identify_image_callback(img)
    }
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': url
    }
    r_unlock = req.post(unlock_url, data, headers=headers)
    if not r_unlock.ok:
        raise WechatSogouVcodeOcrException(
            'unlock[{}] failed: {}[{}]'.format(unlock_url, r_unlock.text, r_unlock.status_code))

    return r_unlock.json()
