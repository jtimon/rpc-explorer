#!/usr/bin/env python

# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"elementsregtest",
                     u"Chain to for which to generate txs and/or Blocks")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from explorer import env_config
from explorer.process.generator.block import BlockGenerator
from explorer.process.generator.pegin import PeginGenerator
from explorer.process.generator.pegout import PegoutGenerator
from explorer.process.generator.transaction import TxGenerator

chain = FLAGS.chain

if 'block_gen' in env_config.AVAILABLE_CHAINS[chain]['proc']:
    block_gen_params = [chain, env_config.rpccaller_for_chain(chain)]
    block_gen_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['block_gen'])
    block_generator = BlockGenerator(*block_gen_params)
    block_generator.start()

if 'tx_gen' in env_config.AVAILABLE_CHAINS[chain]['proc']:
    tx_gen_params = [chain, env_config.rpccaller_for_chain(chain)]
    tx_gen_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['tx_gen'])
    tx_generator = TxGenerator(*tx_gen_params)
    tx_generator.start()

if 'pegin_gen' in env_config.AVAILABLE_CHAINS[chain]['proc'] and 'parent_chain' in env_config.AVAILABLE_CHAINS[chain]['properties']:
    parent_chain_rpccaller = env_config.rpccaller_for_chain(env_config.AVAILABLE_CHAINS[chain]['properties']['parent_chain'])
    pegin_gen_params = [chain, env_config.rpccaller_for_chain(chain), parent_chain_rpccaller]
    pegin_gen_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['pegin_gen'])
    pegin_generator = PeginGenerator(*pegin_gen_params)
    pegin_generator.start()

if 'pegout_gen' in env_config.AVAILABLE_CHAINS[chain]['proc'] and 'parent_chain' in env_config.AVAILABLE_CHAINS[chain]['properties']:
    parent_chain_rpccaller = env_config.rpccaller_for_chain(env_config.AVAILABLE_CHAINS[chain]['properties']['parent_chain'])
    parent_chain_has_CT = env_config.AVAILABLE_CHAINS[chain]['properties']['parent_chain_has_CT']
    pegout_gen_params = [chain, env_config.rpccaller_for_chain(chain), parent_chain_rpccaller, parent_chain_has_CT]
    pegout_gen_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['pegout_gen'])
    pegout_generator = PegoutGenerator(*pegout_gen_params)
    pegout_generator.start()
