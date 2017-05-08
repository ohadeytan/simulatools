from enum import Enum

class Policy(Enum):
    opt =   'opt.Clairvoyant'
    lru =   'linked.Lru'
    lfu =   'linked.Lfu'
    wtlfu = 'sketch.WindowTinyLfu'
