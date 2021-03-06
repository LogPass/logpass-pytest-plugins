import pytest

from tests.logic.pytester import (
    disable_plugins,
    render_pytest_plugins,
)


@pytest.fixture
def tester(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `auto_pytest_factoryboy`."""
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest(
        render_pytest_plugins(
            'pytest-factoryboy',
            'logpass_pytest_plugins.contrib.auto_pytest_factoryboy',
        ),
    )
    with open(pytester.path / 'pytest.ini.template') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='',
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    monkeypatch.syspath_prepend(str(pytester.path))
    return pytester


def test_ini_options(tester: pytest.Pytester) -> None:  # noqa: WPS442
    """Ensure `auto_pytest_factoryboy` INI options are present in help text."""
    help_result = tester.runpytest('--help')

    plugin_ini_options_lines = [
        line
        for line in help_result.outlines
        if line.strip().startswith('auto_pytest_factoryboy_')
    ]
    assert len(plugin_ini_options_lines) == 2


def test_fixtures(  # noqa: WPS210, WPS231
    tester: pytest.Pytester,  # noqa: WPS442
) -> None:
    """Ensure proper `factoryboy` fixtures are created."""
    tester.makepyfile(
        factories='''
        import factory

        SOME_CONSTANT = 123


        class User(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age


        class NameableFactory(factory.Factory):
            name = factory.Faker('name')

            class Meta(object):
                abstract = True


        class UserFactory(NameableFactory):
            age = factory.Faker('random_int', min=1, max=100)

            class Meta(object):
                model = User


        class FemaleUserFactory(UserFactory):
            name = factory.Faker('name_female')


        class ChildUserFactory(NameableFactory):
            age = factory.Faker('random_int', min=1, max=17)

            class Meta(object):
                model = 'User'


        class NotFactoryForSure(object):
            pass

        not_factory_for_sure = NotFactoryForSure()
        ''',
    )
    expected_auto_pytest_factoryboy_fixtures = [
        'child_user_factory',
        'female_user_factory',
        'user',
        'user__age',
        'user__name',
        'user_factory',
    ]

    fixtures_result = tester.runpytest('--fixtures')

    auto_pytest_factoryboy_fixtures = []
    lines = list(fixtures_result.outlines)
    line = lines.pop(0) if lines else ''
    headers = ('functools', 'pytest_factoryboy')
    while lines and not any(header in line for header in headers):
        line = lines.pop(0)
    for line in lines:  # noqa: WPS440
        # start of the next section or end of the report
        if line.startswith('-') or line.startswith('='):
            break
        if line and not line.startswith(' '):
            auto_pytest_factoryboy_fixtures.append(line.partition(' ')[0])
    assert (
        sorted(auto_pytest_factoryboy_fixtures)
        == expected_auto_pytest_factoryboy_fixtures
    )
