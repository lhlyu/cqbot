import logging
from typing import Any
import requests
from .enum import *


class Action:
    """
    go-cqhttp 实现的API
    """

    def __init__(self, http: str):
        """
        初始化
        :param http: 请求地址
        """
        self.__http = http
        self.__request = requests.Session()
        pass

    def do_post(self, uri: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        """
        一个通用的post请求
        :param uri: 终结点
        :param payload: 参数
        :return: dict[str, Any] | None
        """
        headers = {'content-type': 'application/json; charset=utf-8'}
        api_url = f'{self.__http}{uri}'
        with self.__request.post(api_url, json=payload, headers=headers) as resp:
            if resp.status_code != 200:
                logging.error(resp.text)
                return None
            return resp.json()

    def send_private_msg(self, user_id: int, message: Any, group_id: int | None = None, auto_escape: bool = False) -> \
            dict[str, Any] | None:
        """
        发送私聊消息

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        :param user_id: 对方 QQ 号
        :param message: 要发送的内容
        :param group_id: 主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return: dict[str, Any] | None
        """
        uri = '/send_private_msg'
        payload = {
            'user_id': user_id,
            'message': message,
            'group_id': group_id,
            'auto_escape': auto_escape,
        }
        return self.do_post(uri, payload)

    def send_group_msg(self, group_id: int, message: Any, auto_escape: bool = False) -> dict[str, Any] | None:
        """
        发送群消息

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E6%B6%88%E6%81%AF
        :param group_id: 群号
        :param message: 要发送的内容
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return: dict[str, Any] | None
        """
        uri = '/send_group_msg'
        payload = {
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape,
        }
        return self.do_post(uri, payload)

    def send_group_forward_msg(self, group_id: int, messages: list[Any]) -> dict[str, Any] | None:
        """
        发送合并转发 ( 群 )

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91-%E7%BE%A4
        :param group_id: 群号
        :param messages: 自定义转发消息, 具体看 https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
        :return: dict[str, Any] | None
        """
        uri = '/send_group_forward_msg'
        payload = {
            'group_id': group_id,
            'messages': messages,
        }
        return self.do_post(uri, payload)

    def send_msg(self, message_type: PostMessageType, message: Any, user_id: int = 0, group_id: int = 0,
                 auto_escape: bool = False) -> dict[str, Any] | None:
        """
        发送群消息

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E6%B6%88%E6%81%AF
        :param message_type: 支持 private、group , 分别对应私聊、群组
        :param user_id: 对方 QQ 号 ( 消息类型为 private 时需要 )
        :param group_id: 群号 ( 消息类型为 group 时需要 )
        :param message: 要发送的内容
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return: dict[str, Any] | None
        """
        uri = '/send_msg'
        payload = {
            'message_type': message_type,
            'user_id': user_id,
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape,
        }
        return self.do_post(uri, payload)

    def delete_msg(self, message_id: int) -> dict[str, Any] | None:
        """
        撤回消息

        文档: https://docs.go-cqhttp.org/api/#%E6%92%A4%E5%9B%9E%E6%B6%88%E6%81%AF
        :param message_id: 消息ID
        :return: dict[str, Any] | None
        """
        uri = '/delete_msg'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def get_msg(self, message_id: int) -> dict[str, Any] | None:
        """
        获取消息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E6%B6%88%E6%81%AF
        :param message_id: 消息ID
        :return: dict[str, Any] | None
        """
        uri = '/get_msg'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def get_forward_msg(self, message_id: int) -> dict[str, Any] | None:
        """
        获取合并转发内容

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E5%86%85%E5%AE%B9
        :param message_id: 对应合并转发中的 id 字段
        :return: dict[str, Any] | None
        """
        uri = '/get_forward_msg'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def get_image(self, file: str) -> dict[str, Any] | None:
        """
        获取图片信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%9B%BE%E7%89%87%E4%BF%A1%E6%81%AF
        :param file: 图片缓存文件名
        :return: dict[str, Any] | None
        """
        uri = '/get_image'
        payload = {
            'file': file,
        }
        return self.do_post(uri, payload)

    def mark_msg_as_read(self, message_id: int) -> dict[str, Any] | None:
        """
        标记消息已读

        文档: https://docs.go-cqhttp.org/api/#%E6%A0%87%E8%AE%B0%E6%B6%88%E6%81%AF%E5%B7%B2%E8%AF%BB
        :param message_id: 消息ID
        :return: dict[str, Any] | None
        """
        uri = '/mark_msg_as_read'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False) -> dict[str, Any] | None:
        """
        群组踢人

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E8%B8%A2%E4%BA%BA
        :param group_id: 群号
        :param user_id: 要踢的 QQ 号
        :param reject_add_request: 拒绝此人的加群请求
        :return: dict[str, Any] | None
        """
        uri = '/set_group_kick'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'reject_add_request': reject_add_request,
        }
        return self.do_post(uri, payload)

    def set_group_ban(self, group_id: int, user_id: int, duration: int = 1800) -> dict[str, Any] | None:
        """
        群组单人禁言

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%8D%95%E4%BA%BA%E7%A6%81%E8%A8%80
        :param group_id: 群号
        :param user_id: 要踢的 QQ 号
        :param duration: 禁言时长, 单位秒, 0 表示取消禁言
        :return:
        """
        uri = '/set_group_ban'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'duration': duration,
        }
        return self.do_post(uri, payload)

    def set_group_anonymous_ban(self, group_id: int, anonymous: Any = None, anonymous_flag: str = '',
                                duration: int = 1800) -> dict[str, Any] | None:
        """
        群组匿名用户禁言
        anonymous 和 anonymous_flag 两者任选其一传入即可, 若都传入, 则使用 anonymous。

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%8C%BF%E5%90%8D%E7%94%A8%E6%88%B7%E7%A6%81%E8%A8%80
        :param group_id: 群号
        :param anonymous: 可选, 要禁言的匿名用户对象（群消息上报的 anonymous 字段）
        :param anonymous_flag: 可选, 要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
        :param duration: 禁言时长, 单位秒, 0 表示取消禁言
        :return: dict[str, Any] | None
        """
        uri = '/set_group_anonymous_ban'
        payload = {
            'group_id': group_id,
            'anonymous': anonymous,
            'anonymous_flag': anonymous_flag,
            'duration': duration,
        }
        return self.do_post(uri, payload)

    def set_group_whole_ban(self, group_id: int, enable: bool = True) -> dict[str, Any] | None:
        """
        群组全员禁言

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%85%A8%E5%91%98%E7%A6%81%E8%A8%80
        :param group_id: 群号
        :param enable: 是否禁言
        :return: dict[str, Any] | None
        """
        uri = '/set_group_whole_ban'
        payload = {
            'group_id': group_id,
            'enable': enable,
        }
        return self.do_post(uri, payload)

    def set_group_admin(self, group_id: int, user_id: int, enable: bool = True) -> dict[str, Any] | None:
        """
        群组设置管理员

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E8%AE%BE%E7%BD%AE%E7%AE%A1%E7%90%86%E5%91%98
        :param group_id: 群号
        :param user_id: 要设置管理员的 QQ 号
        :param enable: true 为设置, false 为取消
        :return: dict[str, Any] | None
        """
        uri = '/set_group_admin'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'enable': enable,
        }
        return self.do_post(uri, payload)

    def set_group_anonymous(self, group_id: int, enable: bool = True) -> dict[str, Any] | None:
        """
        群组匿名

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%8C%BF%E5%90%8D
        :param group_id: 群号
        :param enable: 是否允许匿名聊天
        :return: dict[str, Any] | None
        """
        uri = '/set_group_anonymous'
        payload = {
            'group_id': group_id,
            'enable': enable,
        }
        return self.do_post(uri, payload)

    def set_group_card(self, group_id: int, user_id: int, card: str = '') -> dict[str, Any] | None:
        """
        设置群名片 ( 群备注 )

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D%E7%89%87-%E7%BE%A4%E5%A4%87%E6%B3%A8
        :param group_id: 群号
        :param user_id: 要设置的 QQ 号
        :param card: 群名片内容, 不填或空字符串表示删除群名片
        :return: dict[str, Any] | None
        """
        uri = '/set_group_card'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'card': card,
        }
        return self.do_post(uri, payload)

    def set_group_name(self, group_id: int, group_name: str) -> dict[str, Any] | None:
        """
        设置群名

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D
        :param group_id: 群号
        :param group_name: 新群名
        :return: dict[str, Any] | None
        """
        uri = '/set_group_name'
        payload = {
            'group_id': group_id,
            'group_name': group_name,
        }
        return self.do_post(uri, payload)

    def set_group_leave(self, group_id: int, is_dismiss: bool = False) -> dict[str, Any] | None:
        """
        退出群组

        文档: https://docs.go-cqhttp.org/api/#%E9%80%80%E5%87%BA%E7%BE%A4%E7%BB%84
        :param group_id: 群号
        :param is_dismiss: 是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散
        :return: dict[str, Any] | None
        """
        uri = '/set_group_leave'
        payload = {
            'group_id': group_id,
            'is_dismiss': is_dismiss,
        }
        return self.do_post(uri, payload)

    def set_group_special_title(self, group_id: int, user_id: int, special_title: str = '', duration: int = -1) -> dict[
                                                                                                                       str, Any] | None:
        """
        设置群组专属头衔

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E7%BB%84%E4%B8%93%E5%B1%9E%E5%A4%B4%E8%A1%94
        :param group_id: 群号
        :param user_id: 要设置的 QQ 号
        :param special_title: 专属头衔, 不填或空字符串表示删除专属头衔
        :param duration: 专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果, 可能是只有某些特殊的时间长度有效, 有待测试
        :return: dict[str, Any] | None
        """
        uri = '/set_group_special_title'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'special_title': special_title,
            'duration': duration,
        }
        return self.do_post(uri, payload)

    def send_group_sign(self, group_id: int) -> dict[str, Any] | None:
        """
        群打卡

        文档: https://docs.go-cqhttp.org/api/#%E7%BE%A4%E6%89%93%E5%8D%A1
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/send_group_sign'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def set_friend_add_request(self, flag: str, approve: bool = True, remark: str = '') -> dict[str, Any] | None:
        """
        处理加好友请求

        文档: https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82
        :param flag: 加好友请求的 flag（需从上报的数据中获得）
        :param approve: 是否同意请求
        :param remark: 添加后的好友备注（仅在同意时有效）
        :return: dict[str, Any] | None
        """
        uri = '/set_friend_add_request'
        payload = {
            'flag': flag,
            'approve': approve,
            'remark': remark,
        }
        return self.do_post(uri, payload)

    def set_group_add_request(self, flag: str, sub_type: str, approve: bool = True, reason: str = '') -> dict[
                                                                                                             str, Any] | None:
        """
        处理加群请求／邀请

        文档: https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        :param flag: 加群请求的 flag（需从上报的数据中获得）
        :param sub_type: add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）
        :param approve: 是否同意请求／邀请
        :param reason: 拒绝理由（仅在拒绝时有效）
        :return: dict[str, Any] | None
        """
        uri = '/set_group_add_request'
        payload = {
            'flag': flag,
            'sub_type': sub_type,
            'approve': approve,
            'reason': reason,
        }
        return self.do_post(uri, payload)

    def get_login_info(self) -> dict[str, Any] | None:
        """
        获取登录号信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%99%BB%E5%BD%95%E5%8F%B7%E4%BF%A1%E6%81%AF
        :return: dict[str, Any] | None
        """
        uri = '/get_login_info'
        payload = {}
        return self.do_post(uri, payload)

    def set_qq_profile(self, nickname: str, company: str, email: str, college: str, personal_note: str) -> dict[
                                                                                                               str, Any] | None:
        """
        设置登录号资料

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%99%BB%E5%BD%95%E5%8F%B7%E8%B5%84%E6%96%99
        :param nickname: 名称
        :param company: 公司
        :param email: 邮箱
        :param college: 学校
        :param personal_note: 个人说明
        :return: dict[str, Any] | None
        """
        uri = '/set_qq_profile'
        payload = {
            'nickname': nickname,
            'company': company,
            'email': email,
            'college': college,
            'personal_note': personal_note,
        }
        return self.do_post(uri, payload)

    def get_stranger_info(self, user_id: int, no_cache: bool = False) -> dict[str, Any] | None:
        """
        获取陌生人信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E9%99%8C%E7%94%9F%E4%BA%BA%E4%BF%A1%E6%81%AF
        :param user_id: QQ 号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return: dict[str, Any] | None
        """
        uri = '/get_stranger_info'
        payload = {
            'user_id': user_id,
            'no_cache': no_cache,
        }
        return self.do_post(uri, payload)

    def get_friend_list(self) -> dict[str, Any] | None:
        """
        获取好友列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8
        :return: dict[str, Any] | None
        """
        uri = '/get_friend_list'
        payload = {}
        return self.do_post(uri, payload)

    def get_unidirectional_friend_list(self) -> dict[str, Any] | None:
        """
        获取单向好友列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%8D%95%E5%90%91%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8
        :return: dict[str, Any] | None
        """
        uri = '/get_unidirectional_friend_list'
        payload = {}
        return self.do_post(uri, payload)

    def delete_friend(self, user_id: int) -> dict[str, Any] | None:
        """
        删除好友

        文档: https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E5%A5%BD%E5%8F%8B
        :param user_id: 好友 QQ 号
        :return: dict[str, Any] | None
        """
        uri = '/delete_friend'
        payload = {
            'user_id': user_id,
        }
        return self.do_post(uri, payload)

    def get_group_info(self, group_id: int, no_cache: bool = False) -> dict[str, Any] | None:
        """
        获取群信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E4%BF%A1%E6%81%AF
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return: dict[str, Any] | None
        """
        uri = '/get_group_info'
        payload = {
            'group_id': group_id,
            'no_cache': no_cache,
        }
        return self.do_post(uri, payload)

    def get_group_list(self, no_cache: bool = False) -> dict[str, Any] | None:
        """
        获取群列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%88%97%E8%A1%A8
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return: dict[str, Any] | None
        """
        uri = '/get_group_list'
        payload = {
            'no_cache': no_cache
        }
        return self.do_post(uri, payload)

    def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False) -> dict[str, Any] | None:
        """
        获取群成员信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF
        :param group_id: 群号
        :param user_id: QQ 号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return: dict[str, Any] | None
        """
        uri = '/get_group_member_info'
        payload = {
            'group_id': group_id,
            'user_id': user_id,
            'no_cache': no_cache,
        }
        return self.do_post(uri, payload)

    def get_group_member_list(self, group_id: int, no_cache: bool = False) -> dict[str, Any] | None:
        """
        获取群成员列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E5%88%97%E8%A1%A8
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return: dict[str, Any] | None
        """
        uri = '/get_group_member_list'
        payload = {
            'group_id': group_id,
            'no_cache': no_cache,
        }
        return self.do_post(uri, payload)

    def get_group_honor_info(self, group_id: int, type: str) -> dict[str, Any] | None:
        """
        获取群荣誉信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E8%8D%A3%E8%AA%89%E4%BF%A1%E6%81%AF
        :param group_id: 群号
        :param type: 要获取的群荣誉类型, 可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据, 或传入 all 获取所有数据
        :return: dict[str, Any] | None
        """
        uri = '/get_group_honor_info'
        payload = {
            'group_id': group_id,
            'type': type,
        }
        return self.do_post(uri, payload)

    def can_send_image(self) -> dict[str, Any] | None:
        """
        检查是否可以发送图片

        文档: https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87
        :return: dict[str, Any] | None
        """
        uri = '/can_send_image'
        payload = {}
        return self.do_post(uri, payload)

    def can_send_record(self) -> dict[str, Any] | None:
        """
        检查是否可以发送语音

        文档: https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E8%AF%AD%E9%9F%B3
        :return: dict[str, Any] | None
        """
        uri = '/can_send_record'
        payload = {}
        return self.do_post(uri, payload)

    def get_version_info(self, x: int) -> dict[str, Any] | None:
        """
        获取版本信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%89%88%E6%9C%AC%E4%BF%A1%E6%81%AF
        :param x:
        :return: dict[str, Any] | None
        """
        uri = '/get_version_info'
        payload = {
            'x': x,
        }
        return self.do_post(uri, payload)

    def set_group_portrait(self, group_id: int, file: str, cache: int) -> dict[str, Any] | None:
        """
        设置群头像

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%A4%B4%E5%83%8F
        :param group_id: 群号
        :param file: 图片文件名
        :param cache: 表示是否使用已缓存的文件
        :return: dict[str, Any] | None
        """
        uri = '/set_group_portrait'
        payload = {
            'group_id': group_id,
            'file': file,
            'cache': cache,
        }
        return self.do_post(uri, payload)

    def get_group_system_msg(self, invited_requests: list[Any], join_requests: list[Any]) -> dict[str, Any] | None:
        """
        获取群系统消息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E7%B3%BB%E7%BB%9F%E6%B6%88%E6%81%AF
        :param invited_requests: 邀请消息列表
        :param join_requests: 进群消息列表
        :return: dict[str, Any] | None
        """
        uri = '/get_group_system_msg'
        payload = {
            'invited_requests': invited_requests,
            'join_requests': join_requests,
        }
        return self.do_post(uri, payload)

    def upload_private_file(self, group_id: int, file: str, name: str) -> dict[str, Any] | None:
        """
        上传私聊文件

        文档: https://docs.go-cqhttp.org/api/#%E4%B8%8A%E4%BC%A0%E7%A7%81%E8%81%8A%E6%96%87%E4%BB%B6
        :param group_id: 群号
        :param file: 本地文件路径
        :param name: 储存名称
        :return: dict[str, Any] | None
        """
        uri = '/upload_private_file'
        payload = {
            'group_id': group_id,
            'file': file,
            'name': name,
        }
        return self.do_post(uri, payload)

    def upload_group_file(self, group_id: int, file: str, name: str, folder: str) -> dict[str, Any] | None:
        """
        上传群文件

        文档: https://docs.go-cqhttp.org/api/#%E4%B8%8A%E4%BC%A0%E7%BE%A4%E6%96%87%E4%BB%B6
        :param group_id: 群号
        :param file: 本地文件路径
        :param name: 储存名称
        :param folder: 父目录ID
        :return: dict[str, Any] | None
        """
        uri = '/upload_group_file'
        payload = {
            'group_id': group_id,
            'file': file,
            'name': name,
            'folder': folder,
        }
        return self.do_post(uri, payload)

    def get_group_file_system_info(self, group_id: int) -> dict[str, Any] | None:
        """
        获取群文件系统信息

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BF%A1%E6%81%AF
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/get_group_file_system_info'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def get_group_root_files(self, group_id: int) -> dict[str, Any] | None:
        """
        获取群根目录文件列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%A0%B9%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/get_group_root_files'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def get_group_files_by_folder(self, group_id: int, folder_id: str) -> dict[str, Any] | None:
        """
        获取群子目录文件列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%AD%90%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8
        :param group_id: 群号
        :param folder_id: 文件夹ID 参考 Folder 对象
        :return: dict[str, Any] | None
        """
        uri = '/get_group_files_by_folder'
        payload = {
            'group_id': group_id,
            'folder_id': folder_id,
        }
        return self.do_post(uri, payload)

    def create_group_file_folder(self, group_id: int, name: str, parent_id: str = '/') -> dict[str, Any] | None:
        """
        创建群文件文件夹
        仅能在根目录创建文件夹

        文档: https://docs.go-cqhttp.org/api/#%E5%88%9B%E5%BB%BA%E7%BE%A4%E6%96%87%E4%BB%B6%E6%96%87%E4%BB%B6%E5%A4%B9
        :param group_id: 群号
        :param name: 文件夹名称
        :param parent_id: 仅能为 /
        :return: dict[str, Any] | None
        """
        uri = '/create_group_file_folder'
        payload = {
            'group_id': group_id,
            'name': name,
            'parent_id': parent_id,
        }
        return self.do_post(uri, payload)

    def delete_group_folder(self, group_id: int, folder_id: str) -> dict[str, Any] | None:
        """
        删除群文件文件夹

        文档: https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E7%BE%A4%E6%96%87%E4%BB%B6%E6%96%87%E4%BB%B6%E5%A4%B9
        :param group_id: 群号
        :param folder_id: 文件夹ID 参考 Folder 对象
        :return: dict[str, Any] | None
        """
        uri = '/delete_group_folder'
        payload = {
            'group_id': group_id,
            'folder_id': folder_id,
        }
        return self.do_post(uri, payload)

    def delete_group_file(self, group_id: int, file_id: str, busid: int) -> dict[str, Any] | None:
        """
        删除群文件

        文档: https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E7%BE%A4%E6%96%87%E4%BB%B6
        :param group_id: 群号
        :param file_id: 文件ID 参考 File 对象
        :param busid: 文件类型 参考 File 对象
        :return: dict[str, Any] | None
        """
        uri = '/delete_group_file'
        payload = {
            'group_id': group_id,
            'file_id': file_id,
            'busid': busid,
        }
        return self.do_post(uri, payload)

    def get_group_file_url(self, group_id: int, file_id: str, busid: int) -> dict[str, Any] | None:
        """
        获取群文件资源链接

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E8%B5%84%E6%BA%90%E9%93%BE%E6%8E%A5
        :param group_id: 群号
        :param file_id: 文件ID 参考 File 对象
        :param busid: 文件类型 参考 File 对象
        :return: dict[str, Any] | None
        """
        uri = '/get_group_file_url'
        payload = {
            'group_id': group_id,
            'file_id': file_id,
            'busid': busid,
        }
        return self.do_post(uri, payload)

    def get_status(self) -> dict[str, Any] | None:
        """
        获取状态

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%8A%B6%E6%80%81
        :return: dict[str, Any] | None
        """
        uri = '/get_status'
        payload = {}
        return self.do_post(uri, payload)

    def get_group_at_all_remain(self, group_id: int) -> dict[str, Any] | None:
        """
        获取群 @全体成员 剩余次数

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4-%E5%85%A8%E4%BD%93%E6%88%90%E5%91%98-%E5%89%A9%E4%BD%99%E6%AC%A1%E6%95%B0
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/get_group_at_all_remain'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def _send_group_notice(self, group_id: int, content: str, image: str = '') -> dict[str, Any] | None:
        """
        发送群公告

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E5%85%AC%E5%91%8A
        :param group_id: 群号
        :param content: 公告内容
        :param image: 图片路径（可选）
        :return: dict[str, Any] | None
        """
        uri = '/_send_group_notice'
        payload = {
            'group_id': group_id,
            'content': content,
            'image': image,
        }
        return self.do_post(uri, payload)

    def _get_group_notice(self, group_id: int) -> dict[str, Any] | None:
        """
        获取群公告

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%85%AC%E5%91%8A
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/_get_group_notice'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def reload_event_filter(self, file: str) -> dict[str, Any] | None:
        """
        重载事件过滤器

        文档: https://docs.go-cqhttp.org/api/#%E9%87%8D%E8%BD%BD%E4%BA%8B%E4%BB%B6%E8%BF%87%E6%BB%A4%E5%99%A8
        :param file: 事件过滤器文件
        :return: dict[str, Any] | None
        """
        uri = '/reload_event_filter'
        payload = {
            'file': file,
        }
        return self.do_post(uri, payload)

    def download_file(self, url: str, thread_count: int, headers: str | list) -> dict[str, Any] | None:
        """
        下载文件到缓存目录

        文档: https://docs.go-cqhttp.org/api/#%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6%E5%88%B0%E7%BC%93%E5%AD%98%E7%9B%AE%E5%BD%95
        :param url: 链接地址
        :param thread_count: 下载线程数
        :param headers: 自定义请求头
        :return: dict[str, Any] | None
        """
        uri = '/download_file'
        payload = {
            'url': url,
            'thread_count': thread_count,
            'headers': headers,
        }
        return self.do_post(uri, payload)

    def get_online_clients(self, no_cache: bool) -> dict[str, Any] | None:
        """
        获取当前账号在线客户端列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E8%B4%A6%E5%8F%B7%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%88%97%E8%A1%A8
        :param no_cache: 是否无视缓存
        :return: dict[str, Any] | None
        """
        uri = '/get_online_clients'
        payload = {
            'no_cache': no_cache,
        }
        return self.do_post(uri, payload)

    def get_group_msg_history(self, message_seq: int, group_id: int) -> dict[str, Any] | None:
        """
        获取群消息历史记录

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%B6%88%E6%81%AF%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95
        :param message_seq: 起始消息序号, 可通过 get_msg 获得
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/get_group_msg_history'
        payload = {
            'message_seq': message_seq,
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def set_essence_msg(self, message_id: int) -> dict[str, Any] | None:
        """
        设置精华消息

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF
        :param message_id: 消息ID
        :return: dict[str, Any] | None
        """
        uri = '/set_essence_msg'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def delete_essence_msg(self, message_id: int) -> dict[str, Any] | None:
        """
        移出精华消息

        文档: https://docs.go-cqhttp.org/api/#%E7%A7%BB%E5%87%BA%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF
        :param message_id: 消息ID
        :return: dict[str, Any] | None
        """
        uri = '/delete_essence_msg'
        payload = {
            'message_id': message_id,
        }
        return self.do_post(uri, payload)

    def get_essence_msg_list(self, group_id: int) -> dict[str, Any] | None:
        """
        获取精华消息列表

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%88%97%E8%A1%A8
        :param group_id: 群号
        :return: dict[str, Any] | None
        """
        uri = '/get_essence_msg_list'
        payload = {
            'group_id': group_id,
        }
        return self.do_post(uri, payload)

    def check_url_safely(self, url: str) -> dict[str, Any] | None:
        """
        检查链接安全性

        文档: https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E9%93%BE%E6%8E%A5%E5%AE%89%E5%85%A8%E6%80%A7
        :param url: 需要检查的链接
        :return: dict[str, Any] | None
        """
        uri = '/check_url_safely'
        payload = {
            'url': url,
        }
        return self.do_post(uri, payload)

    def _get_model_show(self, model: str) -> dict[str, Any] | None:
        """
        获取在线机型

        文档: https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%9C%A8%E7%BA%BF%E6%9C%BA%E5%9E%8B
        :param model: 机型名称
        :return: dict[str, Any] | None
        """
        uri = '/_get_model_show'
        payload = {
            'model': model,
        }
        return self.do_post(uri, payload)

    def _set_model_show(self, model: str, model_show: str) -> dict[str, Any] | None:
        """
        设置在线机型

        文档: https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E5%9C%A8%E7%BA%BF%E6%9C%BA%E5%9E%8B
        :param model: 机型名称
        :param model_show:
        :return: dict[str, Any] | None
        """
        uri = '/_set_model_show'
        payload = {
            'model': model,
            'model_show': model_show,
        }
        return self.do_post(uri, payload)

    def delete_unidirectional_friend(self, user_id: int) -> dict[str, Any] | None:
        """
        删除单向好友

        文档: https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E5%8D%95%E5%90%91%E5%A5%BD%E5%8F%8B
        :param user_id: 单向好友QQ号
        :return: dict[str, Any] | None
        """
        uri = '/delete_unidirectional_friend'
        payload = {
            'user_id': user_id,
        }
        return self.do_post(uri, payload)

    def send_private_forward_msg(self, user_id: int, messages: list[Any]) -> dict[str, Any] | None:
        """
        发送合并转发 ( 好友 )

        文档: https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91-%E5%A5%BD%E5%8F%8B
        :param user_id: 好友QQ号
        :param messages: 自定义转发消息, 具体看 https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
        :return: dict[str, Any] | None
        """
        uri = '/send_private_forward_msg'
        payload = {
            'user_id': user_id,
            'messages': messages,
        }
        return self.do_post(uri, payload)


__all__ = ['Action']