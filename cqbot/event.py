import re
from typing import Any
from .action import *
from .enum import *


class EventPost(object):
    """
    事件上报有效通用数据
    """
    # 事件发生的unix时间戳
    time: int
    # 收到事件的机器人的 QQ 号
    self_id: int
    # 表示该上报的类型, 消息, 消息发送, 请求, 通知, 或元事件
    post_type: PostType

    def __init__(self, message_data: dict[str, Any]):
        self.time = int(message_data['time'])
        self.self_id = int(message_data['self_id'])
        self.post_type = PostType(message_data['post_type'])


class PostMessageMessageSender:
    """
    消息发送者的信息

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-message-messagesender
    """

    # 发送者 QQ 号
    user_id: int
    # 昵称
    nickname: str
    # 性别, male 或 female 或 unknown
    sex: str
    # 年龄
    age: int

    # ------- 当私聊类型为群临时会话时的额外字段 -------
    group_id: int | None

    # ------- 群聊时的额外字段 -------
    # 群名片／备注
    card: str | None
    # 地区
    area: str | None
    # 成员等级
    level: str | None
    # 角色, owner 或 admin 或 member
    role: str | None
    # 专属头衔
    title: str | None

    def __init__(self, sender: dict[str, Any]):
        self.user_id = int(sender['user_id'])
        self.age = int(sender['age'])
        self.nickname = sender['nickname']
        self.sex = sender['sex']

        self.group_id = sender.get('group_id', None)

        self.card = sender.get('card', None)
        self.area = sender.get('area', None)
        self.level = sender.get('level', None)
        self.role = sender.get('role', None)
        self.title = sender.get('title', None)


class Anonymous:
    """
    匿名信息
    """
    # 匿名用户id
    id: int
    # 匿名用户昵称
    name: str
    # 匿名用户 flag, 在调用禁言 API 时需要传入
    flag: str

    def __init__(self, anonymous: dict[str, Any]):
        self.id = anonymous.get('id', 0)
        self.name = anonymous.get('name', '')
        self.flag = anonymous.get('flag', '')


office_bots = [
    # q群管家
    2854196310,
    # 热议小助手
    2854209495,
    # 小冰
    2854196306,
    # 占卜师喵吉
    2854196318,
    # 暗区突围老皮
    2854203945,
    # 小YOYO
    2854203763,
    # 清安
    2854200554,
    # 小世界情报菌
    2854200454,
    # 玄中记卷卷
    2854214686,
    # 卧龙吟2乔妹
    2854211316,
    # 赞噢机器人
    2854204259,
    # QQ官方
    2854196320,
    # QQ小店助手
    2854196925,
    # Eva-创造恋人
    2854205672,
    # 小微欢乐多
    2854196324,
    # 表情包老铁
    2854196312,
    # 王者荣耀小狐狸
    2854196311,
    # 看点直播小助理
    2854215747,
    # DNF小酱油
    2854214473,
    # 英雄联盟 撸妹儿
    2854209507,
    # CODM-瘦普
    2854214941,
    # 火影忍者-豚豚
    2854211389,
    # 梦想新大陆-鲁鲁
    2854198999,
    # 黎明觉醒秀研
    2854216101,
    # 和平精英-小几
    2854196316,
    # 蒸汽机器人
    2854213468,
    # 奇迹Angela
    2854206897,
    # 小森村百科
    2854214963,
    # 饭团团
    2854211892,
    # 小莹机器人
    2854213893,
    # 阿暖
    2854202380,
    # 腾讯灯塔
    2854200812,
    # 蓝鲸信息流
    2854200449,
]


class EventMessage(EventPost):
    """
    post_type 为 message 或 message_sent 的上报将会有以下有效通用数据

    文档: https://docs.go-cqhttp.org/event/#%E6%B6%88%E6%81%AF%E4%B8%8A%E6%8A%A5
    """

    # 消息类型
    message_type: PostMessageType
    # 表示消息的子类型
    sub_type: PostMessageSubType
    # 消息 ID
    message_id: int
    # 发送者 QQ 号
    user_id: int
    # 一个消息链
    message: Any
    # CQ 码格式的消息
    raw_message: str
    # 字体
    font: int
    # 发送者信息
    sender: PostMessageMessageSender
    # 下面属性非通用数据
    # 消息序号
    message_seq: int | None
    # 临时对话的来源
    temp_source: PostMessageTempSource | None
    # 群ID
    group_id: str | None
    # 匿名信息, 如果不是匿名消息则为 null
    anonymous: Anonymous | None

    def __init__(self, message_data: dict[str, Any]):
        super().__init__(message_data)
        self.message_type = PostMessageType(message_data['message_type'])
        self.sub_type = PostMessageSubType(message_data['sub_type'])
        self.message_id = int(message_data['message_id'])
        self.user_id = int(message_data['user_id'])
        self.font = int(message_data['font'])
        self.raw_message = message_data['raw_message']
        self.message = message_data['message']
        self.sender = PostMessageMessageSender(message_data['sender'])

        self.message_seq = message_data.get('message_seq', None)
        if self.message_type == PostMessageType.PRIVATE:
            temp_source = message_data.get('temp_source', None)
            if temp_source is not None:
                self.temp_source = PostMessageTempSource(temp_source)
        elif self.message_type == PostMessageType.GROUP:
            self.group_id = message_data.get('group_id', None)
            anonymous = message_data.get('anonymous', None)
            if anonymous is not None:
                self.anonymous = Anonymous(anonymous)

    def is_at(self, qq: int | str = 0) -> bool:
        """
        某人是否被提及，默认是当前机器人
        :param qq: 查看指定QQ号是否被提及，或则all查看是不是提及了所有人，默认是查看当前机器人qq是否被提及
        :return:
        """
        if qq == 0:
            qq = self.self_id

        rule = rf'(\[CQ:at,qq\={qq}(,[a-z]+\=\S+)*\])'
        result = re.findall(rule, self.message)
        if len(result) == 0:
            return False
        return True

    def is_office_bot(self, qq: int = 0) -> bool:
        """
        当前消息是否是官方机器人发送的，也可以指定QQ查看是否是官方机器人
        :return:
        """
        if qq == 0:
            qq = self.user_id
        return qq in office_bots


class EventRequest(EventPost):
    """
    post_type 为 request 的上报会有以下有效通用数据

    文档: https://docs.go-cqhttp.org/event/#%E8%AF%B7%E6%B1%82%E4%B8%8A%E6%8A%A5
    """
    # 请求类型
    request_type: PostRequestType
    # 下面属性非通用数据
    # 发送请求的 QQ 号
    user_id: int | None
    # 验证信息
    comment: str | None
    # 请求 flag, 在调用处理请求的 API 时需要传入
    flag: str | None
    # add、invite 请求子类型, 分别表示加群请求、邀请登录号入群
    sub_type: str | None
    # 群号
    group_id: str | None

    def __init__(self, message_data: dict[str, Any]):
        super().__init__(message_data)
        self.request_type = PostRequestType(message_data['request_type'])

        self.user_id = message_data.get('user_id', None)
        self.comment = message_data.get('comment', None)
        self.flag = message_data.get('flag', None)
        self.sub_type = message_data.get('sub_type', None)
        self.group_id = message_data.get('group_id', None)


class EventNotice(EventPost):
    """
    post_type 为 notice 的上报会有以下有效通用数据

    文档: https://docs.go-cqhttp.org/event/#%E9%80%9A%E7%9F%A5%E4%B8%8A%E6%8A%A5
    """
    # 请求类型
    notice_type: PostNoticeType
    # 下面属性非通用数据
    # 私聊消息撤回[notice_type = friend_recall] 好友QQ
    # 群消息撤回[notice_type = group_recall] 消息发送者 QQ 号
    # 群成员增加[notice_type = group_increase] 加入者 QQ 号
    # 群成员减少[notice_type = group_decrease] 离开者 QQ 号
    # 群管理员变动[notice_type = group_decrease] 管理员 QQ 号
    # 群文件上传[notice_type = group_upload] 发送者 QQ 号
    # 群禁言[notice_type = group_ban] 被禁言 QQ 号 (为全员禁言时为0)
    # 好友添加[notice_type = friend_add] 新添加好友 QQ 号
    # 戳一戳（双击头像）[notice_type = notify, sub_type = poke] 发送者 QQ 号
    # 群红包运气王提示[notice_type = notify, sub_type = lucky_king] 红包发送者
    # 群成员荣誉变更提示[notice_type = notify, sub_type = honor] 成员id
    # 群成员头衔变更[notice_type = notify, sub_type = title] 变更头衔的用户 QQ 号
    # 群成员名片更新[notice_type = group_card] 成员id
    # 接收到离线文件[notice_type = offline_file] 发送者id
    user_id: int | None
    # 被撤回的消息 ID
    message_id: int | None
    # 群号
    group_id: int | None
    # 操作者 QQ 号
    operator_id: int | None
    # 群成员增加[notice_type = group_increase]事件子类型, 分别表示管理员已同意入群、管理员邀请入群: approve、invite
    # 群成员减少[notice_type = group_decrease]事件子类型, 分别表示主动退群、成员被踢、登录号被踢: leave、kick、kick_me
    # 群管理员变动[notice_type = group_admin]事件子类型, 分别表示设置和取消管理员: set、unset
    # 群禁言[notice_type = group_ban]事件子类型, 分别表示禁言、解除禁言: ban、lift_ban
    # 精华消息变更[notice_type = essence]事件子类型, 分别表示添加、移除: add、delete
    # 戳一戳（双击头像）[notice_type = notify, sub_type = poke]
    # 群红包运气王提示[notice_type = notify, sub_type = lucky_king]
    # 群成员荣誉变更提示[notice_type = notify, sub_type = honor]
    # 群成员头衔变更[notice_type = notify, sub_type = title]
    sub_type: str | None
    # 禁言时长, 单位秒 (为全员禁言时为-1)
    duration: int | None
    # 文件信息
    # 文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0
    file: dict[str, Any] | None
    # 发送者 QQ 号
    sender_id: int | None
    # 戳一戳（双击头像）[notice_type = notify, sub_type = poke] 被戳者
    # 群红包运气王提示[notice_type = notify, sub_type = lucky_king] 运气王id
    target_id: int | None
    # 荣誉类型: talkative - 龙王 、performer - 群聊之火 、emotion - 快乐源泉
    honor_type: str | None
    # 获得的新头衔
    title: str | None
    # 群成员名片更新 - 新名片
    card_new: str | None
    # 群成员名片更新 - 旧名片
    card_old: str | None
    # 客户端信息
    client: Any | None
    # 当前是否在线
    online: bool | None

    def __init__(self, message_data: dict[str, Any]):
        super().__init__(message_data)
        self.notice_type = PostNoticeType(message_data['notice_type'])

        self.user_id = message_data.get('user_id', None)
        self.message_id = message_data.get('message_id', None)
        self.group_id = message_data.get('group_id', None)
        self.operator_id = message_data.get('operator_id', None)
        self.sub_type = message_data.get('sub_type', None)
        self.duration = message_data.get('duration', None)
        self.file = message_data.get('file', None)
        self.sender_id = message_data.get('sender_id', None)
        self.target_id = message_data.get('target_id', None)
        self.honor_type = message_data.get('honor_type', None)
        self.title = message_data.get('title', None)
        self.card_new = message_data.get('card_new', None)
        self.card_old = message_data.get('card_old', None)
        self.client = message_data.get('client', None)
        self.online = message_data.get('online', None)


class EventMetaEvent(EventPost):
    """
    post_type 为 meta_event 的上报会有以下有效数据

    文档: https://docs.go-cqhttp.org/event/#%E5%85%83%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5
    """
    # 请求类型
    meta_event_type: PostMetaEventType
    # 下面属性非通用数据
    # 应用程序状态
    status: dict[str, Any] | None
    # 距离上一次心跳包的时间(单位是毫秒)
    interval: int | None
    # 生命周期子类型: enable, disable, connect
    sub_type: str | None

    def __init__(self, message_data: dict[str, Any]):
        super().__init__(message_data)
        self.meta_event_type = PostMetaEventType(message_data['meta_event_type'])
        self.status = message_data.get('status', None)
        self.interval = message_data.get('interval', None)
        self.sub_type = message_data.get('sub_type', None)


# 事件
class Event:

    # -------- post - message ----------

    def on_message_private(self, act: Action, msg: EventMessage):
        """
        私聊消息

        文档: https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_message_group(self, act: Action, msg: EventMessage):
        """
        群消息

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    # -------- post - notice ----------

    def on_notice_friend_recall(self, act: Action, msg: EventNotice):
        """
        私聊消息撤回

        文档: https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF%E6%92%A4%E5%9B%9E
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_recall(self, act: Action, msg: EventNotice):
        """
        群消息撤回

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF%E6%92%A4%E5%9B%9E
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_increase(self, act: Action, msg: EventNotice):
        """
        群成员增加

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_decrease(self, act: Action, msg: EventNotice):
        """
        群成员减少

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91
        :param msg:
        :return:
        """
        pass

    def on_notice_group_admin(self, act: Action, msg: EventNotice):
        """
        群管理员变动

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%AE%A1%E7%90%86%E5%91%98%E5%8F%98%E5%8A%A8
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_upload(self, act: Action, msg: EventNotice):
        """
        群文件上传

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_ban(self, act: Action, msg: EventNotice):
        """
        群禁言

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%A6%81%E8%A8%80
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_friend_add(self, act: Action, msg: EventNotice):
        """
        好友添加

        文档: https://docs.go-cqhttp.org/event/#%E5%A5%BD%E5%8F%8B%E6%B7%BB%E5%8A%A0
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_notify_poke(self, act: Action, msg: EventNotice):
        """
        戳一戳（双击头像）
        包含好友、群内

        文档: https://docs.go-cqhttp.org/event/#%E5%A5%BD%E5%8F%8B%E6%88%B3%E4%B8%80%E6%88%B3-%E5%8F%8C%E5%87%BB%E5%A4%B4%E5%83%8F
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_notify_lucky_king(self, act: Action, msg: EventNotice):
        """
        群红包运气王提示

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E7%BA%A2%E5%8C%85%E8%BF%90%E6%B0%94%E7%8E%8B%E6%8F%90%E7%A4%BA
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_notify_honor(self, act: Action, msg: EventNotice):
        """
        群成员荣誉变更提示

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E8%8D%A3%E8%AA%89%E5%8F%98%E6%9B%B4%E6%8F%90%E7%A4%BA
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_notify_title(self, act: Action, msg: EventNotice):
        """
        群成员头衔变更

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A4%B4%E8%A1%94%E5%8F%98%E6%9B%B4
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_group_card(self, act: Action, msg: EventNotice):
        """
        群成员名片更新

        文档: https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%90%8D%E7%89%87%E6%9B%B4%E6%96%B0
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_offline_file(self, act: Action, msg: EventNotice):
        """
        接收到离线文件

        文档: https://docs.go-cqhttp.org/event/#%E6%8E%A5%E6%94%B6%E5%88%B0%E7%A6%BB%E7%BA%BF%E6%96%87%E4%BB%B6
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_client_status(self, act: Action, msg: EventNotice):
        """
        其他客户端在线状态变更

        文档: https://docs.go-cqhttp.org/event/#%E5%85%B6%E4%BB%96%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%9C%A8%E7%BA%BF%E7%8A%B6%E6%80%81%E5%8F%98%E6%9B%B4
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_notice_essence(self, act: Action, msg: EventNotice):
        """
        精华消息变更

        文档: https://docs.go-cqhttp.org/event/#%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%8F%98%E6%9B%B4
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    # -------- post - request ----------

    def on_request_friend(self, act: Action, msg: EventRequest):
        """
        加好友请求

        文档: https://docs.go-cqhttp.org/event/#%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_request_group(self, msg: EventRequest):
        """
        加群请求／邀请

        文档: https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    # -------- post - meta ----------

    def on_meta_event_heartbeat(self, act: Action, msg: EventMetaEvent):
        """
        心跳包

        文档: https://docs.go-cqhttp.org/event/#%E5%BF%83%E8%B7%B3%E5%8C%85
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass

    def on_meta_event_lifecycle(self, act: Action, msg: EventMetaEvent):
        """
        生命周期

        文档: https://docs.go-cqhttp.org/event/#%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F
        :param act: api方法
        :param msg: 消息体
        :return:
        """
        pass


__all__ = [
    'EventPost',
    'PostMessageMessageSender',
    'Anonymous',
    'EventMessage',
    'EventRequest',
    'EventNotice',
    'EventMetaEvent',
    'Event',
]