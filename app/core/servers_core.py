from enum import Enum


class ServerID(Enum):
    MC_SURVIVAL = "mc-survival"
    MC_REDSTONE = "mc-redstone"
    MC_SWEET = "mc-sweet"
    MC_FORGEPACK = "mc-forgepack"

    FC_VANILLA = "fc-vanilla"
    FC_KRASTORIO2 = "fc-krastorio2"

VALID_SERVERS = tuple(s.value for s in ServerID)