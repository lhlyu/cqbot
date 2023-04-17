import re
from typing import Callable, List, Any
from .action import Action
from .event import EventMessage
from .cq import CQ

# def handler(act: Action, msg: EventMessage, args: List[Any]) -> bool
CmdHandler = Callable[[Action, EventMessage, List[Any]], bool] | None


class Cmd:
    __cmds: dict[str, CmdHandler]
    __helps: dict[str, str]
    __commanders: dict[str, List[int]]

    def __init__(self, admins: List[int] = None):
        """
        初始化
        :param admins: 指定只有管理员才能使用所有的指令
        """
        self.__cmds = {}
        self.__helps = {}
        self.__commanders = {}
        self.admins = admins
        pass

    def add(self, cmd: str, help: str, handler: CmdHandler = None, commander: List[int] | None = None):
        """
        添加指令和处理方法
        :param cmd: 指令名字
        :param help: 指令说明文案
        :param handler: 处理方法，可以先空着不实现
        :param commander: 指定某个qq才能使用这个指令, 不指定则所有人可使用
        :return:
        """
        self.__cmds[cmd] = handler
        self.__helps[cmd] = help
        if commander is not None:
            self.__commanders[cmd] = commander
        pass

    def help(self) -> str:
        """
        返回所有指令的使用方法
        :return:
        """
        if len(self.__helps) == 0:
            return ''
        items = ['指令说明: ']
        for key in self.__helps:
            items.append(f'{key} - {self.__helps[key]}')
        return '\n'.join(items)

    def run(self, act: Action, msg: EventMessage) -> bool:
        """
        执行指令
        :param msg:
        :return:
        """
        # 机器人的消息过滤
        if msg.self_id == msg.user_id:
            return False
        if self.admins is not None and msg.user_id not in self.admins:
            return False
        # 将CQ码替换成空
        prompt = CQ.replace(msg.message, ' ').strip()
        # 根据空格切割参数
        args = re.split(r'\s+', prompt)
        if len(args) == 0:
            return False
        handler = self.__cmds.get(args[0], None)
        if handler is None:
            return False
        commander = self.__commanders.get(args[0], None)
        if commander is not None and msg.user_id not in commander:
            return False
        return handler(act, msg, args[1:])


__all__ = ['Cmd', 'CmdHandler']