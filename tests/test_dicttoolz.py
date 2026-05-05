"""Tests for toolz.dicttoolz to verify stubs work correctly."""

import sys
from typing import TypeGuard, assert_type

if sys.version_info >= (3, 13):
    from typing import TypeIs  # pyright: ignore[reportUnreachable]
else:
    from typing_extensions import TypeIs

import pytest
import toolz.dicttoolz as dt


class TestMerge:
    """Tests for merge function."""

    def test_basic(self) -> None:
        """merge should combine dictionaries."""
        result = dt.merge({1: "one"}, {2: "two"})

        _ = assert_type(result, dict[int, str])
        assert result == {1: "one", 2: "two"}

    def test_precedence(self) -> None:
        """Later dictionaries have precedence."""
        result = dt.merge({1: 2, 3: 4}, {3: 3, 4: 4})

        _ = assert_type(result, dict[int, int])
        assert result == {1: 2, 3: 3, 4: 4}


class TestMergeWith:
    """Tests for merge_with function."""

    def test_sum(self) -> None:
        """merge_with should apply function to combined values."""
        result = dt.merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
        _ = assert_type(result, dict[int, int])
        assert result == {1: 11, 2: 22}


class TestValmap:
    """Tests for valmap function."""

    def test_basic(self) -> None:
        """valmap should apply function to values."""
        bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
        result = dt.valmap(sum, bills)

        _ = assert_type(result, dict[str, int])
        assert result == {"Alice": 65, "Bob": 45}


class TestKeymap:
    """Tests for keymap function."""

    def test_basic(self) -> None:
        """keymap should apply function to keys."""
        bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
        result = dt.keymap(str.lower, bills)

        _ = assert_type(result, dict[str, list[int]])
        assert result == {"alice": [20, 15, 30], "bob": [10, 35]}


class TestItemmap:
    """Tests for itemmap function."""

    def test_basic(self) -> None:
        """itemmap should apply function to items."""
        accountids = {"Alice": 10, "Bob": 20}

        def swap(item: tuple[str, int]) -> tuple[int, str]:
            k, v = item
            return (v, k)

        result = dt.itemmap(swap, accountids)

        _ = assert_type(result, dict[int, str])
        assert result == {10: "Alice", 20: "Bob"}


class TestValfilter:
    """Tests for valfilter function."""

    def test_basic(self) -> None:
        """valfilter should filter items by value."""

        def iseven(x: int) -> bool:
            return x % 2 == 0

        d = {1: 2, 2: 3, 3: 4, 4: 5}
        result = dt.valfilter(iseven, d)

        _ = assert_type(result, dict[int, int])
        assert result == {1: 2, 3: 4}

    def test_type_guard(self) -> None:
        """valfilter with TypeGuard predicate should narrow value type."""

        def is_str(x: str | int) -> TypeGuard[str]:
            return isinstance(x, str)

        d: dict[int, str | int] = {1: "hello", 2: 42, 3: "world"}
        result = dt.valfilter(is_str, d)

        _ = assert_type(result, dict[int, str])
        assert result == {1: "hello", 3: "world"}

    def test_type_is(self) -> None:
        """valfilter with TypeIs predicate should narrow value type."""

        def is_str(x: str | int) -> TypeIs[str]:
            return isinstance(x, str)

        d: dict[int, str | int] = {1: "hello", 2: 42, 3: "world"}
        result = dt.valfilter(is_str, d)

        _ = assert_type(result, dict[int, str])
        assert result == {1: "hello", 3: "world"}


class TestKeyfilter:
    """Tests for keyfilter function."""

    def test_basic(self) -> None:
        """keyfilter should filter items by key."""

        def iseven(x: int) -> bool:
            return x % 2 == 0

        d = {1: 2, 2: 3, 3: 4, 4: 5}
        result = dt.keyfilter(iseven, d)

        _ = assert_type(result, dict[int, int])
        assert result == {2: 3, 4: 5}

    def test_string_values(self) -> None:
        """keyfilter with string values (README example)."""

        def iseven(x: int) -> bool:
            return x % 2 == 0

        result = dt.keyfilter(iseven, {1: "a", 2: "b", 3: "c"})

        _ = assert_type(result, dict[int, str])
        assert result == {2: "b"}

    def test_type_guard(self) -> None:
        """keyfilter with TypeGuard predicate should narrow key type."""

        def is_str(x: str | int) -> TypeGuard[str]:
            return isinstance(x, str)

        d: dict[str | int, int] = {"a": 1, 2: 2, "b": 3}
        result = dt.keyfilter(is_str, d)

        _ = assert_type(result, dict[str, int])
        assert result == {"a": 1, "b": 3}

    def test_type_is(self) -> None:
        """keyfilter with TypeIs predicate should narrow key type."""

        def is_str(x: str | int) -> TypeIs[str]:
            return isinstance(x, str)

        d: dict[str | int, int] = {"a": 1, 2: 2, "b": 3}
        result = dt.keyfilter(is_str, d)

        _ = assert_type(result, dict[str, int])
        assert result == {"a": 1, "b": 3}


class TestItemfilter:
    """Tests for itemfilter function."""

    def test_basic(self) -> None:
        """itemfilter should filter items by item."""

        def isvalid(item: tuple[int, int]) -> bool:
            k, v = item
            return k % 2 == 0 and v < 4

        d = {1: 2, 2: 3, 3: 4, 4: 5}
        result = dt.itemfilter(isvalid, d)

        _ = assert_type(result, dict[int, int])
        assert result == {2: 3}

    def test_type_guard(self) -> None:
        """itemfilter with TypeGuard predicate should narrow item type."""

        def has_str_value(item: tuple[int, str | int]) -> TypeGuard[tuple[int, str]]:
            return isinstance(item[1], str)

        d: dict[int, str | int] = {1: "hello", 2: 42, 3: "world"}
        result = dt.itemfilter(has_str_value, d)

        _ = assert_type(result, dict[int, str])
        assert result == {1: "hello", 3: "world"}

    def test_type_is(self) -> None:
        """itemfilter with TypeIs predicate should narrow item type."""

        def has_str_value(item: tuple[int, str | int]) -> TypeIs[tuple[int, str]]:
            return isinstance(item[1], str)

        d: dict[int, str | int] = {1: "hello", 2: 42, 3: "world"}
        result = dt.itemfilter(has_str_value, d)

        _ = assert_type(result, dict[int, str])
        assert result == {1: "hello", 3: "world"}


class TestAssoc:
    """Tests for assoc function."""

    def test_update(self) -> None:
        """assoc should return new dict with updated value."""
        result = dt.assoc({"x": 1}, "x", 2)

        _ = assert_type(result, dict[str, int])
        assert result == {"x": 2}

    def test_add(self) -> None:
        """assoc should return new dict with new key."""
        result = dt.assoc({"x": 1}, "y", 3)

        _ = assert_type(result, dict[str, int])
        assert result == {"x": 1, "y": 3}

    def test_immutable(self) -> None:
        """assoc should not modify the original dictionary."""
        original = {"x": 1}
        result = dt.assoc(original, "y", 2)

        _ = assert_type(result, dict[str, int])
        assert original == {"x": 1}


class TestDissoc:
    """Tests for dissoc function."""

    def test_single(self) -> None:
        """dissoc should return new dict with key removed."""
        result = dt.dissoc({"x": 1, "y": 2}, "y")

        _ = assert_type(result, dict[str, int])
        assert result == {"x": 1}

    def test_multiple(self) -> None:
        """dissoc should remove multiple keys."""
        result = dt.dissoc({"x": 1, "y": 2}, "y", "x")

        _ = assert_type(result, dict[str, int])
        assert result == {}

    def test_missing(self) -> None:
        """dissoc should ignore missing keys."""
        result = dt.dissoc({"x": 1}, "y")

        _ = assert_type(result, dict[str, int])
        assert result == {"x": 1}

    def test_immutable(self) -> None:
        """dissoc should not modify the original dictionary."""
        original = {"x": 1, "y": 2}
        result = dt.dissoc(original, "y")

        _ = assert_type(result, dict[str, int])
        assert original == {"x": 1, "y": 2}


class TestAssocIn:
    """Tests for assoc_in function."""

    def test_nested(self) -> None:
        """assoc_in should update nested value."""
        purchase = {
            "name": "Alice",
            "order": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
            "credit card": "5555-1234-1234-1234",
        }
        result = dt.assoc_in(purchase, ("order", "costs"), [0.25, 1.00])

        _ = assert_type(
            result,
            dict[
                str, dict[str, list[str] | list[float]] | str | list[str] | list[float]
            ],
        )
        assert result["order"]["costs"] == [0.25, 1.00]  # pyright: ignore[reportArgumentType,reportCallIssue]
        assert result["name"] == "Alice"

    def test_immutable(self) -> None:
        """assoc_in should not modify the original dictionary."""
        original: dict[str, dict[str, int]] = {"a": {"b": 1}}
        result = dt.assoc_in(original, ["a", "b"], 2)

        _ = assert_type(result, dict[str, dict[str, int] | int])
        assert original == {"a": {"b": 1}}


class TestUpdateIn:
    """Tests for update_in function."""

    def test_basic(self) -> None:
        """update_in should apply function to nested value."""

        def inc(x: int) -> int:
            return x + 1

        result = dt.update_in({"a": 0}, ["a"], inc)

        _ = assert_type(result, dict[str, int])
        assert result == {"a": 1}

    # TODO see https://github.com/mgrinshpon/toolz-stubs/issues/13
    # def test_nested(self) -> None:
    #     """update_in with nested path."""
    #     transaction = {
    #         "name": "Alice",
    #         "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
    #         "credit card": "5555-1234-1234-1234",
    #     }
    #     result = dt.update_in(transaction, ["purchase", "costs"], sum)

    #     _ = assert_type(result, dict[str, str | dict[str, list[str] | list[float]]])
    #     assert result["purchase"]["costs"] == 1.75  # type: ignore[index]

    def test_with_default(self) -> None:
        """update_in creating nested structure with default."""
        result = dt.update_in({}, [1, 2, 3], str, default="bar")

        _ = assert_type(result, dict[int, str])
        assert result == {1: {2: {3: "bar"}}}

    def test_add_to_existing(self) -> None:
        """update_in adding to existing dict with default."""

        def inc(x: int) -> int:
            return x + 1

        result = dt.update_in({1: "foo"}, [2, 3, 4], inc, 0)

        _ = assert_type(result, dict[int, str | int])
        assert result == {1: "foo", 2: {3: {4: 1}}}

    def test_immutable(self) -> None:
        """update_in should not modify the original dictionary."""
        original = {"a": 0}

        def add_one(x: int) -> int:
            return x + 1

        result = dt.update_in(original, ["a"], add_one)

        _ = assert_type(result, dict[str, int])
        assert original == {"a": 0}


class TestGetIn:
    """Tests for get_in function."""

    # TODO see https://github.com/mgrinshpon/toolz-stubs/issues/14
    # def test_nested_dict(self) -> None:
    #     """get_in should retrieve nested dict value."""
    #     transaction = {
    #         "name": "Alice",
    #         "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
    #         "credit card": "5555-1234-1234-1234",
    #     }
    #     result = dt.get_in(["purchase", "items", 0], transaction)

    #     _ = assert_type(result, str | dict[str, list[str] | list[float]] | None)
    #     assert result == "Apple"

    def test_single_key(self) -> None:
        """get_in with single key."""
        transaction = {
            "name": "Alice",
            "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
            "credit card": "5555-1234-1234-1234",
        }
        result = dt.get_in(["name"], transaction)

        _ = assert_type(result, str | dict[str, list[str] | list[float]] | None)
        assert result == "Alice"

    def test_missing_returns_none(self) -> None:
        """get_in returns None for missing key by default."""
        transaction = {
            "name": "Alice",
            "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
            "credit card": "5555-1234-1234-1234",
        }
        result = dt.get_in(["purchase", "total"], transaction)

        _ = assert_type(result, str | dict[str, list[str] | list[float]] | None)
        assert result is None

    # def test_missing_index_returns_none(self) -> None:
    #     """get_in returns None for missing index."""
    #     transaction = {
    #         "name": "Alice",
    #         "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
    #         "credit card": "5555-1234-1234-1234",
    #     }
    #     result = dt.get_in(["purchase", "items", 10], transaction)

    #     _ = assert_type(result, str | dict[str, list[str] | list[float]] | None)
    #     assert result is None

    def test_with_default(self) -> None:
        """get_in with explicit default value."""
        transaction = {
            "name": "Alice",
            "purchase": {"items": ["Apple", "Orange"], "costs": [0.50, 1.25]},
            "credit card": "5555-1234-1234-1234",
        }
        result = dt.get_in(["purchase", "total"], transaction, 0)

        _ = assert_type(result, str | dict[str, list[str] | list[float]] | int)
        assert result == 0

    def test_no_default_raises(self) -> None:
        """get_in with no_default=True should raise KeyError."""

        coll: dict[str, int] = {}

        with pytest.raises(KeyError):
            _ = dt.get_in(["y"], coll, no_default=True)
