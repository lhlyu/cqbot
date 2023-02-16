from cqbot import *
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
