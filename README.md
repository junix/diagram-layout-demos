# Diagram Layout Demos

Automatic layout as a rendering capability across twelve reference scenarios: Graphviz handles clustered, radial, free-form, state, lineage, and DAG topology; D2 handles modern semantic diagram DSLs.

`catalog.json` records the use case, question, diagram family, complexity, and engine-oriented tags.

| Architecture | Knowledge | Incident | Data lineage |
|---|---|---|---|
| ![architecture](out/architecture-transparent.png) | ![knowledge](out/knowledge-transparent.png) | ![incident](out/incident-transparent.png) | ![data lineage](out/data-lineage-transparent.png) |
| State machine | Radial ontology | Build pipeline | Sequence |
| ![state machine](out/state-machine-transparent.png) | ![radial ontology](out/radial-ontology-transparent.png) | ![build pipeline](out/build-pipeline-transparent.png) | ![sequence](out/sequence-transparent.png) |
| Platform | Decision | Ownership | Event storm |
| ![platform](out/platform-transparent.png) | ![decision](out/decision-transparent.png) | ![ownership](out/ownership-transparent.png) | ![event storm](out/event-storm-transparent.png) |

```bash
uv sync
uv run python tools/render.py
```

The renderer checks all external binaries, compiles DSL source to SVG, rasterizes with a transparent background, and rejects PNGs without meaningful alpha, content, and color.
