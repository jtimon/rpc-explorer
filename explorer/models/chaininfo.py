
from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Chaininfo(RpcCachedModel):
    bestblockhash = ormin.StringField()
    blocks = ormin.IntField()
    mediantime = ormin.IntField()
    cached_blocks = ormin.IntField()
    signblock_asm = ormin.StringField(required=False)
    signblock_hex = ormin.StringField(required=False)

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Chaininfo, cls)._rpccaller.RpcCall('getblockchaininfo', {})
        if 'error' in json_result:
            return json_result

        chaininfo = cls(json_dict=json_result)
        chaininfo.id = req_id
        chaininfo.start_caching_progress()
        chaininfo.save()
        return chaininfo

    def start_caching_progress(self):
        self.cached_blocks = -1
