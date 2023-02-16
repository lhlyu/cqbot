import os
import platform
import subprocess
import time
import yaml
import json
import websocket
from typing import Callable
from .event import *
from .action import *

CONFIG_FILE = "./config.yml"
LOG_FORMAT = "[%(asctime)s]-[%(levelname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Bot(Event):

    def __init__(self, loglevel: int = logging.INFO, path: str = './'):
        """
        初始化
        :param loglevel: 日志等级，默认 logging.INFO
        :param path: config.yml 和 go-cqhttp 所在目录，这两个东西必须放在一起
        """
        super().__init__()
        # 检查config.yml是否合法
        self.__check = False
        # http请求的地址
        self.__http_address = None
        # websocket需要连接的地址
        self.__ws_address = None
        self.__path = path
        self.__cfg = os.path.join(path, CONFIG_FILE)
        # 所有api
        self.__action = None
        # 所有事件
        self.__events = {}
        logging.basicConfig(level=loglevel, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    def run(self):
        """
        运行bot
        :return:
        """

        # 检查是否有config.yml文件
        if not os.path.exists(self.__cfg):
            raise FileExistsError('config.yml文件不存在')

        # 检查配置文件
        self.__check_config()

        if self.__check is False:
            raise Exception('config.yml配置错误，请仔细检查')

        # 运行go-cqhttp
        self.__run_go_cqhttp()

        # 初始化事件
        self.__init_events()

        # 初始化action, 所有的API操作都在这里
        self.__action = Action(self.__http_address)

        # 连接ws
        self.__run_ws()

    def __check_config(self):
        """
        检查配置文件
        :return:
        """
        with open(self.__cfg, "r") as f:
            yml = yaml.load(f.read(), Loader=yaml.Loader)
            servers = yml.get('servers', None)
            if servers is None:
                raise Exception('config.yml文件缺少属性servers')
            if not isinstance(servers, list):
                raise Exception('config.yml属性servers不是list类型')
            for server in servers:
                for k, v in server.items():
                    if k == 'http':
                        if not isinstance(v, dict):
                            raise Exception('config.yml属性servers.http.address不是dict类型')
                        self.__http_address = v.get('address', None)
                        if self.__http_address is None:
                            raise Exception('config.yml属性servers.http.address不能为空')

                        self.__http_address = f'http://{self.__http_address}'

                    if k == 'ws':
                        if not isinstance(v, dict):
                            raise Exception('config.yml属性servers.ws.address不是dict类型')
                        self.__ws_address = v.get('address', None)
                        if self.__ws_address is None:
                            raise Exception('config.yml属性servers.ws.address不能为空')

                        self.__ws_address = f'ws://{self.__ws_address}'

        self.__check = True

    def __run_go_cqhttp(self):
        """
        运行go_cqhttp
        :return:
        """
        plat = platform.system().lower()
        if plat == 'windows':
            subp = subprocess.Popen(f"cd {self.__path} && .\\go-cqhttp.exe -faststart", shell=True,
                                    stdout=subprocess.PIPE)
        else:
            subp = subprocess.Popen(f"cd {self.__path} && ./go-cqhttp -faststart", shell=True, stdout=subprocess.PIPE)

        while True:
            # 等待成功启动的信号
            shell_msg = subp.stdout.readline().decode("utf-8").strip()
            if shell_msg.strip() == "":
                continue

            print(shell_msg)
            if "CQ WebSocket 服务器已启动" in shell_msg:
                time.sleep(1)
                return

    def __run_ws(self):
        """
        运行websocket连接go-cqhttp
        :return:
        """

        def on_message(ws, msg):
            data = json.loads(msg)
            self.__call(data)

        def on_error(ws, error):
            logging.error(error)

        def on_close(ws):
            logging.info("websocket连接关闭")

        def on_open(ws):
            logging.info("websocket连接建立成功")

        ws = websocket.WebSocketApp(
            self.__ws_address,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
        )
        # 断开后5秒重连
        ws.run_forever(reconnect=5)

    def __init_events(self):
        """
        初始化事件
        :return:
        """
        self.__events: dict[PostType, dict[str, Callable[[Any], None]]] = {
            PostType.MESSAGE: {
                'on_message_private': self.on_message_private,
                'on_message_group': self.on_message_group
            },
            PostType.MESSAGE_SENT: {
                'on_message_private': self.on_message_private,
                'on_message_group': self.on_message_group
            },
            PostType.NOTICE: {
                'on_notice_friend_recall': self.on_notice_friend_recall,
                'on_notice_group_recall': self.on_notice_group_recall,
                'on_notice_group_increase': self.on_notice_group_increase,
                'on_notice_group_decrease': self.on_notice_group_decrease,
                'on_notice_group_admin': self.on_notice_group_admin,
                'on_notice_group_upload': self.on_notice_group_upload,
                'on_notice_group_ban': self.on_notice_group_ban,
                'on_notice_friend_add': self.on_notice_friend_add,
                'on_notice_notify_poke': self.on_notice_notify_poke,
                'on_notice_notify_lucky_king': self.on_notice_notify_lucky_king,
                'on_notice_notify_honor': self.on_notice_notify_honor,
                'on_notice_notify_title': self.on_notice_notify_title,
                'on_notice_group_card': self.on_notice_group_card,
                'on_notice_offline_file': self.on_notice_offline_file,
                'on_notice_client_status': self.on_notice_client_status,
                'on_notice_essence': self.on_notice_essence,
            },
            PostType.REQUEST: {
                'on_request_friend': self.on_request_friend,
                'on_request_group': self.on_request_group,
            },
            PostType.META_EVENT: {
                'on_meta_event_heartbeat': self.on_meta_event_heartbeat,
                'on_meta_event_lifecycle': self.on_meta_event_lifecycle,
            },
        }

    def __call(self, message_data: dict[str, Any]):
        """
        根据消息类型调用指定的方法
        :param message_data:
        :return:
        """
        pt = message_data.get('post_type', None)
        if pt is None:
            return

        post_type = PostType(pt)
        events = self.__events.get(post_type, None)

        if events is None:
            return

        if post_type == PostType.MESSAGE:
            msg = EventMessage(message_data)
            ev = f'on_{msg.post_type.value}_{msg.message_type.value}'
            fn = events.get(ev, None)
            if fn is None:
                return
            fn(self.__action, msg)

        elif post_type == PostType.MESSAGE_SENT:
            msg = EventMessage(message_data)
            ev = f'on_{msg.post_type.value}_{msg.message_type.value}'
            fn = events.get(ev, None)
            if fn is None:
                return
            fn(self.__action, msg)

        elif post_type == PostType.NOTICE:
            msg = EventNotice(message_data)
            ev = f'on_{msg.post_type.value}_{msg.notice_type.value}'
            if msg.notice_type == PostNoticeType.NOTIFY:
                ev += f'_{msg.sub_type}'
            fn = events.get(ev, None)
            if fn is None:
                return
            fn(self.__action, msg)

        elif post_type == PostType.REQUEST:
            msg = EventRequest(message_data)
            ev = f'on_{msg.post_type.value}_{msg.request_type.value}'
            fn = events.get(ev, None)
            if fn is None:
                return
            fn(self.__action, msg)

        elif post_type == PostType.META_EVENT:
            msg = EventMetaEvent(message_data)
            ev = f'on_{msg.post_type.value}_{msg.meta_event_type.value}'
            fn = events.get(ev, None)
            if fn is None:
                return
            fn(self.__action, msg)
