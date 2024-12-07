"""
该例说明使用concurrent.future框架实现并发下载保存各国国旗图片
"""
from concurrent import futures
import requests
import os
import sys
import time

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
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


"""
批量下载-这里是区分顺序下载还是并行下载的关键
"""
def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))


# 调用客户端代码
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
