import execjs


def encodePasswd(modulus, exponent, passwd):
    f = open("./LoginCrawl/encode/security.js", 'r', encoding='utf-8')  # 打开JS文件
    ctx = execjs.compile(f.read())  # 加载JS文件
    key = ctx.call('RSAencode', passwd, exponent, modulus)
    return key
