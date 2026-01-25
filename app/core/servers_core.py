from enum import Enum


class ServerID(Enum):
    MC_SURVIVAL = "mc-survival"
    MC_REDSTONE = "mc-redstone"
    MC_SWEET = "mc-sweet"


    FC_VANILLA = "fc-vanilla"
    FC_KRASTORIO2 = "fc-krastorio2"

VALID_SERVERS = tuple(ServerID)