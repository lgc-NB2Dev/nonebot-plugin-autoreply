import random
import re
from typing import Iterable, Optional, Tuple, TypeVar

from nonebot import on_message
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.matcher import Matcher

from .config import ReplyEntry, replies

T = TypeVar("T")

matcher = on_message(priority=99)


def check_filter(filter: ReplyEntry.Filter[T], val: T) -> bool:
    ok = val in filter.values
    if filter.type == "black":
        ok = not ok
    return ok


def check_filter_list(filters: Iterable[Tuple[ReplyEntry.Filter[T], T]]) -> bool:
    for f, v in filters:
        if not check_filter(f, v):
            return False
    return True


# 大屎山，勿喷
# 心情烦躁的时候写出来的
def get_reply(event: MessageEvent) -> Optional[Message]:
    group = event.group_id if isinstance(event, GroupMessageEvent) else None

    for rep in replies:
        filters = [(rep.groups, group), (rep.users, event.user_id)]
        if not check_filter_list(filters):
            continue

        for mat in rep.matches:
            if mat.to_me and (not event.is_tome()):
                continue

            msg = str(event.message)
            msg_plaintext = event.message.extract_plain_text()
            match = mat.match

            if mat.strip:
                msg = msg.strip()
                msg_plaintext = msg_plaintext.strip()

            if mat.ignore_case:
                if not mat.type == "regex":
                    msg = msg.lower()
                    match = match.lower()

            if mat.type == "full":
                matched = (msg == match) or (
                    msg_plaintext == match if mat.allow_plaintext else False
                )
            elif mat.type == "regex":
                flag = re.I if mat.ignore_case else 0
                matched = bool(
                    (re.search(match, msg, flag))
                    or (
                        re.search(match, msg_plaintext, flag)
                        if mat.allow_plaintext
                        else False
                    )
                )
            else:  # default fuzzy
                if (not msg) or (mat.allow_plaintext and (not msg_plaintext)):
                    continue
                matched = (match in msg) or (
                    (match in msg_plaintext) if mat.allow_plaintext else False
                )

            if matched:
                reply = random.choice(rep.replies)
                if isinstance(reply, list):
                    reply = [MessageSegment(x["type"], x["data"]) for x in reply]
                return Message(reply)


@matcher.handle()
async def _(matcher: Matcher, event: MessageEvent):
    if reply := get_reply(event):
        await matcher.finish(reply)
