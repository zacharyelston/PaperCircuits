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
    with pytest.raises(TypeError, match="has no callable build"):
        _ = build.SheetSpec("one.pdf", "shared").build


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
