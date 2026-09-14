#!/usr/bin/env python3
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "exp01_sequential_random_adaptive_1lsb", "exp02_payload_size_vs_quality",
    "exp03_compression_before_embedding", "exp04_encryption_and_compression",
    "exp05_robustness_transformations", "exp06_lsb_depth_study",
    "exp07_container_content_sensitivity", "exp08_adaptive_parameter_study",
    "exp09a_capacity_limits", "exp09b_literary_payloads", "exp10_basic_steganalysis",
    "exp11_rs_analysis", "exp12_rs_embedding_rate_estimation", "exp13_rs_generalization",
    "exp14_cross_container_rs_estimator", "exp15_hybrid_steganalysis",
]


def verify_manifest(path: Path) -> None:
    for line in path.read_text().splitlines():
        expected, relative = line.split(None, 1)
        target = ROOT / relative.strip()
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected: raise AssertionError(f"Checksum mismatch: {relative}")


def main() -> None:
    standard = ROOT / "experiments" / "standard"
    for name in EXPECTED:
        directory = standard / name
        assert directory.is_dir(), f"Missing experiment: {name}"
        readme = directory / "README.md"
        assert readme.is_file() and readme.stat().st_size, f"Missing/empty README: {name}"
        assert list(directory.glob("results/metrics/*.csv")), f"Missing metrics CSV: {name}"
    assert (ROOT / "data/images/input2.png").is_file()
    assert (ROOT / "data/payload/text.txt").is_file()
    project_files = [*standard.rglob("*.py"), *ROOT.glob("src/**/*.py"), *ROOT.glob("tests/**/*.py")]
    text = "\n".join(path.read_text() for path in project_files)
    assert "sys.path.insert" not in text, "Repository-internal sys.path manipulation remains"
    assert "/" + "Users/" not in text, "Private absolute path remains"
    assert "exp09" + "_capacity_limits" not in text, "Stale Exp09A directory name remains"
    assert not list(ROOT.rglob(".DS_Store")), ".DS_Store remains in project tree"
    readme_text = (ROOT / "README.md").read_text()
    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", readme_text):
        if "://" not in link and not (ROOT / link.split("#", 1)[0]).exists():
            raise AssertionError(f"Broken README link: {link}")
    verify_manifest(ROOT / "checksums/research-inputs.sha256")
    verify_manifest(ROOT / "checksums/result-metrics.sha256")
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
