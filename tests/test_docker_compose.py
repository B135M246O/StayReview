from pathlib import Path


def test_compose_builds_local_backend_and_persists_database():
    root = Path(__file__).parents[1]
    compose = (root / 'infra/docker-compose.yaml').read_text(encoding='utf-8')
    assert 'image: postgres:' in compose
    assert 'build: ../api_yamdb' in compose
    assert 'postgres_data:/var/lib/postgresql/data' in compose
    assert '8002:80' in compose
    images = [line.split('image:', 1)[1].strip() for line in compose.splitlines()
              if line.strip().startswith('image:')]
    assert all(image.startswith(('postgres:', 'nginx:')) for image in images)
