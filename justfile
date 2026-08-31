set shell := ["bash", "-euo", "pipefail", "-c"]

default: build

# Sync deps and render every source into out/ (the renderer validates its
# outputs: transparency, content, chroma).
build:
    uv sync
    uv run python tools/render.py

# The render gate is the test gate.
test: build
    @echo "all sources rendered and validated"

# Demos repo — no binary, no launcher (ADR-749: nothing to install).
install:
    @echo "diagram-layout-demos: demos repo, nothing to install"

# Remove generated images.
clean:
    rm -rf out
    mkdir -p out
    touch out/.gitkeep

# Rebuild gallery.html from catalog.json, README.md and the artifacts in out/.
gallery:
    python3 tools/gallery.py
