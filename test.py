import execjs
passwd='1312'
exponent='12321'
modulus='23123'
f = open("./LoginCrawl/encode/security.js", 'r', encoding='utf-8')  # 打开JS文件
ctx = execjs.compile(f.read())  # 加载JS文件
key = ctx.call('RSAencode', passwd, exponent, modulus)
print(key)

