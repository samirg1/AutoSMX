from typing import Callable, MutableMapping, TypeVar

_K = TypeVar("_K")
_V = TypeVar("_V")


def remove_from_mapping(mutable_mapping: MutableMapping[_K, _V], *, key_condition: Callable[[_K], bool] = lambda _: False, value_condition: Callable[[_V], bool] = lambda _: False) -> None:
    keys_to_remove: set[_K] = set()
    for key, value in mutable_mapping.items():
        if key_condition(key):
            keys_to_remove.add(key)
        elif value_condition(value):
            keys_to_remove.add(key)

    for key in keys_to_remove:
        del mutable_mapping[key]


item_model = "AT - SLINGS -> LSS920332"
print(item_model.partition("->")[0])