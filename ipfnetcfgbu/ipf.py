from aioipfabric import IPFabricClient as _IPFabricClient
from aioipfabric.mixin_configs import IPFConfigsMixin

__all__ = ["IPFabricClient"]


class IPFabricClient(_IPFabricClient, IPFConfigsMixin):
    pass
