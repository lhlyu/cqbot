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
