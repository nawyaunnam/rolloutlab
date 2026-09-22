"""Deterministic, explainable rollout decisions with monotonic cohorts."""
import hashlib
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Flag:
    key: str
    version: int
    percentage: float = 0
    enabled: bool = True
    allow: frozenset = field(default_factory=frozenset)
    deny: frozenset = field(default_factory=frozenset)
    attributes: dict = field(default_factory=dict)
    salt: str = 'v1'
    def __post_init__(self):
        if not self.key or self.version < 1 or not 0 <= self.percentage <= 100:
            raise ValueError('key, positive version and percentage in [0,100] required')

def bucket(namespace, subject, salt='v1'):
    if not isinstance(subject, str) or not subject:
        raise ValueError('nonempty subject string required')
    # Length-prefix fields so delimiter-containing IDs cannot collide.
    value = ''.join(f'{len(x)}:{x}' for x in (namespace, subject, salt))
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:8], 'big') % 10000

def decide(flag, subject, attributes=None):
    position = bucket(flag.key, subject, flag.salt)
    attrs = attributes or {}
    if not flag.enabled: enabled, reason = False, 'kill-switch'
    elif subject in flag.deny: enabled, reason = False, 'explicit-deny'
    elif subject in flag.allow: enabled, reason = True, 'explicit-allow'
    elif any(attrs.get(k) != v for k, v in flag.attributes.items()):
        enabled, reason = False, 'attribute-mismatch'
    else: enabled, reason = position < flag.percentage * 100, 'percentage'
    return {'flag': flag.key, 'version': flag.version, 'enabled': enabled,
            'reason': reason, 'bucket': position}

def experiment(key, subject, weights, salt='v1'):
    if not weights or any(type(v) is not int or v < 0 for v in weights.values()) or sum(weights.values()) != 100:
        raise ValueError('nonnegative integer weights must total 100')
    position, cumulative = bucket(key, subject, salt), 0
    # Sorting makes assignment independent of dictionary insertion order.
    for variant, weight in sorted(weights.items()):
        cumulative += weight * 100
        if position < cumulative:
            return variant
    raise AssertionError('unreachable bucket')
