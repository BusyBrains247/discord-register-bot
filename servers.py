register_channels = {
    768934271620087858: 768934271620087861,
    761946620693970995: 793425449300656158,
}
data_channels = {
    768934271620087858: 1,
    761946620693970995: 793495327470256140,
}


def get_register_channel_id(guild_id):
    return register_channels[guild_id]


def get_data_channel_id(guild_id):
    return data_channels[guild_id]
