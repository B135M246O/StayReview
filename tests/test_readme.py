from pathlib import Path


def test_readme_has_local_launch_and_attribution():
    readme = (Path(__file__).parents[1] / 'README.md').read_text(encoding='utf-8')
    assert 'StayReview' in readme
    assert 'Автор адаптации и доработок — Рябуха Олег' in readme
    assert 'manage.py migrate' in readme
    assert '8002' in readme
