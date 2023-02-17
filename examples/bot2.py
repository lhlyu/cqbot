from cqbot import *
from addict import Dict


def to_json(obj: object):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


# 自定义一个Bot,继承Bot,重写需要处理的事件
class MyBot(Bot):

    # 群消息处理
    def on_message_group(self, act: Action, msg: EventMessage):
        # 打印消息体
        print('on_message_group:', to_json(msg))
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
