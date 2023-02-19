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
│   ├── go-cqhttp - go-cqhttp执行文件，window下是exe结尾的文件， 如果使用docker构建不需要这个文件
│   ├── Dockerfile - 构建镜像的文件
│   ├── run.sh - 脚本构建镜像并创建容器运行
```

- [config.yml配置](https://docs.go-cqhttp.org/guide/config.html#%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)
- [支持的事件](https://docs.go-cqhttp.org/event)
- [支持的API](https://docs.go-cqhttp.org/api)
- [支持的CQ码](https://docs.go-cqhttp.org/cqcode)

## [例子](./examples)

### 第一种方式

```python
# pip install cqbot
import json
from typing import List, Any

# pip install addict
from addict import Dict

# pip install cqbot
from cqbot import *


def to_json(obj: object):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


on = True


def cmd_enable(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    global on
    on = True
    act.send_group_msg(msg.group_id, "已启动！")
    return True


def cmd_stop(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    global on
    on = False
    act.send_group_msg(msg.group_id, "已停止！")
    return True


def cmd_test(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    if len(args) == 0:
        # 当没有参数的时候打印帮助
        act.send_group_msg(msg.group_id, cmd.help())
        return
    # 将参数原样发回
    act.send_group_msg(msg.group_id, ' '.join(args))
    return True


# 设置指令
cmd = Cmd()
cmd.add('#启动', '启动程序', cmd_enable)
cmd.add('#停止', '停止程序', cmd_stop)
cmd.add('#测试', '#测试 你的内容', cmd_test)


def on_message_group(act: Action, msg: EventMessage):
    # 打印消息体
    print('on_message_group:', to_json(msg))
    # 如果是官方机器人则不处理
    if msg.is_office_bot():
        return
    # 执行指令
    if cmd.run(act, msg):
        return
    # 判断当前的消息是否at了机器人
    if msg.is_at():
        # 回复这条消息
        message = f'{CQ.at(msg.user_id)} 好的{CQ.face(124)}'
        act.send_group_msg(msg.group_id, message)
        # 再发送一条文字转语音
        message = f'{CQ.tts("人类的赞歌是勇气的赞歌，人类的伟大是勇气的伟大。")}'
        act.send_group_msg(msg.group_id, message)
        return


def on_notice_group_recall(act: Action, msg: EventNotice):
    # 如果是撤回机器人的消息则不处理
    if msg.self_id == msg.user_id:
        return
    print('on_notice_group_recall:', to_json(msg))
    # 获取被撤回的消息
    recall_msg = act.get_msg(msg.message_id)
    if recall_msg is None:
        return
    m = Dict(recall_msg)
    # 将撤回的消息重新发回群里
    message = f'{CQ.at(m.data.sender.user_id)}撤回了一条消息: {m.data.message}'
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
import json
from typing import List, Any

# pip install addict
from addict import Dict

# pip install cqbot
from cqbot import *


def to_json(obj: object):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


on = True


def cmd_enable(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    global on
    on = True
    act.send_group_msg(msg.group_id, "已启动！")
    return True


def cmd_stop(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    global on
    on = False
    act.send_group_msg(msg.group_id, "已停止！")
    return True


def cmd_test(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    if len(args) == 0:
        # 当没有参数的时候打印帮助
        act.send_group_msg(msg.group_id, cmd.help())
        return
    # 将参数原样发回
    act.send_group_msg(msg.group_id, ' '.join(args))
    return True


# 设置指令
cmd = Cmd()
cmd.add('#启动', '启动程序', cmd_enable)
cmd.add('#停止', '停止程序', cmd_stop)
cmd.add('#测试', '#测试 你的内容', cmd_test)


# 自定义一个Bot,继承Bot,重写需要处理的事件
class MyBot(Bot):

    # 群消息处理
    def on_message_group(self, act: Action, msg: EventMessage):
        # 打印消息体
        print('on_message_group:', to_json(msg))
        # 如果是官方机器人则不处理
        if msg.is_office_bot():
            return
        # 执行指令
        if cmd.run(act, msg):
            return
        # 判断当前的消息是否at了机器人
        if msg.is_at():
            # 回复这条消息
            message = f'{CQ.at(msg.user_id)} 好的{CQ.face(124)}'
            act.send_group_msg(msg.group_id, message)
            # 再发送一条文字转语音
            message = f'{CQ.tts("人类的赞歌是勇气的赞歌，人类的伟大是勇气的伟大。")}'
            act.send_group_msg(msg.group_id, message)
            return

    # 群消息撤回处理
    def on_notice_group_recall(self, act: Action, msg: EventNotice):
        # 如果是撤回机器人的消息则不处理
        if msg.self_id == msg.user_id:
            return
        print('on_notice_group_recall:', to_json(msg))
        # 获取被撤回的消息
        recall_msg = act.get_msg(msg.message_id)
        if recall_msg is None:
            return
        m = Dict(recall_msg)
        # 将撤回的消息重新发回群里
        message = f'{CQ.at(m.data.sender.user_id)}撤回了一条消息: {m.data.message}'
        act.send_group_msg(msg.group_id, message)


if __name__ == '__main__':
    bot = MyBot()
    bot.run()
```

### 直接使用Api

当`go-cqhttp`启动后可以直接使用`Action`方法

```python
# pip install cqbot
from cqbot import *


if __name__ == '__main__':
    # 连接go-cqhttp暴露的http
    act = Action('http://0.0.0.0:8000')
    # 直接指定群号发送消息
    act.send_group_msg(123, f'你好{CQ.face(78)}')
```

### CQ码使用

```python
# pip install cqbot
from cqbot import *

if __name__ == '__main__':
    # 输出: [CQ:at,qq=12313]
    print(CQ.at(12313))
    # 输出: [CQ:face,id=12]
    print(CQ.face(12))
    
```

### 指令使用

```python
from typing import List, Any
from cqbot import *

def cmd_test(act: Action, msg: EventMessage, args: List[Any]) -> bool:
    if len(args) == 0:
        act.send_group_msg(msg.group_id, cmd.help())
        return
    act.send_group_msg(msg.group_id, ' '.join(args))
    return True


# 设置指令
cmd = Cmd()
cmd.add('#测试1', '#测试 你的内容', cmd_test)
cmd.add('#测试2', '#测试 你的内容', cmd_test)


# 监听群消息
def on_message_group(act: Action, msg: EventMessage):
    # 执行指令
    cmd.run(act, msg)
```

## 一些问题

- 在服务器上部署后不好登录，或则提示账号设备不安全

> 可以在本地登录好，将 `session.token` `device.json` 一同上传到服务器，免去了登录的烦恼