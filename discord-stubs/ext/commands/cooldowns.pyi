from typing import Optional, Tuple, Type, TypeVar, Union

from discord.enums import Enum

from ...message import Message

_CM = TypeVar('_CM', bound=CooldownMapping)
_MC = TypeVar('_MC', bound=MaxConcurrency)

class BucketType(Enum):
    default: int
    user: int
    guild: int
    channel: int
    member: int
    category: int
    role: int
    def get_key(
        self, msg: Message
    ) -> Optional[Union[int, Tuple[Optional[int], int]]]: ...

class Cooldown:
    rate: int
    per: float
    type: BucketType
    def __init__(self, rate: int, per: float, type: BucketType) -> None: ...
    def get_tokens(self, current: Optional[int] = ...) -> int: ...
    def get_retry_after(self, current: Optional[float] = ...) -> float: ...
    def update_rate_limit(self, current: Optional[float] = ...) -> Optional[float]: ...
    def reset(self) -> None: ...
    def copy(self) -> Cooldown: ...

class CooldownMapping:
    def __init__(self, original: Cooldown) -> None: ...
    def copy(self) -> CooldownMapping: ...
    @property
    def valid(self) -> bool: ...
    @classmethod
    def from_cooldown(
        cls: Type[_CM], rate: int, per: float, type: BucketType
    ) -> _CM: ...
    def get_bucket(
        self, message: Message, current: Optional[float] = ...
    ) -> Cooldown: ...
    def update_rate_limit(
        self, message: Message, current: Optional[float] = ...
    ) -> Optional[float]: ...

class MaxConcurrency:
    number: int
    per: BucketType
    wait: bool
    def __init__(self, number: int, *, per: BucketType, wait: bool) -> None: ...
    def copy(self: _MC) -> _MC: ...
    def get_key(self, message: Message) -> Union[str, int]: ...
    async def acquire(self, message: Message) -> None: ...
    async def release(self, message: Message) -> None: ...
