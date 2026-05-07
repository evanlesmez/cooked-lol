from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptiveForceShard:
    adaptive_force: int = 9


ADAPTIVE_FORCE_SHARD = AdaptiveForceShard()

# Adaptive Force conversion when the champion's profile resolves to AP.
AP_PER_ADAPTIVE_FORCE = 1.0


def ap_from_shards(shard: AdaptiveForceShard, count: int) -> float:
    """AP granted by `count` Adaptive Force shards (AP form selected)."""
    return shard.adaptive_force * AP_PER_ADAPTIVE_FORCE * count
