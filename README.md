# Cqbot

go-cqhttp python 框架，可以用于快速塔建 bot

## 安装

```shell
pip install cqbot
```

## 使用

可以从[examples](examples)文件夹下拷贝所需的文件

go-cqhttp需要去[releases](https://github.com/Mrs4s/go-cqhttp/releases)下载最新的文件

- 下面是我的目录结构，仅供参考

```
├── mybot - 项目目录
│   ├── bot.py - 机器人逻辑文件
│   ├── config.yml - go-cqhttp配置文件，根据自己的要求修改
│   ├── go-cqhttp - go-cqhttp执行文件，window下是exe结尾的文件
│   ├── Dockerfile - 构建镜像的文件
│   ├── run.sh - 脚本构建镜像并创建容器运行
```

- [config.yml配置](https://docs.go-cqhttp.org/guide/config.html#%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)
- [支持的事件](https://docs.go-cqhttp.org/event)
- [支持的API](https://docs.go-cqhttp.org/api)

## [例子](./examples)

### 第一种方式

```python
# pip install cqbot
from cqbot import *
# pip install addict
from addict import Dict

def to_json(obj: object):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


def on_message_group(act: Action, msg: EventMessage):
    # 打印消息体
    print('on_message_group:', to_json(msg))
    # 将用户的消息用bot发一遍
    act.send_group_msg(msg.group_id, msg.message)


def on_notice_group_recall(act: Action, msg: EventNotice):
    # 如果是撤回机器人的消息则不处理
    if msg.bot_id == msg.user_id:
        return
    print('on_notice_group_recall:', to_json(msg))
    # 获取被撤回的消息
    recall_msg = act.get_msg(msg.message_id)
    if recall_msg is None:
        return
    m = Dict(recall_msg)
    # 将撤回的消息重新发回群里
    message = f'[CQ:at,qq={m.data.sender.user_id}]撤回了一条消息: {m.data.message}'
    act.send_group_msg(msg.group_id, message)


if __name__ == '__main__':
    bot = Bot()
    # 处理群消息
    bot.on_message_group = on_message_group
    # 处理群消息撤回
    bot.on_notice_group_recall = on_notice_group_recall
    bot.run()
```

### 第二种方式

```python
# pip install cqbot
from cqbot import *
# pip install addict
from addict import Dict


def to_json(obj: object):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


# 自定义一个Bot,继承Bot,重写需要处理的事件
class MyBot(Bot):

    # 群消息处理
    def on_message_group(self, act: Action, msg: EventMessage):
        # 打印消息体
        print('on_message_group:', to_json(msg))
        # 将用户的消息用bot发一遍
        act.send_group_msg(msg.group_id, msg.message)

    # 群消息撤回处理
    def on_notice_group_recall(self, act: Action, msg: EventNotice):
        # 如果是撤回机器人的消息则不处理
        if msg.bot_id == msg.user_id:
            return
        print('on_notice_group_recall:', to_json(msg))
        # 获取被撤回的消息
        recall_msg = act.get_msg(msg.message_id)
        if recall_msg is None:
            return
        m = Dict(recall_msg)
        # 将撤回的消息重新发回群里
        message = f'[CQ:at,qq={m.data.sender.user_id}]撤回了一条消息: {m.data.message}'
        act.send_group_msg(msg.group_id, message)


if __name__ == '__main__':
    bot = MyBot()
    bot.run()

```