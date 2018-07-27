#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import argparse

parser = argparse.ArgumentParser(description='Test block api.')
parser.add_argument('--chain', help='specify the chain.')

args = parser.parse_args()

chain = args.chain
print('Running %s for chain %s' % (__file__, chain))

# ===----------------------------------------------------------------------===

from explorer.env_config import AVAILABLE_CHAINS, AVAILABLE_RPCS, DB_FACTORY
from explorer.process.generator.block import BlockGenerator
from explorer.process.generator.pegin import PeginGenerator
from explorer.process.generator.pegout import PegoutGenerator
from explorer.process.generator.transaction import TxGenerator
from explorer.process.greedy import GreedyCacher

block_gen_params = [chain, AVAILABLE_RPCS[chain]]
block_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['block_gen'])
block_generator = BlockGenerator(*block_gen_params)

tx_gen_params = [chain, AVAILABLE_RPCS[chain]]
tx_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['tx_gen'])
tx_generator = TxGenerator(*tx_gen_params)

greedy_cacher_params = [chain, AVAILABLE_RPCS[chain], DB_FACTORY.create()]
greedy_cacher_params.extend(AVAILABLE_CHAINS[chain]['proc']['greedy_cacher'])
greedy_cacher = GreedyCacher(*greedy_cacher_params, wait_time_greedy=0)

for i in xrange(101):
    block_generator._cron_loop()

greedy_cacher._cron_loop()
    
for i in xrange(5):
    for j in xrange(5):
        tx_generator._cron_loop()
    block_generator._cron_loop()

# Shouldn't cache anything else because greedy_cacher doesn't handle tip changes
greedy_cacher._cron_loop()
