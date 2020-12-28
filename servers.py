register_channels = {
    768934271620087858: 768934271620087861,
    761946620693970995: 1,
}


def get_register_channel_id(guild_id):
    return register_channels[guild_id]
