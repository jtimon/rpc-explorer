# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import requests
import json
import time

file = open('/build_docker/docker/conf/RPC_ALLOWED_CALLS.json', 'r').read()
RPC_ALLOWED_CALLS = json.loads(file)['allowed_rpc']
# print('RPC_ALLOWED_CALLS', len(RPC_ALLOWED_CALLS), RPC_ALLOWED_CALLS)

class RpcCaller(object):

    def __init__(self, address, user, password,
                 **kwargs):

        if not address:
            raise Exception('RpcCaller.__init__: No address provided')
        self.address = address
        if not user:
            raise Exception('RpcCaller.__init__: No user provided')
        self.user = user
        if not password:
            raise Exception('RpcCaller.__init__: No password provided')
        self.password = password

        super(RpcCaller, self).__init__(**kwargs)

    def RpcCall(self, method, params):
        if not method in RPC_ALLOWED_CALLS:
            return {'error': {'message': 'Daemon RPC method "%s" not supported.' % method}}

        requestData = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': self.address + '_' + method,
        }
        rpcAuth = (self.user, self.password)
        rpcHeaders = {'content-type': 'application/json'}
        response = None
        counter = 0
        while response == None:
            json_result = False
            try:
                response = requests.request('post', 'http://' + self.address,
                                            data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
                # response.raise_for_status()
                json_result = response.json()
            except Exception as e:
                print("Error in RpcCaller.RpcCall:", type(e), e)
                if counter == 5:
                    return {'error': {'message': 'Rpc connection error for method %s' % method}}
                time.sleep(2)
                counter = counter + 1
                continue

        if not json_result:
            return {'error': {'message': 'No rpc result for method %s' % method}}
        # If there's errors, only return the errors
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}

        if ('result' in json_result):
            json_result = json_result['result']

        return json_result
