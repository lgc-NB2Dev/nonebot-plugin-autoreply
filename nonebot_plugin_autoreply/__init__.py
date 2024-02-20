from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from .config import ConfigModel, reload_replies as reload_replies

__version__ = "0.2.12"
__plugin_meta__ = PluginMetadata(
    name="AutoReply",
    description="配置文件高度可自定义的自动回复插件",
    usage="这是一个一个一个自动回复插件啊啊啊",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-autoreply",
    type="application",
    config=ConfigModel,
    supported_adapters={"~onebot.v11"},
    extra={"License": "MIT", "Author": "student_2333"},
)
