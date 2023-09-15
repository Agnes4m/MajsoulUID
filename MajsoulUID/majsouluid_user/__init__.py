from typing import List

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from ..utils.api import get_sqla
from ..utils.mj_prefix import PREFIX
from ..utils.message import send_diff_msg
from .draw_user_card import get_user_card

sv_user_config = SV("mj用户管理", pm=2)
sv_user_add = SV("mj用户添加")
sv_user_info = SV("mj用户信息")
# sv_user_help = SV('mj绑定帮助')


@sv_user_info.on_fullmatch(f"{PREFIX}绑定信息")
async def send_bind_card(bot: Bot, ev: Event):
    await bot.logger.info("mj开始执行[查询用户绑定状态]")
    uid_list = await get_user_card(ev.bot_id, ev.user_id)
    if not uid_list:
        return await bot.send("你还没有绑定MJ_UID哦!")
    await bot.logger.info("mj[查询用户绑定状态]完成!等待图片发送中...")
    await bot.send(uid_list)
    return None


@sv_user_info.on_command(
    (f"{PREFIX}绑定uid", f"{PREFIX}切换uid", f"{PREFIX}删除uid", f"{PREFIX}解绑uid")
)
async def send_link_uid_msg(bot: Bot, ev: Event):
    await bot.logger.info("mj开始执行[绑定/解绑用户信息]")
    qid = ev.user_id
    await bot.logger.info(f"mj[绑定/解绑]UserID: {qid}")

    sqla = get_sqla(ev.bot_id)
    mj_uid = ev.text.strip()
    if mj_uid and not mj_uid.isdigit():
        return await bot.send("你输入了错误的格式!")

    if "绑定" in ev.command:
        data = await sqla.insert_bind_data(qid, mj_uid=mj_uid)
        return await send_diff_msg(
            bot,
            data,
            {
                0: f"绑定MJ_UID{mj_uid}成功!",
                -1: f"MJ_UID{mj_uid}的位数不正确!",
                -2: f"MJ_UID{mj_uid}已经绑定过了!",
                -3: "你输入了错误的格式!",
            },
        )
    if "切换" in ev.command:
        data = await sqla.switch_uid(qid, uid=mj_uid)
        if isinstance(data, List):
            return await bot.send(f"切换MJ_UID{mj_uid}成功!")
        return await bot.send(f"尚未绑定该MJ_UID{mj_uid}")
    data = await sqla.delete_bind_data(qid, mj_uid=mj_uid)
    return await send_diff_msg(
        bot,
        data,
        {
            0: f"删除MJ_UID{mj_uid}成功!",
            -1: f"该MJ_UID{mj_uid}不在已绑定列表中!",
        },
    )
