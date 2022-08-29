from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    board_url: str
    list_name: str
    list_id: str = None
    card_name: str
    member_id: str

