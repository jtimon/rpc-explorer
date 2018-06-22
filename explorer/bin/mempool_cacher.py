#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"bitcoin",
                     u"Chain to subscribe to for caching mempool stats")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from explorer import process

from explorer.env_config import AVAILABLE_CHAINS

chain = FLAGS.chain

mempool_cacher_params = [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create()]
mempool_cacher_params.extend(AVAILABLE_CHAINS[chain]['proc']['mempool_cacher'])
mempool_cacher = process.mempoolstats.MempoolStatsCacher(*mempool_cacher_params)
mempool_cacher.start()

if 'mempool_saver' in AVAILABLE_CHAINS[chain]:
    mempool_saver_params = [chain, AVAILABLE_CHAINS[chain]['rpc']]
    mempool_saver_params.extend(AVAILABLE_CHAINS[chain]['proc']['mempool_saver'])
    mempool_saver = process.mempoolsaver.MempoolSaver(*mempool_saver_params)
    mempool_saver.start()
