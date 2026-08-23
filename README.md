# Diagram Layout Demos

Automatic layout as a rendering capability: Graphviz handles clustered and free-form graph topology; D2 handles a modern incident-response flow DSL.

| Scene | Preview | Engine |
|---|---|---|
| Ocean observatory | ![architecture](out/architecture-transparent.png) | Graphviz `dot` |
| Living-systems field | ![knowledge](out/knowledge-transparent.png) | Graphviz `neato` |
| Incident response | ![incident](out/incident-transparent.png) | D2 `dagre` |

```bash
uv sync
uv run python scripts/render.py
```

The renderer checks all external binaries, compiles DSL source to SVG, rasterizes with a transparent background, and rejects PNGs without meaningful alpha, content, and color.
