from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()

pytest_plugins = [
    "tests.fixtures.app",
    "tests.fixtures.db",
    "tests.fixtures.session",
    "tests.fixtures.fakers.people",
    "tests.fixtures.fakers.police_officers",
    "tests.fixtures.fakers.vehicles",
    "tests.fixtures.fakers.traffic_violations"
]
