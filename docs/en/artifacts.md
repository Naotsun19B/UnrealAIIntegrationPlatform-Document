**[日本語](../ja/artifacts.md)** | [Back to README](../../README.md)

# Artifacts

Every UAIP command returns **artifacts** — output files such as PNG screenshots, JSON state dumps, logs, and reports. Artifacts allow the AI to verify editor state without asking the user.

---

## Artifact types

| Type | Extension | Typical content |
|---|---|---|
| `Image` | `.png` | Screenshots of viewport, editor tab, or active window |
| `Json` | `.json` | State dumps (world, editor, actor, Slate tree), command responses |
| `Log` | `.log` / `.txt` | OutputLog / MessageLog dumps |
| `Report` | `.json` | Automation test results |
| `Bundle` | archive | Several artifacts grouped (e.g. `CheckpointCapture`) |

---

## Where artifacts live

```
Saved/UAIP/<SessionId>/
  Dumps/        ← JSON dumps
  Screenshots/  ← PNG captures
  Logs/         ← log files
  Reports/      ← test reports
```

Artifacts are stored per session. When a session ends, artifacts become GC candidates.

---

## Reading artifacts

### From `uaip_execute`

```json
{
  "Success": true,
  "Artifacts": [
    {
      "ArtifactId": "8D1403DB4896B4742E423CBD9F535F19",
      "FilePath": "MCP-Anonymous-.../Screenshots/capture.png",
      "Type": "Image"
    }
  ]
}
```

### From `uaip_run_scenario`

```json
{
  "StepResults": [
    { "StepName": "Cap", "ArtifactIds": ["8D1403DB..."] }
  ],
  "ArtifactIds": ["8D1403DB..."]
}
```

Scenarios return only artifact **ids**, not file paths. Use the id to fetch the file.

---

## Automatic inlining

The MCP Bridge may inline small artifacts directly in the response under `_inlined_artifacts`:

```json
{
  "_inlined_artifacts": [
    {
      "artifact_id": "...",
      "content_type": "application/json",
      "data_base64": "..."
    }
  ]
}
```

Default inline policy:

| Type | Inlined by default |
|---|---|
| `Image` (PNG) | **No** — PNG accumulates across sessions and can exceed token limits |
| `Json` | Yes |
| `Text` | Yes |

To view a PNG screenshot, use the `Read` tool with the file path — do not rely on inlining for images.

---

## Artifacts by command

| Command | Artifact |
|---|---|
| `CaptureActiveWindowImage` | One PNG — active editor window |
| `CaptureViewportImage` | One PNG — PIE / game viewport |
| `CaptureEditorTabImage` | One PNG — specific editor tab |
| `CaptureGraphViewportImage` | One PNG — graph editor (Blueprint, Material, …) |
| `CaptureCanonicalGraphImage` | One PNG — full-graph layout (requires a registered external capture provider) |
| `DumpEditorState` | One JSON — open assets, active tab, window dimensions |
| `DumpWorldState` | One JSON — all actors, components, transforms (can be large) |
| `DumpSlateTree` | One JSON — Slate widget tree |
| `CheckpointCapture` | PNG + JSON bundled together |
| `LoadMap` / `StartPIE` | Two JSONs — before/after state |

---

## Best practices

- **Check artifact count and type first**, then fetch only what you need
- **Large JSON dumps**: do not load the whole file into context — use `grep` / `jq` to extract the relevant slice
- **PNG screenshots**: display one at a time with the `Read` tool; describe what you see rather than writing the path in prose
- **Self-verify before asking the user**: capture a screenshot or dump JSON state to answer factual questions without a human round-trip
  - Active editor state → `CaptureActiveWindowImage`
  - Viewport / PIE → `CaptureViewportImage`
  - Graph editor → `CaptureGraphViewportImage`
  - World actors → `DumpWorldState`
  - Slate widget tree → `DumpSlateTree`

---

## Handling large artifacts

When a response exceeds the token cap, the bridge saves the content to a `.txt` file and returns a notice:

```
Output has been saved to <path>.txt.
Use offset and limit parameters to read specific portions...
```

Use the `Read` tool with `offset` and `limit` parameters to page through large files.
