# pyright: reportAny=false
import collections.abc
import typing

from _typeshed import SupportsRichComparison

from .utils import no_default

__all__ = (
    "remove",
    "accumulate",
    "groupby",
    "merge_sorted",
    "interleave",
    "unique",
    "isiterable",
    "isdistinct",
    "take",
    "drop",
    "take_nth",
    "first",
    "second",
    "nth",
    "last",
    "get",
    "concat",
    "concatv",
    "mapcat",
    "cons",
    "interpose",
    "frequencies",
    "reduceby",
    "iterate",
    "sliding_window",
    "partition",
    "partition_all",
    "count",
    "pluck",
    "join",
    "tail",
    "diff",
    "topk",
    "peek",
    "peekn",
    "random_sample",
)

### Special types for toolz
type _NoDefaultType = typing.Literal["__no__default__"]
type _NoPadType = typing.Literal["__no__pad__"]

class _Randomable(typing.Protocol):
    def random(self) -> float: ...

### Toolz itself

def remove[T](
    predicate: collections.abc.Callable[[T], bool], seq: collections.abc.Iterable[T]
) -> collections.abc.Iterable[T]:
    """Return those items of sequence for which predicate(item) is False

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(remove(iseven, [1, 2, 3, 4]))
    [1, 3]
    """
    ...

@typing.overload
def accumulate[T](
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
) -> collections.abc.Iterator[T]: ...
@typing.overload
def accumulate[T](
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    initial: T,
) -> collections.abc.Iterator[T]: ...
def accumulate[T](
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    initial: T | _NoDefaultType = no_default,
) -> collections.abc.Iterator[T]:
    """Repeatedly apply binary function to a sequence, accumulating results

    >>> from operator import add, mul
    >>> list(accumulate(add, [1, 2, 3, 4, 5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate(mul, [1, 2, 3, 4, 5]))
    [1, 2, 6, 24, 120]

    Accumulate is similar to ``reduce`` and is good for making functions like
    cumulative sum:

    >>> from functools import partial, reduce
    >>> sum    = partial(reduce, add)
    >>> cumsum = partial(accumulate, add)

    Accumulate also takes an optional argument that will be used as the first
    value. This is similar to reduce.

    >>> list(accumulate(add, [1, 2, 3], -1))
    [-1, 0, 2, 5]
    >>> list(accumulate(add, [], 1))
    [1]

    See Also:
        itertools.accumulate :  In standard itertools for Python 3.2+
    """
    ...

def groupby[KT, T](
    key: collections.abc.Callable[[T], KT], seq: collections.abc.Iterable[T]
) -> dict[KT, list[T]]:
    """Group a collection by a key function

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    Non-callable keys imply grouping on a member.

    >>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
    ...                    {'name': 'Bob', 'gender': 'M'},
    ...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}

    Not to be confused with ``itertools.groupby``

    See Also:
        countby
    """
    ...

def merge_sorted[CT: SupportsRichComparison](
    *seqs: collections.abc.Iterable[CT],
    key: collections.abc.Callable[[CT], CT] | None = None,
) -> collections.abc.Iterator[CT]:
    """Merge and sort a collection of sorted collections

    This works lazily and only keeps one value from each iterable in memory.

    >>> list(merge_sorted([1, 3, 5], [2, 4, 6]))
    [1, 2, 3, 4, 5, 6]

    >>> ''.join(merge_sorted('abc', 'abc', 'abc'))
    'aaabbbccc'

    The "key" function used to sort the input may be passed as a keyword.

    >>> list(merge_sorted([2, 3], [1, 3], key=lambda x: x // 3))
    [2, 1, 3, 3]
    """
    ...

def interleave[T](
    seqs: collections.abc.Iterable[collections.abc.Iterable[T]],
) -> collections.abc.Iterator[T]:
    """Interleave a sequence of sequences

    >>> list(interleave([[1, 2], [3, 4]]))
    [1, 3, 2, 4]

    >>> ''.join(interleave(('ABC', 'XY')))
    'AXBYC'

    Both the individual sequences and the sequence of sequences may be infinite

    Returns a lazy iterator
    """
    ...

def unique[T](
    seq: collections.abc.Iterable[T],
    key: collections.abc.Callable[[T], typing.Any] | None = None,
) -> collections.abc.Iterator[T]:
    """Return only unique elements of a sequence

    >>> tuple(unique((1, 2, 3)))
    (1, 2, 3)
    >>> tuple(unique((1, 2, 1, 3)))
    (1, 2, 3)

    Uniqueness can be defined by key keyword

    >>> tuple(unique(['cat', 'mouse', 'dog', 'hen'], key=len))
    ('cat', 'mouse')
    """
    ...

def isiterable(x: typing.Any) -> typing.TypeGuard[collections.abc.Iterable[typing.Any]]:
    """Is x iterable?

    >>> isiterable([1, 2, 3])
    True
    >>> isiterable('abc')
    True
    >>> isiterable(5)
    False
    """
    ...

def isdistinct(
    seq: collections.abc.Iterable[typing.Any] | collections.abc.Sequence[typing.Any],
) -> bool:
    """All values in sequence are distinct

    >>> isdistinct([1, 2, 3])
    True
    >>> isdistinct([1, 2, 1])
    False

    >>> isdistinct("Hello")
    False
    >>> isdistinct("World")
    True
    """
    ...

def take[T](n: int, seq: collections.abc.Iterable[T]) -> collections.abc.Iterator[T]:
    """The first n elements of a sequence

    >>> list(take(2, [10, 20, 30, 40, 50]))
    [10, 20]

    See Also:
        drop
        tail
    """
    ...

def tail[T](n: int, seq: collections.abc.Iterable[T]) -> collections.abc.Iterator[T]:
    """The last n elements of a sequence

    >>> tail(2, [10, 20, 30, 40, 50])
    [40, 50]

    See Also:
        drop
        take
    """
    ...

def drop[T](n: int, seq: collections.abc.Iterable[T]) -> collections.abc.Iterator[T]:
    """The sequence following the first n elements

    >>> list(drop(2, [10, 20, 30, 40, 50]))
    [30, 40, 50]

    See Also:
        take
        tail
    """
    ...

def take_nth[T](
    n: int, seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[T]:
    """Every nth item in seq

    >>> list(take_nth(2, [10, 20, 30, 40, 50]))
    [10, 30, 50]
    """
    ...

def first[T](seq: collections.abc.Iterable[T]) -> T:
    """The first element in a sequence

    >>> first('ABC')
    'A'
    """
    ...

def second[T](seq: collections.abc.Iterable[T]) -> T:
    """The second element in a sequence

    >>> second('ABC')
    'B'
    """
    ...

def nth[T](n: int, seq: collections.abc.Iterable[T]) -> T:
    """The nth element in a sequence

    >>> nth(1, 'ABC')
    'B'
    """
    ...

def last[T](seq: collections.abc.Iterable[T]) -> T:
    """The last element in a sequence

    >>> last('ABC')
    'C'
    """
    ...

def rest[T](seq: collections.abc.Iterable[T]) -> collections.abc.Iterable[T]:
    """All but the first element in a sequence

    >>> rest('ABC')
    'BC'
    """
    # Warning - this function is not exposed via __all__ and should be considered private.
    ...

@typing.overload
def get[T](
    ind: list[typing.Any],
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    default: T | _NoDefaultType = ...,
) -> tuple[T, ...]: ...
@typing.overload
def get[T](
    ind: typing.Any,
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    default: T | _NoDefaultType = ...,
) -> T: ...
def get[T](
    ind: typing.Any | list[typing.Any],
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    default: T | _NoDefaultType = no_default,
) -> T | tuple[T, ...]:
    """Get element in a sequence or dict

    Provides standard indexing

    >>> get(1, 'ABC')       # Same as 'ABC'[1]
    'B'

    Pass a list to get multiple values

    >>> get([1, 2], 'ABC')  # ('ABC'[1], 'ABC'[2])
    ('B', 'C')

    Works on any value that supports indexing/getitem
    For example here we see that it works with dictionaries

    >>> phonebook = {'Alice':  '555-1234',
    ...              'Bob':    '555-5678',
    ...              'Charlie':'555-9999'}
    >>> get('Alice', phonebook)
    '555-1234'

    >>> get(['Alice', 'Bob'], phonebook)
    ('555-1234', '555-5678')

    Provide a default for missing values

    >>> get(['Alice', 'Dennis'], phonebook, None)
    ('555-1234', None)

    See Also:
        pluck
    """
    ...

def concat[T](
    seqs: collections.abc.Iterable[collections.abc.Iterable[T]],
) -> collections.abc.Iterator[T]:
    """Concatenate zero or more iterables, any of which may be infinite.

    An infinite sequence will prevent the rest of the arguments from
    being included.

    We use chain.from_iterable rather than ``chain(*seqs)`` so that seqs
    can be a generator.

    >>> list(concat([[], [1], [2, 3]]))
    [1, 2, 3]

    See also:
        itertools.chain.from_iterable  equivalent
    """
    ...

def concatv[T](*seqs: collections.abc.Iterable[T]) -> collections.abc.Iterator[T]:
    """Variadic version of concat

    >>> list(concatv([], ["a"], ["b", "c"]))
    ['a', 'b', 'c']

    See also:
        itertools.chain
    """
    ...

def mapcat[T, R](
    func: collections.abc.Callable[[T], collections.abc.Iterable[R]],
    seqs: collections.abc.Iterable[T],
) -> collections.abc.Iterator[R]:
    """Apply func to each sequence in seqs, concatenating results.

    >>> list(mapcat(lambda s: [c.upper() for c in s],
    ...             [["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']
    """
    ...

def cons[T](el: T, seq: collections.abc.Iterable[T]) -> collections.abc.Iterator[T]:
    """Add el to beginning of (possibly infinite) sequence seq.

    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    ...

def interpose[T](
    el: T, seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[T]:
    """Introduce element between each pair of elements in seq

    >>> list(interpose("a", [1, 2, 3]))
    [1, 'a', 2, 'a', 3]
    """
    ...

def frequencies[T](seq: collections.abc.Iterable[T]) -> dict[T, int]:
    """Find number of occurrences of each value in seq

    >>> frequencies(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'])  #doctest: +SKIP
    {'cat': 3, 'ox': 1, 'pig': 2}

    See Also:
        countby
        groupby
    """
    ...

@typing.overload
def reduceby[T, K](
    key: collections.abc.Callable[[T], K],
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
) -> dict[K, T]: ...
@typing.overload
def reduceby[T, K](
    key: collections.abc.Callable[[T], K],
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    init: T | collections.abc.Callable[[], T],
) -> dict[K, T]: ...
@typing.overload
def reduceby[T](
    key: typing.Any,  # when not callable, use identity function
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
) -> dict[T, T]: ...
@typing.overload
def reduceby[T](
    key: typing.Any,  # when not callable, use identity function
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    init: T | collections.abc.Callable[[], T],
) -> dict[T, T]: ...
def reduceby[T, K](
    key: collections.abc.Callable[[T], K] | typing.Any,
    binop: collections.abc.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    init: T | collections.abc.Callable[[], T] | _NoDefaultType = no_default,
) -> dict[K, T]:
    """Perform a simultaneous groupby and reduction

    The computation:

    >>> result = reduceby(key, binop, seq, init)      # doctest: +SKIP

    is equivalent to the following:

    >>> def reduction(group):                           # doctest: +SKIP
    ...     return reduce(binop, group, init)           # doctest: +SKIP

    >>> groups = groupby(key, seq)                    # doctest: +SKIP
    >>> result = valmap(reduction, groups)              # doctest: +SKIP

    But the former does not build the intermediate groups, allowing it to
    operate in much less space.  This makes it suitable for larger datasets
    that do not fit comfortably in memory

    The ``init`` keyword argument is the default initialization of the
    reduction.  This can be either a constant value like ``0`` or a callable
    like ``lambda : 0`` as might be used in ``defaultdict``.

    Simple Examples
    ---------------

    >>> from operator import add, mul
    >>> iseven = lambda x: x % 2 == 0

    >>> data = [1, 2, 3, 4, 5]

    >>> reduceby(iseven, add, data)  # doctest: +SKIP
    {False: 9, True: 6}

    >>> reduceby(iseven, mul, data)  # doctest: +SKIP
    {False: 15, True: 8}

    Complex Example
    ---------------

    >>> projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000},
    ...             {'name': 'fight crime', 'state': 'IL', 'cost': 100000},
    ...             {'name': 'help farmers', 'state': 'IL', 'cost': 2000000},
    ...             {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]

    >>> reduceby('state',                        # doctest: +SKIP
    ...          lambda acc, x: acc + x['cost'],
    ...          projects, 0)
    {'CA': 1200000, 'IL': 2100000}

    Example Using ``init``
    ----------------------

    >>> def set_add(s, i):
    ...     s.add(i)
    ...     return s

    >>> reduceby(iseven, set_add, [1, 2, 3, 4, 1, 2, 3], set)  # doctest: +SKIP
    {True:  set([2, 4]),
     False: set([1, 3])}
    """
    ...

def iterate[T](
    func: collections.abc.Callable[[T], T], x: T
) -> collections.abc.Iterator[T]:
    """Repeatedly apply a function func onto an original input

    Yields x, then func(x), then func(func(x)), then func(func(func(x))), etc..

    >>> def inc(x):  return x + 1
    >>> counter = iterate(inc, 0)
    >>> next(counter)
    0
    >>> next(counter)
    1
    >>> next(counter)
    2

    >>> double = lambda x: x * 2
    >>> powers_of_two = iterate(double, 1)
    >>> next(powers_of_two)
    1
    >>> next(powers_of_two)
    2
    >>> next(powers_of_two)
    4
    >>> next(powers_of_two)
    8
    """
    ...

def sliding_window[T](
    n: int, seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[tuple[T, ...]]:
    """A sequence of overlapping subsequences

    >>> list(sliding_window(2, [1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    This function creates a sliding window suitable for transformations like
    sliding means / smoothing

    >>> mean = lambda seq: float(sum(seq)) / len(seq)
    >>> list(map(mean, sliding_window(2, [1, 2, 3, 4])))
    [1.5, 2.5, 3.5]
    """
    ...

no_pad = "__no__pad__"

@typing.overload
def partition[T, P](
    n: typing.Literal[1], seq: collections.abc.Iterable[T], pad: typing.Any = ...
) -> collections.abc.Iterator[tuple[T]]: ...
@typing.overload
def partition[T](
    n: int, seq: collections.abc.Iterable[T], pad: _NoPadType = ...
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def partition[T, P](
    n: int, seq: collections.abc.Iterable[T], pad: P
) -> collections.abc.Iterator[tuple[T | P, ...]]: ...
def partition[T, P](
    n: int, seq: collections.abc.Iterable[T], pad: P | _NoPadType = no_pad
) -> collections.abc.Iterator[tuple[T | P, ...]]:
    """Partition sequence into tuples of length n

    >>> list(partition(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    If the length of ``seq`` is not evenly divisible by ``n``, the final tuple
    is dropped if ``pad`` is not specified, or filled to length ``n`` by pad:

    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

    >>> list(partition(2, [1, 2, 3, 4, 5], pad=None))
    [(1, 2), (3, 4), (5, None)]

    See Also:
        partition_all
    """
    ...

@typing.overload
def partition_all[T](
    n: typing.Literal[1], seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[tuple[T]]: ...
@typing.overload
def partition_all[T](
    n: int, seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[tuple[T, ...]]: ...
def partition_all[T](
    n: int, seq: collections.abc.Iterable[T]
) -> collections.abc.Iterator[tuple[T, ...]]:
    """Partition all elements of sequence into tuples of length at most n

    The final tuple may be shorter to accommodate extra elements.

    >>> list(partition_all(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    >>> list(partition_all(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    See Also:
        partition
    """
    ...

def count(seq: collections.abc.Iterable[typing.Any]) -> int:
    """Count the number of items in seq

    Like the builtin ``len`` but works on lazy sequences.

    Not to be confused with ``itertools.count``

    See also:
        len
    """
    ...

@typing.overload
def pluck[T](
    ind: list[typing.Any],
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    default: T | _NoDefaultType = ...,
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def pluck[T](
    ind: typing.Any,
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    default: T | _NoDefaultType = ...,
) -> collections.abc.Iterator[T]: ...
def pluck[T](
    ind: typing.Any | list[typing.Any],
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    default: T | _NoDefaultType = no_default,
) -> collections.abc.Iterator[T] | collections.abc.Iterator[tuple[T, ...]]:
    """plucks an element or several elements from each item in a sequence.

    ``pluck`` maps ``itertoolz.get`` over a sequence and returns one or more
    elements of each item in the sequence.

    This is equivalent to running `map(curried.get(ind), seqs)`

    ``ind`` can be either a single string/index or a list of strings/indices.
    ``seqs`` should be sequence containing sequences or dicts.

    e.g.

    >>> data = [{'id': 1, 'name': 'Cheese'}, {'id': 2, 'name': 'Pies'}]
    >>> list(pluck('name', data))
    ['Cheese', 'Pies']
    >>> list(pluck([0, 1], [[1, 2, 3], [4, 5, 7]]))
    [(1, 2), (4, 5)]

    See Also:
        get
        map
    """
    ...

@typing.overload
def getter[T](
    index: list[typing.Any],
) -> collections.abc.Callable[
    [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]],
    tuple[T, ...],
]: ...
@typing.overload
def getter[T](
    index: typing.Any,
) -> collections.abc.Callable[
    [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]], T
]: ...
def getter[T](
    index: typing.Any | list[typing.Any],
) -> collections.abc.Callable[
    [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]],
    T | tuple[T, ...],
]:
    # Warning - this function is not exposed via __all__ and should be considered private.
    ...

# === CALLABLE + CALLABLE (4 overloads) ===
@typing.overload
def join[T, U](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
) -> collections.abc.Iterator[tuple[T, U]]: ...
@typing.overload
def join[T, U, L](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    left_default: L,
) -> collections.abc.Iterator[tuple[T | L, U]]: ...
@typing.overload
def join[T, U, R](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    *,
    right_default: R,
) -> collections.abc.Iterator[tuple[T, U | R]]: ...
@typing.overload
def join[T, U, L, R](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    left_default: L,
    right_default: R,
) -> collections.abc.Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + CALLABLE (4 overloads) ===
@typing.overload
def join[T, U](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
) -> collections.abc.Iterator[tuple[T, U]]: ...
@typing.overload
def join[T, U, L](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    left_default: L,
) -> collections.abc.Iterator[tuple[T | L, U]]: ...
@typing.overload
def join[T, U, R](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    *,
    right_default: R,
) -> collections.abc.Iterator[tuple[T, U | R]]: ...
@typing.overload
def join[T, U, L, R](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable],
    rightseq: collections.abc.Iterable[U],
    left_default: L,
    right_default: R,
) -> collections.abc.Iterator[tuple[T | L, U | R]]: ...

# === CALLABLE + HASHABLE (4 overloads) ===
@typing.overload
def join[T, U](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
) -> collections.abc.Iterator[tuple[T, U]]: ...
@typing.overload
def join[T, U, L](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    left_default: L,
) -> collections.abc.Iterator[tuple[T | L, U]]: ...
@typing.overload
def join[T, U, R](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    *,
    right_default: R,
) -> collections.abc.Iterator[tuple[T, U | R]]: ...
@typing.overload
def join[T, U, L, R](
    leftkey: collections.abc.Callable[[T], typing.Hashable],
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    left_default: L,
    right_default: R,
) -> collections.abc.Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + HASHABLE (4 overloads) ===
@typing.overload
def join[T, U](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
) -> collections.abc.Iterator[tuple[T, U]]: ...
@typing.overload
def join[T, U, L](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    left_default: L,
) -> collections.abc.Iterator[tuple[T | L, U]]: ...
@typing.overload
def join[T, U, R](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    *,
    right_default: R,
) -> collections.abc.Iterator[tuple[T, U | R]]: ...
@typing.overload
def join[T, U, L, R](
    leftkey: typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    left_default: L,
    right_default: R,
) -> collections.abc.Iterator[tuple[T | L, U | R]]: ...

# Implementation signature
def join[T, U, L, R](
    leftkey: collections.abc.Callable[[T], typing.Hashable] | typing.Hashable,
    leftseq: collections.abc.Iterable[T],
    rightkey: collections.abc.Callable[[U], typing.Hashable] | typing.Hashable,
    rightseq: collections.abc.Iterable[U],
    left_default: L | _NoDefaultType = no_default,
    right_default: R | _NoDefaultType = no_default,
) -> collections.abc.Iterator[tuple[T | L, U | R]]:
    """Join two sequences on common attributes

    This is a semi-streaming operation.  The LEFT sequence is fully evaluated
    and placed into memory.  The RIGHT sequence is evaluated lazily and so can
    be arbitrarily large.

    (Note: If right_default is defined, then unique keys of rightseq
        will also be stored in memory.)

    >>> friends = [('Alice', 'Edith'),
    ...            ('Alice', 'Zhao'),
    ...            ('Edith', 'Alice'),
    ...            ('Zhao', 'Alice'),
    ...            ('Zhao', 'Edith')]

    >>> cities = [('Alice', 'NYC'),
    ...           ('Alice', 'Chicago'),
    ...           ('Dan', 'Sydney'),
    ...           ('Edith', 'Paris'),
    ...           ('Edith', 'Berlin'),
    ...           ('Zhao', 'Shanghai')]

    >>> # Vacation opportunities
    >>> # In what cities do people have friends?
    >>> result = join(second, friends,
    ...               first, cities)
    >>> for ((a, b), (c, d)) in sorted(unique(result)):
    ...     print((a, d))
    ('Alice', 'Berlin')
    ('Alice', 'Paris')
    ('Alice', 'Shanghai')
    ('Edith', 'Chicago')
    ('Edith', 'NYC')
    ('Zhao', 'Chicago')
    ('Zhao', 'NYC')
    ('Zhao', 'Berlin')
    ('Zhao', 'Paris')

    Specify outer joins with keyword arguments ``left_default`` and/or
    ``right_default``.  Here is a full outer join in which unmatched elements
    are paired with None.

    >>> identity = lambda x: x
    >>> list(join(identity, [1, 2, 3],
    ...           identity, [2, 3, 4],
    ...           left_default=None, right_default=None))
    [(2, 2), (3, 3), (None, 4), (1, None)]

    Usually the key arguments are callables to be applied to the sequences.  If
    the keys are not obviously callable then it is assumed that indexing was
    intended, e.g. the following is a legal change.
    The join is implemented as a hash join and the keys of leftseq must be
    hashable. Additionally, if right_default is defined, then keys of rightseq
    must also be hashable.

    >>> # result = join(second, friends, first, cities)
    >>> result = join(1, friends, 0, cities)  # doctest: +SKIP
    """
    ...

@typing.overload
def diff[T](
    *seqs: collections.abc.Iterable[T],
    key: collections.abc.Callable[[T], typing.Any] | None = None,
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def diff[T](
    *seqs: collections.abc.Iterable[T],
    default: T,
    key: collections.abc.Callable[[T], typing.Any] | None = None,
) -> collections.abc.Iterator[tuple[T, ...]]: ...
def diff[T](
    *seqs: collections.abc.Iterable[T],
    default: T | _NoDefaultType = no_default,
    key: collections.abc.Callable[[T], typing.Any] | None = None,
) -> collections.abc.Iterator[tuple[T, ...]]:
    """Return those items that differ between sequences

    >>> list(diff([1, 2, 3], [1, 2, 10, 100]))
    [(3, 10)]

    Shorter sequences may be padded with a ``default`` value:

    >>> list(diff([1, 2, 3], [1, 2, 10, 100], default=None))
    [(3, 10), (None, 100)]

    A ``key`` function may also be applied to each item to use during
    comparisons:

    >>> list(diff(['apples', 'bananas'], ['Apples', 'Oranges'], key=str.lower))
    [('bananas', 'Oranges')]
    """
    ...

def topk[T](
    k: int,
    seq: collections.abc.Iterable[T],
    key: collections.abc.Callable[[T], SupportsRichComparison] | None = None,
) -> tuple[T, ...]:
    """Find the k largest elements of a sequence

    Operates lazily in ``n*log(k)`` time

    >>> topk(2, [1, 100, 10, 1000])
    (1000, 100)

    Use a key function to change sorted order

    >>> topk(2, ['Alice', 'Bob', 'Charlie', 'Dan'], key=len)
    ('Charlie', 'Alice')

    See also:
        heapq.nlargest
    """
    ...

def peek[T](
    seq: collections.abc.Iterable[T],
) -> tuple[T, collections.abc.Iterator[T]]:
    """Retrieve the next element of a sequence

    Returns the first element and an iterable equivalent to the original
    sequence, still having the element retrieved.

    >>> seq = [0, 1, 2, 3, 4]
    >>> first, seq = peek(seq)
    >>> first
    0
    >>> list(seq)
    [0, 1, 2, 3, 4]
    """
    ...

def peekn[T](
    n: int, seq: collections.abc.Iterable[T]
) -> tuple[tuple[T, ...], collections.abc.Iterator[T]]:
    """Retrieve the next n elements of a sequence

    Returns a tuple of the first n elements and an iterable equivalent
    to the original, still having the elements retrieved.

    >>> seq = [0, 1, 2, 3, 4]
    >>> first_two, seq = peekn(2, seq)
    >>> first_two
    (0, 1)
    >>> list(seq)
    [0, 1, 2, 3, 4]
    """
    ...

def random_sample[T](
    prob: float,
    seq: collections.abc.Iterable[T],
    random_state: int | _Randomable | None = None,
) -> collections.abc.Iterator[T]:
    """Return elements from a sequence with probability of prob

    Returns a lazy iterator of random items from seq.

    ``random_sample`` considers each item independently and without
    replacement. See below how the first time it returned 13 items and the
    next time it returned 6 items.

    >>> seq = list(range(100))
    >>> list(random_sample(0.1, seq)) # doctest: +SKIP
    [6, 9, 19, 35, 45, 50, 58, 62, 68, 72, 78, 86, 95]
    >>> list(random_sample(0.1, seq)) # doctest: +SKIP
    [6, 44, 54, 61, 69, 94]

    Providing an integer seed for ``random_state`` will result in
    deterministic sampling. Given the same seed it will return the same sample
    every time.

    >>> list(random_sample(0.1, seq, random_state=2016))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
    >>> list(random_sample(0.1, seq, random_state=2016))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]

    ``random_state`` can also be any object with a method ``random`` that
    returns floats between 0.0 and 1.0 (exclusive).

    >>> from random import Random
    >>> randobj = Random(2016)
    >>> list(random_sample(0.1, seq, random_state=randobj))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
    """
    ...
