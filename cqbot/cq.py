from typing import List, Callable, Any, Dict, Union
import re

rule = r'(\[CQ:\w+(?:,\w+\=\S+?)+\])'


def escape(s):
    """
    转义
    :param s:
    :param quote:
    :return:
    """

    s = s.replace("&", "&amp;")
    s = s.replace("[", "&#91;")
    s = s.replace("]", "&#93;")
    s = s.replace(",", "&#44;")
    return s


def unescape(s):
    """
    反转义
    :param s:
    :param quote:
    :return:
    """

    s = s.replace("&amp;", "&")
    s = s.replace("&#91;", "[")
    s = s.replace("&#93;", "]")
    s = s.replace("&#44;", ",")
    return s


def g(key: str, value: Any, cond: Callable[[Any], bool], escape: bool = False, fail_break: bool = False):
    """
    :param key:
    :param value:
    :param cond: lambda 条件
    :param escape: 是否需要转义
    :param fail_break: 条件Fales是否直接return
    :return:
    """
    return [key, value, cond, escape, fail_break]


def attr_join(attrs: list[List]) -> str:
    """
    属性拼接

    示例: [
            [
                'key',
                value,
                lambda表达式,
                是否转义,
                是否表达式结果为False,直接返回
            ]
    ]
    :param attrs:
    :return:
    """
    items = []
    for v in attrs:
        if v[2](v[1]):
            val = v[1]
            if v[3]:
                val = escape(val)
            items.append(f'{v[0]}={val}')
            continue
        if v[4]:
            return ''
    return ','.join(items)


class CQ:
    """
    CQ码
    仅实现了可发送且没有风险的CQ码

    文档: https://docs.go-cqhttp.org/cqcode
    """

    @classmethod
    def face(cls, id: int) -> str:
        """
        qq 表情

        返回例子:  [CQ:face,id=123]

        文档: https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85
        :param id: 表情id
        :return: str
        """
        if id < 0:
            return ''

        return f'[CQ:face,id={id}]'

    @classmethod
    def record(cls,
               file: str = '',
               magic: int = 0,
               url: str = '',
               cache: int = 1,
               proxy: int = 1,
               timeout: int = 0) -> str:
        """
        语音

        返回例子:  [CQ:record,file=http://baidu.com/1.mp3]

        文档: https://docs.go-cqhttp.org/cqcode/#%E8%AF%AD%E9%9F%B3
        :param file: 语音文件名
        :param magic: 发送时可选, 默认 0, 设置为 1 表示变声
        :param url: 语音 URL
        :param cache: 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 1
        :param proxy: 只在通过网络 URL 发送时有效, 表示是否通过代理下载文件 ( 需通过环境变量或配置文件配置代理 ) , 默认 1
        :param timeout: 只在通过网络 URL 发送时有效, 单位秒, 表示下载网络文件的超时时间 , 默认不超时
        :return: str
        """

        file = file.strip()

        attrs = attr_join([
            g('file', file, lambda x: x != '', True, True),
            g('magic', magic, lambda x: x == 1),
        ])

        if attrs != '':
            return f'[CQ:record,{attrs}]'

        attrs = attr_join([
            g('url', url, lambda x: x != '', True, True),
            g('cache', cache, lambda x: x != 1),
            g('proxy', proxy, lambda x: x != 1),
            g('timeout', timeout, lambda x: x > 1),
        ])

        if attrs != '':
            return f'[CQ:record,{attrs}]'

        return ''

    @classmethod
    def video(cls, file: str, cover: str = '', c: int = 0) -> str:
        """
        短视频

        返回例子:  [CQ:video,file=http://baidu.com/1.mp4]

        文档: https://docs.go-cqhttp.org/cqcode/#%E7%9F%AD%E8%A7%86%E9%A2%91
        :param file: 视频地址, 支持http和file发送
        :param cover: 视频封面, 支持http, file和base64发送, 格式必须为jpg
        :param c: 通过网络下载视频时的线程数, 默认单线程. (在资源不支持并发时会自动处理)
        :return: str
        """
        attrs = attr_join([
            g('file', file, lambda x: x != '', True, True),
            g('cover', cover, lambda x: x != '', True),
            g('c', c, lambda x: x > 0),
        ])

        if attrs == '':
            return ''

        return f'[CQ:video,{attrs}]'

    @classmethod
    def at(cls, qq: int | str = 'all', name: str = '') -> str:
        """
        @某人

        返回例子:  [CQ:at,qq=123,name=不在群的QQ]

        文档: https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85
        :param qq: @的 QQ 号, all 表示全体成员
        :param name: 当在群中找不到此QQ号的名称时才会生效
        :return: str
        """

        attrs = attr_join([
            g('qq', qq, lambda x: True),
            g('name', name, lambda x: x != '', True),
        ])

        return f'[CQ:at,{attrs}]'

    @classmethod
    def share(cls, url: str, title: str, content: str = '', image: str = '') -> str:
        """
        链接分享

        返回例子:  [CQ:share,url=http://baidu.com,title=百度]

        文档: https://docs.go-cqhttp.org/cqcode/#%E9%93%BE%E6%8E%A5%E5%88%86%E4%BA%AB
        :param url: URL
        :param title: 标题
        :param content: 发送时可选, 内容描述
        :param image: 发送时可选, 图片 URL
        :return: str
        """

        attrs = attr_join([
            g('url', url, lambda x: x != '', True, True),
            g('title', title, lambda x: x != '', True, True),
            g('content', content, lambda x: x != '', True),
            g('image', image, lambda x: x != '', True),
        ])

        if attrs == '':
            return ''

        return f'[CQ:share,{attrs}]'

    @classmethod
    def music(cls, type: str, id: int = 0, url: str = '', audio: str = '', title: str = '', content: str = '',
              image: str = '') -> str:
        """
        音乐分享

        返回例子:  [CQ:music,type=163,id=28949129]

        文档: https://docs.go-cqhttp.org/cqcode/#%E9%9F%B3%E4%B9%90%E5%88%86%E4%BA%AB
        :param type: qq 163 xm custom, 分别表示使用 QQ 音乐、网易云音乐、虾米音乐、自定义
        :param id: 歌曲 ID
        :param url: 当type=custom时生效: 点击后跳转目标 URL
        :param audio: 当type=custom时生效: 音乐 URL
        :param title: 当type=custom时生效: 标题
        :param content: 当type=custom时生效: 发送时可选, 内容描述
        :param image: 当type=custom时生效: 发送时可选, 图片 URL
        :return: str
        """

        attrs = attr_join([
            g('type', type, lambda x: x != '', False, True),
            g('id', id, lambda x: x > 0),
            g('url', url, lambda x: x != '', True),
            g('audio', audio, lambda x: x != '', True),
            g('title', title, lambda x: x != '', True),
            g('content', content, lambda x: x != '', True),
            g('image', image, lambda x: x != '', True),
        ])

        if attrs == '':
            return ''

        return f'[CQ:music,{attrs}]'

    @classmethod
    def image(cls, file: str, type: str = '', subType: int = 0, url: str = '', cache: int = 1, id: int = 40000,
              c: int = 1) -> str:
        """
        图片

        返回例子:  [CQ:image,file=http://baidu.com/1.jpg,type=show,id=40004]

        文档: https://docs.go-cqhttp.org/cqcode/#%E5%9B%BE%E7%89%87
        :param file: 图片文件名，支持：绝对路径、网络 URL、Base64 编码
        :param type: 图片类型, flash 表示闪照, show 表示秀图, 默认普通图片
        :param subType: 图片子类型, 只出现在群聊.
        :param url: 图片 URL
        :param cache: 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 1
        :param id: 发送秀图时的特效id, 默认为40000
        :param c: 通过网络下载图片时的线程数, 默认单线程. (在资源不支持并发时会自动处理)
        :return: str
        """

        attrs = attr_join([
            g('file', file, lambda x: x != '', True, True),
            g('type', type, lambda x: x != ''),
            g('subType', subType, lambda x: x != 0),
            g('url', url, lambda x: x != '', True),
            g('cache', cache, lambda x: x != 1),
            g('id', id, lambda x: x != 40000),
            g('c', c, lambda x: x > 1),
        ])

        if attrs == '':
            return ''

        return f'[CQ:image,{attrs}]'

    @classmethod
    def reply(cls, id: int, text: str = '', qq: int = 0, time: int = 0, seq: int = 0) -> str:
        """
        回复

        如果 id 和 text 同时存在, 将采用自定义reply并替换原有信息 如果 id 获取失败, 将回退到自定义reply

        返回例子:  [CQ:reply,text=Hello World,qq=10086,time=3376656000,seq=5123]

        文档: https://docs.go-cqhttp.org/cqcode/#%E5%9B%9E%E5%A4%8D
        :param id: 回复时所引用的消息id, 必须为本群消息.
        :param text: 自定义回复的信息
        :param qq: 自定义回复时的自定义QQ, 如果使用自定义信息必须指定.
        :param time: 自定义回复时的时间, 格式为Unix时间
        :param seq: 起始消息序号, 可通过 get_msg 获得
        :return: str
        """
        attrs = attr_join([
            g('id', id, lambda x: x > 0, False, True),
            g('text', text, lambda x: x != '', True),
            g('qq', qq, lambda x: x > 0),
            g('time', time, lambda x: x > 0),
            g('seq', seq, lambda x: x > 0),
        ])

        if attrs == '':
            return ''

        return f'[CQ:reply,{attrs}]'

    @classmethod
    def poke(cls, qq: int) -> str:
        """
        戳一戳

        发送戳一戳消息无法撤回, 返回的 message id 恒定为 0

        返回例子:  [CQ:poke,qq=123456]

        文档: https://docs.go-cqhttp.org/cqcode/#%E6%88%B3%E4%B8%80%E6%88%B3
        :param qq: 需要戳的成员
        :return: str
        """
        if qq <= 0:
            return ''

        return f'[CQ:poke,qq={qq}]'

    @classmethod
    def gift(cls, qq: int, id: int) -> str:
        """
        礼物

        仅支持免费礼物, 发送群礼物消息 无法撤回, 返回的 message id 恒定为 0

        返回例子:  [CQ:gift,qq=123456,id=8]

        文档: https://docs.go-cqhttp.org/cqcode/#%E7%A4%BC%E7%89%A9
        :param qq: 需要戳的成员
        :param id: 礼物的类型
        :return: str
        """
        attrs = attr_join([
            g('qq', qq, lambda x: x > 0, False, True),
            g('id', id, lambda x: x > 0, False, True),
        ])

        if attrs == '':
            return ''

        return f'[CQ:gift,{attrs}]'

    @classmethod
    def tts(cls, text: str) -> str:
        """
        文本转语音

        通过TX的TTS接口, 采用的音源与登录账号的性别有关

        返回例子:  [CQ:tts,text=这是一条测试消息]

        文档: https://docs.go-cqhttp.org/cqcode/#%E6%96%87%E6%9C%AC%E8%BD%AC%E8%AF%AD%E9%9F%B3
        :param text: text
        :return: str
        """
        if text == '':
            return ''

        return f'[CQ:tts,text={text}]'

    @classmethod
    def parse(cls, message: str, code: str = '') -> Dict[str, Dict[str, Union[int, str]]]:
        """
        解析消息里的CQ码

        例子: [CQ:tts,text=message]xy[CQ:at,qq=123,name=jack]

        返回: {'tts': {'text': 'message'}, 'at': {'qq': 123, 'name': 'jack'}}

        :param code: 仅解析特定的cq码， 如: face
        :param message:
        :return:
        """
        cqs: Dict[str, Dict[str, Union[int, str]]] = {}
        for item in re.findall(rule,  message):
            group = str(item).lstrip('[').rstrip(']').split(',')
            if len(group) == 0:
                continue
            name = group[0][3:]
            if len(code) > 0 and name != code:
                continue

            fields: Dict[str, Union[int, str]] = {}
            for v in group[1:]:
                cols = v.split('=', 1)
                if len(cols) != 2:
                    continue
                fields[cols[0]] = unescape(cols[1])
            cqs[name] = fields

        return cqs

    @classmethod
    def replace(cls, message: str, repl: str = '') -> str:
        """
        替换消息里的cq码
        :param message:
        :param repl:
        :return:
        """
        return re.sub(rule, repl, message)


__all__ = ['CQ']
