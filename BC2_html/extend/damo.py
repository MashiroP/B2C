from BC2_admin.models import category, category_Subcategory


def a ():
    context = { }
    context ['category'] = category.objects.all( )
    for i in context ['category']:
        context ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
    return context



def dxyzm (content,phone):
    import urllib
    import urllib.request
    import hashlib

    def md5 (str):
        import hashlib
        m = hashlib.md5( )
        m.update(str.encode("utf8"))
        return m.hexdigest( )

    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词',
        '51':'短信发送成功',
    }

    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = '643813251'
    # 短信平台密码
    password = md5('643813251')
    # 要发送的短信内容
    data = urllib.parse.urlencode({ 'u': user, 'p': password, 'm': phone, 'c': content })
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read( ).decode('utf-8')
    return statusStr [the_page]
