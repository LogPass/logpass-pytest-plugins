import importlib
import inspect
import random
import string
import sys

from pathlib import Path
from types import ModuleType
from typing import (
    Any,
    Type,
)

import inflection
import pytest

from factory import Factory
from pytest_factoryboy import register
from typing_extensions import Final

ROOT_DIR_OPTION: Final = 'auto_pytest_factoryboy_root_dir'
FACTORY_FILE_PATTERNS_OPTION: Final = 'auto_pytest_factoryboy_globs'


@pytest.hookimpl()
def pytest_addoption(parser):
    """Register plugin options."""
    parser.addini(
        ROOT_DIR_OPTION,
        'Directory where factories declarations searching starts',
        type='string',
        default='.',
    )
    parser.addini(
        FACTORY_FILE_PATTERNS_OPTION,
        (
            'List of `glob` patterns used to find files with `factoryboy` '
            + 'factories declarations starting from the '
            + '`auto_pytest_factoryboy_root_dir` directory'
        ),
        type='args',
        default=['**/factories*.py'],
    )


@pytest.hookimpl()
def pytest_configure(config):
    """`pytest` configuration hook.

    Automatically register all `factoryboy` factories from selected
    directories.

    """
    root_dir = Path(config.getini(ROOT_DIR_OPTION))
    for factory_file_pattern in config.getini(FACTORY_FILE_PATTERNS_OPTION):
        _recursively_register_factories_from(root_dir, factory_file_pattern)


def _recursively_register_factories_from(
    root_dir: Path,
    glob_pathname: str,
) -> None:
    factories_counter = 0
    factories_prefix = ''.join(
        random.choices(string.ascii_lowercase, k=10),  # noqa: S311
    )
    for factories_path in root_dir.glob(glob_pathname):
        factories_module = _import_module_from(
            str(factories_path),
            as_name='_{0}_factories{1}'.format(
                factories_prefix,
                factories_counter,
            ),
        )
        factories_counter += 1
        _register_factories_from(factories_module)


def _import_module_from(path: str, as_name: str) -> ModuleType:
    """Import module from ``path`` as ``as_name``."""
    module_spec = importlib.util.spec_from_file_location(as_name, path)
    assert module_spec  # satisfy `mypy`  # noqa: S101
    module = importlib.util.module_from_spec(module_spec)
    assert isinstance(module_spec.loader, importlib.abc.Loader)  # noqa: S101
    module_spec.loader.exec_module(module)
    return module


def _register_factories_from(module: ModuleType) -> None:
    """Try to register all `factoryboy` factories from ``module``."""
    for name, factory_wannabe in module.__dict__.items():  # noqa: WPS609
        if _is_concrete_factory(name, factory_wannabe):
            frame = sys._getframe()  # noqa: WPS437
            plugin_module = inspect.getmodule(frame)
            assert plugin_module  # noqa: S101  # satisfy `mypy`
            register(
                factory_wannabe,
                _name=_get_model_name(factory_wannabe),
                _caller_locals=plugin_module.__dict__,
            )


def _is_concrete_factory(name: str, class_: Any) -> bool:  # type: ignore[misc]
    """Check if ``class_`` is concrete `factoryboy` factory class."""
    return (
        inspect.isclass(class_)
        and issubclass(class_, Factory)
        and name != 'SubFactory'
        and not class_._meta.abstract  # noqa: WPS437
    )


# TODO(skarzi): refactor name generation when following PR will be released:
# https://github.com/pytest-dev/pytest-factoryboy/pull/163
# TODO(skarzi): firstly try to extract model name from some attribute
# e.g. `_default_model_name`
# https://github.com/LogPass/logpass_pytest_plugins/issues/2
def _get_model_name(factory_class: Type[Factory]) -> str:
    """Extract model name from ``factory_class``."""
    model_class = factory_class._meta.model  # noqa: WPS437
    if isinstance(model_class, str):
        model_name = model_class.rsplit('.', 1)[-1]
    else:
        model_name = model_class.__name__
    return inflection.underscore(model_name)
