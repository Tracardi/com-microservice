from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    board_url: str
    list_name1: str
    list_id1: str = None
    list_name2: str
    list_id2: str = None
    card_name: str
