from enum import Enum, unique


@unique
class PostType(str, Enum):
    """
    枚举: 上报类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-type
    """
    # 消息
    MESSAGE = 'message'
    # 消息发送
    MESSAGE_SENT = 'message_sent'
    # 请求
    REQUEST = 'request'
    # 通知
    NOTICE = 'notice'
    # 元事件
    META_EVENT = 'meta_event'


@unique
class PostMessageType(str, Enum):
    """
    枚举: 消息类型

    文档：https://docs.go-cqhttp.org/reference/data_struct.html#post-message-type
    """
    # 私聊
    PRIVATE = 'private'
    # 群聊
    GROUP = 'group'

    def __str__(self) -> str:
        return self.value


@unique
class PostMessageSubType(str, Enum):
    """
    枚举: 消息子类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-message-type
    """
    # 好友
    FRIEND = 'friend'
    # 群聊
    NORMAL = 'normal'
    # 匿名
    ANONYMOUS = 'anonymous'
    # 群中自身发送
    GROUP_SELF = 'group_self'
    # 群临时会话
    GROUP = 'group'
    # 系统提示
    NOTICE = 'notice'

    def __str__(self) -> str:
        return self.value


@unique
class PostMessageTempSource(int, Enum):
    """
    枚举：消息来源
    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-message-tempsource
    """
    # 群聊
    GROUP = 0
    # qq咨询
    QQ_ZIXUN = 1
    # 查找
    LOOKUP = 2
    # qq电影
    QQ_FILM = 3
    # 热聊
    HOT_CHAT = 4
    # 验证消息
    VERIFY_MESSAGE = 6
    # 多人聊天
    MULTI_PERSON_CHAT = 7
    # 约会
    APPOINTMENT = 8
    # 通讯录
    ADDRESS_LIST = 9

    def __str__(self) -> int:
        return self.value


@unique
class PostRequestType(str, Enum):
    """
    枚举: 请求类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-request-type
    """
    # 好友
    FRIEND = 'friend'
    # 群
    GROUP = 'group'

    def __str__(self) -> str:
        return self.value


@unique
class PostNoticeType(str, Enum):
    """
    枚举: 通知类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-notice-type
    """
    # 群文件上传
    GROUP_UPLOAD = 'group_upload'
    # 群管理员变更
    GROUP_ADMIN = 'group_admin'
    # 群成员减少
    GROUP_DECREASE = 'group_decrease'
    # 群成员增加
    GROUP_INCREASE = 'group_increase'
    # 群成员禁言
    GROUP_BAN = 'group_ban'
    # 好友添加
    FRIEND_ADD = 'friend_add'
    # 群消息撤回
    GROUP_RECALL = 'group_recall'
    # 好友消息撤回
    FRIEND_RECALL = 'friend_recall'
    # 群名片变更
    GROUP_CARD = 'group_card'
    # 离线文件上传
    OFFLINE_FILE = 'offline_file'
    # 客户端状态变更
    CLIENT_STATUS = 'client_status'
    # 精华消息
    ESSENCE = 'essence'
    # 系统通知
    NOTIFY = 'notify'

    def __str__(self) -> str:
        return self.value


@unique
class PostNoticeNotifySubType(str, Enum):
    """
    枚举: 系统通知的子类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-notice-notify-subtype
    """
    # 群荣誉变更
    HONOR = 'honor'
    # 戳一戳
    POKE = 'poke'
    # 群红包幸运王
    LUCKY_KING = 'lucky_king'
    # 群成员头衔变更
    TITLE = 'title'

    def __str__(self) -> str:
        return self.value


@unique
class PostMetaEventType(str, Enum):
    """
    枚举: 元事件类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-metaevent-type
    """
    # 生命周期
    LIFECYCLE = 'lifecycle'
    # 心跳包
    HEARTBEAT = 'heartbeat'

    def __str__(self) -> str:
        return self.value


@unique
class PostMetaEventLifecycleType(str, Enum):
    """
    枚举: 生命周期上报的子类型

    文档: https://docs.go-cqhttp.org/reference/data_struct.html#post-metaevent-lifecycletype
    """
    # 启用
    ENABLE = 'enable'
    # 禁用
    DISABLE = 'disable'
    # 连接
    CONNECT = 'connect'

    def __str__(self) -> str:
        return self.value


__all__ = [
    'PostType',
    'PostMessageType',
    'PostMessageSubType',
    'PostMessageTempSource',
    'PostRequestType',
    'PostNoticeType',
    'PostNoticeNotifySubType',
    'PostMetaEventType',
    'PostMetaEventLifecycleType',
]
