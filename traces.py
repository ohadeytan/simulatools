from enum import Enum

small_caches =  [ x*250 for x in range(1,1+8) ]    # [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
medium_caches = [ 2**x for x in range(12,12+8) ]   # [4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288]
large_caches =  [ x*10**5 for x in range (1,1+8) ] # [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]

class Trace(Enum):

    OLTP =           { 'file' : 'OLTP.lis', 'format' : 'arc', 'typical_caches' : small_caches,  'extra_url' : 'lk7zrCADHQ/Papers/ARCTraces/' }
    DS1 =            { 'file' : 'DS1.lis',  'format' : 'arc', 'typical_caches' : large_caches,  'extra_url' : 'z9qaItlfnw/Papers/ARCTraces/' }
    S1 =             { 'file' : 'S1.lis',   'format' : 'arc', 'typical_caches' : large_caches,  'extra_url' : 'fcv_QZPUZ9/Papers/ARCTraces/' }
    S2 =             { 'file' : 'S2.lis',   'format' : 'arc', 'typical_caches' : large_caches,  'extra_url' : '4U2T9rsZjg/Papers/ARCTraces/' }
    S3 =             { 'file' : 'S3.lis',   'format' : 'arc', 'typical_caches' : large_caches,  'extra_url' : 'YGfSt_Tjmm/Papers/ARCTraces/' }
    P1 =             { 'file' : 'P1.lis',   'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'NRXtHDuFrN/Papers/ARCTraces/' }
    P4 =             { 'file' : 'P4.lis',   'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'H81xdI4cVS/Papers/ARCTraces/' }
    P5 =             { 'file' : 'P5.lis',   'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'BujyVu9ih_/Papers/ARCTraces/' }
    P8 =             { 'file' : 'P8.lis',   'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'zm7Lj6-7z1/Papers/ARCTraces/' }
    P11 =            { 'file' : 'P11.lis',  'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'AoaN_mB-cE/Papers/ARCTraces/' }
    P12 =            { 'file' : 'P12.lis',  'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'SwFarb1sCi/Papers/ARCTraces/' }
    P14 =            { 'file' : 'P14.lis',  'format' : 'arc', 'typical_caches' : medium_caches, 'extra_url' : 'nnSndcrtds/Papers/ARCTraces/' }

    pools =          { 'file' : '2_pools.trace.gz', 'format' : 'lirs', 'typical_caches' : small_caches}
    cpp =            { 'file' : 'cpp.trace.gz',     'format' : 'lirs', 'typical_caches' : small_caches}
    cs =             { 'file' : 'cs.trace.gz',      'format' : 'lirs', 'typical_caches' : small_caches}
    gli =            { 'file' : 'gli.trace.gz',     'format' : 'lirs', 'typical_caches' : small_caches}
    loop =           { 'file' : 'loop.trace.gz',    'format' : 'lirs', 'typical_caches' : small_caches}
    multi1 =         { 'file' : 'multi1.trace.gz',  'format' : 'lirs', 'typical_caches' : small_caches}
    multi2 =         { 'file' : 'multi2.trace.gz',  'format' : 'lirs', 'typical_caches' : small_caches}
    multi3 =         { 'file' : 'multi3.trace.gz',  'format' : 'lirs', 'typical_caches' : small_caches}
    sprite =         { 'file' : 'sprite.trace.gz',  'format' : 'lirs', 'typical_caches' : small_caches}

    w2 =             { 'file' : 'WebSearch2.spc', 'format' : 'umass-storage', 'typical_caches' : large_caches}
    w3 =             { 'file' : 'WebSearch3.spc', 'format' : 'umass-storage', 'typical_caches' : large_caches}

    wiki1190153705 = { 'file' : 'wiki.1190153705.gz', 'format' : 'wikipedia', 'typical_caches' : small_caches}
    wiki1190207720 = { 'file' : 'wiki.1190207720.gz', 'format' : 'wikipedia', 'typical_caches' : small_caches}
    wiki1190222124 = { 'file' : 'wiki.1190222124.gz', 'format' : 'wikipedia', 'typical_caches' : small_caches}
    wiki1190322952 = { 'file' : 'wiki.1190322952.gz', 'format' : 'wikipedia', 'typical_caches' : small_caches}

    SCARAB_RECS_EX = { 'file' : 'recs.trace.20160808T073231Z.xz', 'format' : 'scarab', 'typical_caches' : medium_caches, 'extra_url' : 'http://download.scarabresearch.com/cache-traces/' }

    def file(self):
        return self.value['file']

    def format(self):
        return self.value['format']

    def typical_caches(self):
        return self.value['typical_caches']

    def url(self):
        return self.url_base() + self.value.get('extra_url', '') + self.value['file']

    def url_base(self):
        f = self.format()
        if f == 'arc':
            return 'https://www.dropbox.com/sh/9ii9sc7spcgzrth/'
        elif f == 'lirs':
            return 'https://github.com/ben-manes/caffeine/raw/master/simulator/src/main/resources/com/github/benmanes/caffeine' \
                   '/cache/simulator/parser/lirs/'
        elif f == 'umass-storage':
            return 'http://skuld.cs.umass.edu/traces/storage/'
        elif f == 'wikipedia':
            return 'http://www.wikibench.eu/wiki/2007-09/'
        else:
            return ''
