from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from .config import ConfigModel

__version__ = "0.2.5"
__plugin_meta__ = PluginMetadata(
    "AutoReply",
    "这是一个一个一个自动回复插件啊啊啊",
    "根据配置自动回复，没了",
    ConfigModel,
)
