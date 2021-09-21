from dataclasses import dataclass


@dataclass(frozen=True)
class MixerConfig:
    deposit_poll_interval: float
    house_poll_interval: float
    minimum_pending_settlements: int
