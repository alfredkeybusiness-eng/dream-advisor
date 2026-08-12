from rlm import McpIntegration


class Avina(McpIntegration):
    server = "avina"  # matches the mcpServers key / auth.json `mcp:avina`
    url = "https://api.avina.io/mcp"


avina = Avina()

# Forward bare module access (`import avina; await avina.<tool>(...)`) to the
# instance, but NOT the names the kernel bootstrap probes -- forwarding `run`
# would make it treat the module as a callable skill and break tool dispatch.
_RESERVED = {"run", "__wrapped__", "__call__"}


def __getattr__(name):
    if name.startswith("_") or name in _RESERVED:
        raise AttributeError(name)
    return getattr(avina, name)
