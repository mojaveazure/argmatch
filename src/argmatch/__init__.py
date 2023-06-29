#!/usr/bin/env python3

"""Argument Verification

This module provides argument verification similar to R's
``match.arg()`` function

"""

import re as _re
import ast as _ast
import types as _types
import inspect as _inspect

from typing import TypeVar as _TypeVar
from collections.abc import Sequence as _Sequence

__version__: str = "0.0.0.9000"

__all__: list[str] = [
    'arg_match',
    'ArgMatchError'
]

S = _TypeVar('S', str, bytes)
"""typing.TypeVar: ``str`` or ``bytes`` or any subclass of ``str`` or ``bytes``"""

class ArgMatchError(ValueError):

    """The Argument Match Error Class

    Args:
            n: The number of argument matches found; must be greater
                than or equal to 0
            args: An optional sequence of initial arguments or matches
                to be added to the message; if provided an ``n`` is
                greater than 0, `len(args)` must be ``n``

    Raises:
        ValueError: If ``n`` is less than 0
        ValueError: If ``n`` is greater than 0 and ``len(args)`` is
            not equal to ``n``
    """

    def __init__(self, n: int, args: _Sequence[S]|None=None) -> None:
        if isinstance(args, S.__constraints__):
            args: tuple[S] = tuple(args)
        self._n: int = int(n)
        self._args = args
        if self.n < 0:
            raise ValueError("'n' must be a positive integer")
        if self.args and self.n and self.n != len(args):
            raise ValueError("'args' must be of length 'n' when provided")

    def __repr__(self) -> str:
        return "%(cls)s(n=%(n)i, args=%(args)s)" % {
            'cls': self.__class__.__name__,
            'n': self.n,
            'args': str(self.args)
        }

    def __str__(self) -> str:
        if self.n:
            msg: str = "Too many matches (%i)" % self.n
            if self.args:
                msg += ", found '%s'" % "', '".join(self.args)
            return msg
        msg: str = "No argument match found"
        if len(self.args) == 1:
            msg += ", should be '%s'" % self.args[0]
        elif self.args:
            msg += ", should be one of '%s'" % "', '".join(self.args)
        return msg

    n = property(fget=lambda self: self._n, doc="The number of matches")

    @property
    def args(self) -> tuple[str, ...]|None:
        """The matches or original arguments as a tuple"""
        if not self._args:
            return None
        return tuple(x if isinstance(x, str) else x.decode() for x in self._args)


def arg_match(
        arg: S|_Sequence[S]|None=None,
        /,
        *,
        choices: _Sequence[S]|S|None=None,
        multiple: bool=False
) -> S|_Sequence[S]:
    """Argument Verification

    Args:
        arg: [positional-only] The argument to validate; must be a single
            string unless ``multiple`` is ``True``, in which case it may be
            a sequence of strings
        choices: [keyword-only] A sequence of strings that ``arg`` may be;
            if not provided, will attempt to resolve from the signature
            of the calling function
        multiple: [keyword-only] Allow ``arg`` to have more than one element

    Returns:
        If ``multiple`` is ``True``, a sequence containing all values of
            ``arg`` that match ``choices``; otherwise, the value of
            ``choices`` that ``arg`` matches

    Raises:
        ValueError: If ``arg`` is a sequence of length greater than 1 and
            ``multiple`` is ``False``
        ArgMatchError: If the number of matches is zero
        ArgMatchError: If the number of matches is greater than 1 and
            ``multiple`` is ``False``
    """
    if not choices:
        curr: _types.FrameType = _inspect.currentframe()
        caller: _inspect.FrameInfo = _inspect.getouterframes(curr, 2)[1]
        if not caller.code_context:
            raise ValueError("Cannot determine code context")
        call: _ast.AST = _ast.parse(caller.code_context[-1].strip()).body[0]
        while not isinstance(call, _ast.Call):
            call: _ast.AST = call.value
        arg_id: str = call.args[0].id
        sig: _inspect.Signature = _inspect.signature(caller.frame.f_globals[caller.function])
        choices: _Sequence[S]|S = sig.parameters[arg_id].default
        print(choices)
    if isinstance(choices, S.__constraints__):
        choices: tuple[S] = (choices,)
    if not arg:
        return choices[0]
    if isinstance(arg, S.__constraints__):
        arg: tuple[S]= (arg,)
    if not multiple:
        if arg == choices:
            return arg[0]
        if len(arg) > 1:
            raise ValueError("'arg' must be of length 1")
    matches: tuple[S|None, ...] = tuple(x for y in arg for x in choices if _re.match(y, x))
    if not matches:
        raise ArgMatchError(n=0, args=choices)
    if len(matches) > 1 and not multiple:
        raise ArgMatchError(n=len(matches), args=matches)
    if len(matches) == 1:
        return matches[0]
    return matches


def _f(x=('aa', 'ab'), y=None):
    x = arg_match(x)
    return x
