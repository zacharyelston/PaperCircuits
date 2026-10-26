from pathlib import Path

import pytest

import build


def test_registry_is_unique_and_ordered():
    build.validate_registry()
    assert build.SHEETS[0].filename == "template.pdf"
    assert build.SHEETS[-1].filename == "M7-output.pdf"


def test_registry_rejects_duplicate_and_invalid_names():
    sheet = build.SheetSpec("one.pdf", "template")
    with pytest.raises(ValueError, match="duplicate sheet output names: one.pdf"):
        build.validate_registry((sheet, sheet))
    with pytest.raises(ValueError, match="invalid sheet output name"):
        build.SheetSpec("nested/one.pdf", "template")


def test_registry_requires_callable_builder():
    with pytest.raises(ModuleNotFoundError, match="registered sheet module does not exist"):
        _ = build.SheetSpec("one.pdf", "shared").build


def test_every_registered_sheet_imports_with_a_builder():
    assert all(callable(sheet.build) for sheet in build.SHEETS)


def test_real_full_build_smoke(tmp_path):
    build.generate_pdfs(tmp_path)
    assert {path.name for path in tmp_path.glob("*.pdf")} == {sheet.filename for sheet in build.SHEETS}
    assert all((tmp_path / sheet.filename).stat().st_size > 0 for sheet in build.SHEETS)


def test_compare_pdfs_reports_missing_extra_and_changed(tmp_path):
    generated, committed = tmp_path / "generated", tmp_path / "committed"
    generated.mkdir()
    committed.mkdir()
    for sheet in build.SHEETS:
        (generated / sheet.filename).write_bytes(b"same")
        (committed / sheet.filename).write_bytes(b"same")
    assert build.compare_pdfs(generated, committed) == []

    (committed / build.SHEETS[0].filename).write_bytes(b"changed")
    (committed / build.SHEETS[1].filename).unlink()
    (committed / "extra.pdf").write_bytes(b"extra")
    assert build.compare_pdfs(generated, committed) == [
        f"missing committed PDF: {build.SHEETS[1].filename}",
        "unexpected committed PDF: extra.pdf",
        f"committed PDF differs: {build.SHEETS[0].filename}",
    ]


def test_preview_problems_handles_missing_malformed_and_stale(tmp_path):
    out, fingerprints = tmp_path / "out", tmp_path / "previews.sha256"
    out.mkdir()
    for sheet in build.SHEETS:
        (out / sheet.filename).write_bytes(sheet.filename.encode())
    assert build.preview_problems(out, fingerprints) == ["preview fingerprint file is missing"]

    fingerprints.write_text("bad line\n")
    assert build.preview_problems(out, fingerprints) == ["malformed preview fingerprint on line 1"]

    build.write_fingerprints(out, fingerprints)
    assert build.preview_problems(out, fingerprints) == []
    (out / build.SHEETS[0].filename).write_bytes(b"changed")
    assert build.preview_problems(out, fingerprints) == [f"preview is stale or unrecorded: {build.SHEETS[0].filename}"]


def test_render_previews_reports_missing_tool(monkeypatch, tmp_path):
    monkeypatch.setattr(build.shutil, "which", lambda _name: None)
    assert build.render_previews(tmp_path / "out", tmp_path / "previews") is False


def test_unknown_option_is_rejected(capsys):
    assert build.main(["--unknown"]) == 2
    assert "Unknown option" in capsys.readouterr().out


def test_phase_options_are_validated(capsys):
    assert build.main(["--check", "--phase=pdfs"]) == 2
    assert build.main(["--phase=unknown"]) == 2
    assert "--phase" in capsys.readouterr().out


def test_missing_composite_preview_is_actionable(tmp_path):
    with pytest.raises(FileNotFoundError, match="hero.png; missing previews"):
        build.hero(previews=tmp_path)


def test_publish_files_replaces_only_staged_outputs(tmp_path):
    source, destination = tmp_path / "source", tmp_path / "destination"
    source.mkdir()
    destination.mkdir()
    (source / "changed.txt").write_text("new")
    (destination / "changed.txt").write_text("old")
    (destination / "kept.txt").write_text("kept")
    build.publish_files(source, destination)
    assert (destination / "changed.txt").read_text() == "new"
    assert (destination / "kept.txt").read_text() == "kept"
    assert not (destination / ".changed.txt.tmp").exists()


def test_update_orchestrates_full_build_before_publish(monkeypatch, tmp_path):
    calls = []

    def generate(out):
        calls.append("pdfs")
        out.mkdir(parents=True)
        (out / "one.pdf").write_bytes(b"pdf")

    def render(out, previews, executable=None):
        assert (out / "one.pdf").exists()
        calls.append("previews")
        previews.mkdir(parents=True)
        (previews / "one.png").write_bytes(b"png")
        return True

    def fingerprints(out, path):
        calls.append("fingerprints")
        path.write_text("hash")

    def composites(previews):
        assert (previews / "one.png").exists()
        calls.append("composites")
        (previews / "hero.png").write_bytes(b"hero")

    monkeypatch.setattr(build, "generate_pdfs", generate)
    monkeypatch.setattr(build, "render_previews", render)
    monkeypatch.setattr(build, "write_fingerprints", fingerprints)
    monkeypatch.setattr(build, "compose_images", composites)
    monkeypatch.setattr(build, "OUT", tmp_path / "out")
    monkeypatch.setattr(build, "PREVIEWS", tmp_path / "img")
    assert build.update_artifacts() == 0
    assert calls == ["pdfs", "previews", "fingerprints", "composites"]
    assert (tmp_path / "out/one.pdf").exists()
    assert (tmp_path / "img/hero.png").exists()


def test_failed_phase_publishes_nothing(monkeypatch, tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "old.pdf").write_bytes(b"old")

    def generate(staged):
        staged.mkdir(parents=True)
        (staged / "new.pdf").write_bytes(b"new")

    def fail(*_args, **_kwargs):
        raise RuntimeError("render failed")

    monkeypatch.setattr(build, "generate_pdfs", generate)
    monkeypatch.setattr(build, "render_previews", fail)
    monkeypatch.setattr(build, "OUT", out)
    with pytest.raises(RuntimeError, match="render failed"):
        build.update_artifacts()
    assert {path.name for path in out.iterdir()} == {"old.pdf"}


def snapshot_tree(root: Path):
    return {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def test_verify_artifacts_does_not_modify_committed_directories(monkeypatch, tmp_path):
    out, previews = tmp_path / "out", tmp_path / "img"
    out.mkdir()
    previews.mkdir()
    for sheet in build.SHEETS:
        (out / sheet.filename).write_bytes(sheet.filename.encode())
    fingerprints = previews / "previews.sha256"
    build.write_fingerprints(out, fingerprints)
    before = snapshot_tree(tmp_path)

    def fake_generate(destination):
        destination.mkdir(parents=True, exist_ok=True)
        for sheet in build.SHEETS:
            (destination / sheet.filename).write_bytes(sheet.filename.encode())

    monkeypatch.setattr(build, "OUT", out)
    monkeypatch.setattr(build, "FINGERPRINTS", fingerprints)
    monkeypatch.setattr(build, "generate_pdfs", fake_generate)
    assert build.verify_artifacts() == 0
    assert snapshot_tree(tmp_path) == before
