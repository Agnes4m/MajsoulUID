# flake8: noqa

data_api = "https://ak-data-1.sapk.ch/api"

baseurl = f"{data_api}/v2/pl4"
"""三麻"""
tribaseurl = f"{data_api}/v2/pl3"
"""四麻"""

player_id = f"{baseurl}/search_player"
"""牌谱屋角色id"""
playerid = f"{tribaseurl}/search_player"

_API = locals()
