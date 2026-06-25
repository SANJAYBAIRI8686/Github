from app.services.ignore_rules import should_skip_path


def test_ignore_rules_skip_noise_paths() -> None:
    assert should_skip_path("node_modules/pkg/index.js")
    assert should_skip_path("dist/bundle.js")
    assert should_skip_path("assets/image.png")
    assert not should_skip_path("src/app.py")