"""
该例在上一版本flags_threadpool.py的基础上，
将download_many方法中的 excutor.map 改写为:
由futures.submit（创建和排定future对象）和 futures.as_completed（获取future结果）完成的函数。
"""
from concurrent import futures
import requests
import os
import sys
import time

# POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
POP20_CC = 'CN IN US ID BR PK'.split()
MAX_WORKERS = 20
BASE_URL = 'https://github.com/fluentpython/example-code'  # 发送请求地址
DEST_URL = 'downloads/'  # 存储到目的本地目录


# 发送请求返回图片
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


# 存储图片
def save_flag(img, filename):
    path = os.path.join(DEST_URL, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


# 输出进度
def show(text):
    print(text, end=' ')
    sys.stdout.flush()


# 单个下载-这是在各个线程中执行的函数
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # 设定几个workders表示设定几个并发线程
    with futures.ThreadPoolExecutor(3) as executor:
        # 创建并排定 future
        to_do = []
        for cc in cc_list:
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        results = []
        for future in futures.as_completed(to_do):  # futures.as_completed方法在future运行结束后产出future
            res = future.result()  # future.result在future运行结束后调用，返回可调用对象的结果。
            results.append(res)
            msg = '{} result: {}'
            print(msg.format(future, res))
    return len(results)


# 调用客户端代码
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
