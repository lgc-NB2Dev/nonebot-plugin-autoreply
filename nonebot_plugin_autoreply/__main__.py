import asyncio
import random
import re
from itertools import starmap
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from typing_extensions import TypeVarTuple, Unpack

from nonebot import on_command, on_message, on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .config import (
    FilterModel,
    MatchModel,
    MatchType,
    MessageSegmentModel,
    ReplyModel,
    ReplyType,
    config,
    reload_replies,
    replies,
)
from .util import VarDictType, get_var_dict, replace_message_var

T = TypeVar("T")
TArgs = TypeVarTuple("TArgs")


# 感谢 nb2 群内 Bryan不可思议 佬的帮助！！
def check_list(
    function: Callable[
        [Unpack[TArgs]],
        Union[
            bool,
            Tuple[bool, Optional[Dict[str, Any]]],
        ],
    ],
    will_check: Iterable[Tuple[Unpack[TArgs]]],
    is_any: bool = False,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    var_dict_total = {}

    for val in starmap(function, will_check):
        if not isinstance(val, tuple):
            val = val, None

        ok, var_d = val

        # any，任意一个为 True 就返回 True
        if is_any and ok:
            return val

        if not is_any:
            # all，有一个不为 True 就返回 False
            if not ok:
                return False, None

            # 合并 var_dict
            if var_d:
                var_dict_total.update(var_d)

    # any，循环结束代表所有都是 False，返回 False
    if is_any:
        return False, None

    # all，循环结束代表所有都是 True，返回 True
    return True, var_dict_total


def check_filter(will_check: FilterModel[T], val: Optional[T]) -> bool:
    ok = val not in will_check.values  # 判断黑名单 值不在列表中 ok
    return (not ok) if will_check.type == "white" else ok  # 白名单则反过来


def check_message(
    match: MatchModel,
    event: MessageEvent,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    if match.type == "poke":
        return False, None

    if match.match is None:
        raise ValueError("存在 type 不为 poke，且 match 为空的不合法匹配规则")

    if match.to_me and (not event.is_tome()):
        return False, None

    msg_str = str(event.message)
    msg_plaintext = event.message.extract_plain_text()
    match_template = match.match

    if match.strip:
        msg_str = msg_str.strip()
        msg_plaintext = msg_plaintext.strip()

    if match.type == "regex":
        plaintext = False
        flag = re.IGNORECASE if match.ignore_case else 0
        match_obj = re.search(match_template, msg_str, flag)
        if (not match_obj) and match.allow_plaintext:
            plaintext = True
            match_obj = re.search(match_template, msg_plaintext, flag)

        if match_obj:
            var_dict = {}
            var_dict["v0"] = (
                match_obj.string if plaintext else Message(match_obj.string)
            )
            var_dict.update(
                {
                    f"v{i + 1}": (str(x) if plaintext else Message(x) if x else "")
                    for i, x in enumerate(match_obj.groups())
                },
            )
            var_dict.update(
                {
                    k: (str(v) if plaintext else Message(v) if v else "")
                    for k, v in match_obj.groupdict().items()
                },
            )
            return True, var_dict

        return False, None

    if match.ignore_case:
        # regex 匹配已经处理过了，这边不需要管
        msg_str = msg_str.lower()
        match_template = match_template.lower()

    if match.type == "full":
        return (
            (
                (msg_str == match_template)
                or (msg_plaintext == match_template if match.allow_plaintext else False)
            ),
            None,
        )

    if match.type == "start":
        return (
            (
                msg_str.startswith(match_template)
                or (
                    msg_plaintext.startswith(match_template)
                    if match.allow_plaintext
                    else False
                )
            ),
            None,
        )

    if match.type == "end":
        return (
            (
                msg_str.endswith(match_template)
                or (
                    msg_plaintext.endswith(match_template)
                    if match.allow_plaintext
                    else False
                )
            ),
            None,
        )

    # default fuzzy
    if (not msg_str) or (match.allow_plaintext and (not msg_plaintext)):
        return False, None
    return (
        (
            (match_template in msg_str)
            or ((match_template in msg_plaintext) if match.allow_plaintext else False)
        ),
        None,
    )


def check_poke(match: MatchModel, event: PokeNotifyEvent) -> bool:
    if match.type != "poke":
        return False
    return event.is_tome() if match.to_me else True


def check_match(
    match: MatchType,
    event: Union[MessageEvent, PokeNotifyEvent],
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    if isinstance(match, str):
        match = MatchModel(match=match)

    if match.possibility < 1 and random.random() > match.possibility:
        return False, None

    return (
        check_message(match, event)
        if isinstance(event, MessageEvent)
        else (check_poke(match, event), None)
    )


async def message_checker(
    event: Union[MessageEvent, PokeNotifyEvent],
    state: T_State,
) -> bool:
    group = (
        event.group_id
        if isinstance(event, (GroupMessageEvent, PokeNotifyEvent))
        else None
    )

    state_reply: List[Tuple[ReplyType, Optional[Dict[str, Any]]]] = []
    for reply in replies:
        filter_checks = [(reply.groups, group), (reply.users, event.user_id)]
        match_checks = [(x, event) for x in reply.matches]

        if not (
            check_list(check_filter, filter_checks)[0]
            and (match_result := check_list(check_match, match_checks, is_any=True))[0]
        ):
            continue

        state_reply.append((random.choice(reply.replies), match_result[1]))
        if reply.block:
            break

    state["reply"] = state_reply
    return bool(state_reply)


ReplyMessagesType = Tuple[List[Message], Optional[Tuple[int, int]]]


async def get_reply_msgs(
    reply: ReplyType,
    var_dict: VarDictType,
    refuse_multi: bool = False,
) -> ReplyMessagesType:
    if isinstance(reply, str):
        is_plain = reply.startswith("@")
        if is_plain:
            reply = reply[1:]

        reply = ReplyModel(type="plain" if is_plain else "normal", message=reply)

    elif isinstance(reply, list):
        reply = ReplyModel(type="array", message=reply)

    rt = reply.type
    msg = reply.message

    if rt == "plain":
        msg = cast(str, msg)
        return [Message() + msg], None

    if rt == "array":
        msg = cast(List[MessageSegmentModel], msg)
        msg = Message(MessageSegment(type=x.type, data=x.data) for x in msg)
        msg = await replace_message_var(msg, var_dict)
        return [msg], None

    if rt == "multi":
        if refuse_multi:
            raise ValueError("Nested `multi` is not allowed")

        delay = reply.delay
        if isinstance(delay, int):
            delay = (delay, delay)

        msg = cast(List[ReplyModel], msg)
        msgs = [
            (await get_reply_msgs(x, var_dict, refuse_multi=True))[0][0] for x in msg
        ]
        if reply.shuffle:
            random.shuffle(msgs)

        return msgs, delay

    # default normal
    msg = cast(str, msg)
    return [await replace_message_var(Message(msg), var_dict)], None


message_matcher = on_message(
    rule=message_checker,
    block=config.autoreply_block,
    priority=config.autoreply_priority,
)

poke_matcher = on_notice(
    rule=message_checker,
    block=config.autoreply_block,
    priority=config.autoreply_priority,
)


@message_matcher.handle()
@poke_matcher.handle()
async def _(
    bot: Bot,
    event: Union[MessageEvent, PokeNotifyEvent],
    matcher: Matcher,
    state: T_State,
):
    reply: List[Tuple[ReplyType, Optional[Dict[str, Any]]]] = state["reply"]

    var_dict = await get_var_dict(bot, event)
    reply_msgs: List[ReplyMessagesType] = await asyncio.gather(
        *(
            get_reply_msgs(
                x[0],
                (
                    {**var_dict[0], **(var if (var := x[1]) else {})},
                    var_dict[1],
                ),
            )
            for x in reply
        ),
    )

    for msgs, delay_tuple in reply_msgs:
        for x in msgs:
            await matcher.send(x)

        if delay_tuple:
            d_min, d_max = delay_tuple
            delay = d_min if d_min == d_max else random.randint(d_min, d_max)
            delay /= 1000
            await asyncio.sleep(delay)


reload_matcher = on_command("重载自动回复", permission=SUPERUSER)


@reload_matcher.handle()
async def _(matcher: Matcher):
    success, fail = reload_replies()
    await matcher.finish(f"重载回复配置完毕~\n成功 {success} 个，失败 {fail} 个")
