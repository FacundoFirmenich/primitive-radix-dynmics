"""Check tracked paths and byte signatures for the manuscript embargo."""

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BLOCKED_DIRECTORIES = {"paper", "papers", "manuscript", "manuscripts", "supplement", "supplements", "private-paper", "private-manuscript"}


def main():
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    prohibited = []
    for name in filter(None, files):
        relative = Path(name)
        path = ROOT / relative
        if path.is_symlink() or set(part.lower() for part in relative.parts[:-1]) & BLOCKED_DIRECTORIES:
            prohibited.append(name)
            continue
        with path.open("rb") as stream:
            signature = stream.read(8)
        is_figure = relative.parent == Path("outputs/figures") and relative.stem in {
            "fig01_object_architecture", "fig02_sharp_threshold", "fig03_counterfamily_graph",
            "fig04_spectral_cycle", "graphical_abstract",
        }
        if relative.suffix.lower() == ".tex" or signature.startswith(b"PK\x03\x04") or (signature.startswith(b"%PDF-") and not is_figure):
            prohibited.append(name)
    if prohibited:
        raise SystemExit("Publication boundary violation: " + ", ".join(prohibited))
    print("Tracked public files checked:", sum(bool(name) for name in files))


if __name__ == "__main__":
    main()
