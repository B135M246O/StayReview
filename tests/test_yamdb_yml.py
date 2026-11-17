from pathlib import Path


def test_ci_runs_checks_without_deployment():
    root = Path(__file__).parents[1]
    active = (root / '.github/workflows/yamdb_workflow.yml').read_text(encoding='utf-8')
    copy = (root / 'yamdb_workflow.yml').read_text(encoding='utf-8')
    assert active == copy
    assert 'python -m pytest' in active
    assert 'makemigrations --check' in active
    assert 'ssh-action' not in active
    assert 'telegram-action' not in active
    assert 'push: true' not in active
    assert 'DOCKER_PASSWORD' not in active
