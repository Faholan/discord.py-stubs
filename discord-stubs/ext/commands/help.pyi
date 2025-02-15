from inspect import Parameter
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    TypeVar,
    Union,
    type_check_only,
)
from typing_extensions import Protocol, TypedDict

import discord

from .cog import Cog
from .context import Context
from .cooldowns import Cooldown
from .core import Command, Group, _CheckPredicate
from .errors import CommandError

_T = TypeVar('_T')
_MaybeAwaitable = Union[Awaitable[_T], _T]
_CT = TypeVar('_CT', bound=Context)
_HC = TypeVar('_HC', bound=HelpCommand[Any])

@type_check_only
class _CommandAttrs(TypedDict, total=False):
    name: str
    enabled: bool
    help: Optional[str]
    brief: Optional[str]
    usage: Optional[str]
    aliases: List[str]
    description: str
    hidden: bool
    rest_is_raw: bool
    ignore_extra: bool
    cooldown: Cooldown
    parent: Command[Context]
    checks: List[_CheckPredicate[Any]]

@type_check_only
class _PaginatorProtocol(Protocol):
    prefix: Optional[str]
    suffix: Optional[str]
    max_size: int
    linesep: str
    def clear(self) -> None: ...
    def add_line(self, line: str = ..., *, empty: bool = ...) -> None: ...
    def close_page(self) -> None: ...
    def __len__(self) -> int: ...
    @property
    def pages(self) -> List[str]: ...

class Paginator:
    prefix: Optional[str]
    suffix: Optional[str]
    max_size: int
    linesep: str
    def __init__(
        self,
        prefix: Optional[str] = ...,
        suffix: Optional[str] = ...,
        max_size: int = ...,
        linesep: str = ...,
    ) -> None: ...
    def clear(self) -> None: ...
    def add_line(self, line: str = ..., *, empty: bool = ...) -> None: ...
    def close_page(self) -> None: ...
    def __len__(self) -> int: ...
    @property
    def pages(self) -> List[str]: ...

class _HelpCommandImpl(Command[_CT]):
    async def prepare(self, ctx: _CT) -> None: ...
    @property
    def clean_params(self) -> Mapping[str, Parameter]: ...

class HelpCommand(Generic[_CT]):
    context: Optional[_CT]
    show_hidden: bool
    verify_checks: Optional[bool]
    command_attrs: _CommandAttrs
    cog: Optional[Cog[_CT]]

    MENTION_TRANSFORMS: ClassVar[Dict[str, str]]
    MENTION_PATTERN: ClassVar[Pattern[str]]
    def __init__(
        self,
        *,
        show_hidden: bool = ...,
        verify_checks: Optional[bool] = ...,
        command_attrs: _CommandAttrs = ...,
    ) -> None: ...
    def copy(self: _HC) -> _HC: ...
    def add_check(self, func: _CheckPredicate[_CT]) -> None: ...
    def remove_check(self, func: _CheckPredicate[_CT]) -> None: ...
    def get_bot_mapping(self) -> Dict[Optional[Cog[_CT]], List[Command[_CT]]]: ...
    @property
    def clean_prefix(self) -> str: ...
    @property
    def invoked_with(self) -> str: ...
    def get_command_signature(self, command: Command[_CT]) -> str: ...
    def remove_mentions(self, string: str) -> str: ...
    def command_not_found(self, string: str) -> _MaybeAwaitable[str]: ...
    def subcommand_not_found(
        self, command: Command[_CT], string: str
    ) -> _MaybeAwaitable[str]: ...
    async def filter_commands(
        self,
        commands: Iterable[Command[_CT]],
        *,
        sort: bool = ...,
        key: Optional[Callable[[Command[_CT]], Any]] = ...,
    ) -> List[Command[_CT]]: ...
    def get_max_size(self, commands: Sequence[Command[_CT]]) -> int: ...
    def get_destination(
        self,
    ) -> Union[discord.TextChannel, discord.DMChannel, discord.GroupChannel]: ...
    async def send_error_message(self, error: str) -> None: ...
    async def on_help_command_error(self, ctx: _CT, error: CommandError) -> None: ...
    async def send_bot_help(
        self, mapping: Mapping[Optional[Cog[_CT]], List[Command[_CT]]]
    ) -> Any: ...
    async def send_cog_help(self, cog: Cog[_CT]) -> Any: ...
    async def send_group_help(self, group: Group[_CT]) -> Any: ...
    async def send_command_help(self, command: Command[_CT]) -> Any: ...
    async def prepare_help_command(
        self, ctx: _CT, command: Optional[str] = ...
    ) -> None: ...
    async def command_callback(
        self, ctx: _CT, *, command: Optional[str] = ...
    ) -> Any: ...

class DefaultHelpCommand(HelpCommand[_CT]):
    width: int
    sort_commands: bool
    indent: int
    commands_heading: str
    no_category: str
    paginator: _PaginatorProtocol
    def __init__(
        self,
        *,
        show_hidden: bool = ...,
        verify_checks: bool = ...,
        command_attrs: _CommandAttrs = ...,
        width: int = ...,
        indent: int = ...,
        sort_commands: bool = ...,
        dm_help: Optional[bool] = ...,
        dm_help_threshold: Optional[int] = ...,
        commands_heading: str = ...,
        no_category: str = ...,
        paginator: Optional[_PaginatorProtocol] = ...,
    ) -> None: ...
    def shorten_text(self, text: str) -> str: ...
    def get_ending_note(self) -> str: ...
    def add_indented_commands(
        self,
        commands: Sequence[Command[_CT]],
        *,
        heading: str,
        max_size: Optional[int] = ...,
    ) -> None: ...
    async def send_pages(self) -> None: ...
    def add_command_formatting(self, command: Command[_CT]) -> None: ...
    async def prepare_help_command(self, ctx: _CT, command: Optional[str]) -> None: ...  # type: ignore[override]
    async def send_bot_help(
        self, mapping: Mapping[Optional[Cog[_CT]], List[Command[_CT]]]
    ) -> None: ...
    async def send_command_help(self, command: Command[_CT]) -> None: ...
    async def send_group_help(self, group: Group[_CT]) -> None: ...
    async def send_cog_help(self, cog: Cog[_CT]) -> None: ...

class MinimalHelpCommand(HelpCommand[_CT]):
    sort_commands: bool
    commands_heading: str
    aliases_heading: str
    no_category: str
    paginator: _PaginatorProtocol
    def __init__(
        self,
        *,
        show_hidden: bool = ...,
        verify_checks: bool = ...,
        command_attrs: _CommandAttrs = ...,
        sort_commands: bool = ...,
        commands_heading: str = ...,
        dm_help: Optional[bool] = ...,
        dm_help_threshold: Optional[int] = ...,
        aliases_heading: str = ...,
        no_category: str = ...,
        paginator: Optional[_PaginatorProtocol] = ...,
    ) -> None: ...
    async def send_pages(self) -> None: ...
    def get_opening_note(self) -> str: ...
    def get_command_signature(self, command: Command[_CT]) -> str: ...
    def get_ending_note(self) -> Optional[str]: ...
    def add_bot_commands_formatting(
        self, commands: Sequence[Command[_CT]], heading: str
    ) -> None: ...
    def add_subcommand_formatting(self, command: Command[_CT]) -> None: ...
    def add_aliases_formatting(self, aliases: Sequence[str]) -> None: ...
    def add_command_formatting(self, command: Command[_CT]) -> None: ...
    async def prepare_help_command(self, ctx: _CT, command: Optional[str]) -> None: ...  # type: ignore[override]
    async def send_bot_help(
        self, mapping: Mapping[Optional[Cog[_CT]], List[Command[_CT]]]
    ) -> None: ...
    async def send_cog_help(self, cog: Cog[_CT]) -> None: ...
    async def send_group_help(self, group: Group[_CT]) -> None: ...
    async def send_command_help(self, command: Command[_CT]) -> None: ...
