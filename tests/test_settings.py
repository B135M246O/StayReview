import os
from pathlib import Path
import subprocess
import sys


def test_configurable_local_database_backends():
    project = Path(__file__).parents[1] / 'api_yamdb'
    for engine in ['django.db.backends.postgresql', 'django.db.backends.sqlite3']:
        env = os.environ.copy()
        env.update({
            'DJANGO_SETTINGS_MODULE': 'api_yamdb.settings',
            'DB_ENGINE': engine,
            'DB_NAME': ':memory:' if engine.endswith('sqlite3') else 'stayreview',
            'DEBUG': 'false',
            'ALLOWED_HOSTS': 'localhost,127.0.0.1',
        })
        check = (
            'from django.conf import settings; '
            f'assert settings.DATABASES["default"]["ENGINE"] == {engine!r}; '
            'assert not settings.DEBUG; '
            'assert "*" not in settings.ALLOWED_HOSTS'
        )
        result = subprocess.run([sys.executable, '-c', check], cwd=project,
                                env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
