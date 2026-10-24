# Markdown and Google Docs Synchronization

Guidelines for importing markdown files, handling LaTeX equations, and resolving
sync conflicts.

## Import Markdown

Use `mutate import-md` to convert any markdown file into a native Google Doc
with proper formatting (headings, bold, italic, links, lists, tables):

```bash
"$GDOCS" mutate import-md /path/to/report.md --title "Weekly Report"
```

To update an existing document instead of creating a new one, use the `--update`
flag:

```bash
"$GDOCS" mutate import-md /path/to/report.md --update DOC_ID
```

### Trade-offs: `import-md --update` vs. `sync`

When updating an existing document from a markdown file, choose the tool based
on your needs:

*   **Use `mutate import-md --update`** when you want **clean formatting**
    (native tables, lists, code blocks).
    *   *Warning*: This operation **overwrites the entire document** and
        **destroys all existing comments, suggestions, and anchors**.
*   **Use `mutate sync`** (see below) when you need to **preserve comments and
    collaborate**. It performs a 3-way merge to keep comments intact, but may
    occasionally introduce minor formatting artifacts (e.g., literal markdown
    characters).

> [!CAUTION] Every `mutate` command applies its changes to the live document
> immediately. There is no staged review step and no accept/reject safety net,
> so a destructive import cannot be undone from the CLI. Confirm with the user
> before overwriting a document that other people are working in, and see
> [metadata_retention.md](metadata_retention.md) for the pre-edit checks.

This is the simplest way to turn a local `.md` file into a shareable Google Doc.
The doc is created in your Drive root and the URL is printed on success. Combine
with `mutate share` to distribute:

```bash
DOC_ID=$("$GDOCS" mutate import-md /tmp/notes.md --title "Notes" --json | jq -r .documentId)
"$GDOCS" mutate share $DOC_ID --email team@example.com --role writer
```

## Hyperlinks in Markdown

When preparing markdown files for Google Docs import (`mutate import-md` or
`mutate sync`), format links to source files as web-accessible URLs rather than
local filesystem paths:

*   **Restricted `file:///` Usage:** `file:///` links should **ONLY** be used
    when the user explicitly requests local filesystem links. Never use
    `file:///` as the default protocol for markdown imported into Google Docs.
*   **Why:** Google Workspace web applications enforce strict browser security
    policies (Same-Origin Policy) that block `file://` URI schemes. If
    `file:///` links are imported into a Google Doc, clicking them in a browser
    will be blocked by the browser, rendering the links dead.

## Handling LaTeX Equations & Math Formulas

> [!IMPORTANT] The Google Docs API and Google Drive's native Markdown converter
> do NOT parse LaTeX delimiters (`$` / `$$`). Raw LaTeX formulas will survive
> the conversion only as literal unparsed text, with mangled underscores (`\_`)
> and broken table borders.

Adopt this two-track standard for any document containing math:

1.  **Inline Math & Table Headers:** Format using native Unicode typography
    (`v₁`, `v₂`, `Δv`, `T₀`, `ΔV`, `%`, `→`, `×`, `²`, `±`). Never use `$x$` in
    table cells or inline text.
2.  **Block / Display Equations:** Google Docs cannot typeset `$$...$$`,
    `\[...\]`, or `\begin{equation}`. Either rewrite the equation with Unicode
    typography, or render it to an image yourself and reference the local image
    file from the markdown — `import-md` and `sync` upload local images
    automatically (see "Automatic Image Uploads in Sync" below).

**Guardrails & validation:** `mutate import-md` and `mutate sync` automatically
scan markdown files for unrendered LaTeX math delimiters outside code blocks. If
detected:

-   A diagnostic warning is emitted to `stderr` with remediation steps.
-   Passing `--strict-math` causes `import-md` to fail immediately, preventing
    accidental publication of broken mathematical formatting.

## Handling Mermaid Diagrams

Drive's native Markdown converter does not turn Mermaid blocks (` ```mermaid `)
into images on import, so a Mermaid block passed through `import-md` lands in
the document as a literal code block.

See [`diagrams.md`](diagrams.md) for the supported diagram workflows, including
pre-rendering a diagram to an image and referencing it from the markdown.

## Handling Conflicts during Sync

When using `mutate sync` to synchronize a local markdown file with a Google Doc,
conflicts may occur if both the local file and the remote doc have changed since
the last sync.

By default, `mutate sync` will fail with an error listing the conflicts.

To handle conflicts, you can use the following flags:

*   **`--json-conflicts`**: Outputs conflicts as a JSON string prefixed with
    `CONFLICT_JSON:`, which is useful for programmatic parsing.

    ```bash
    "$GDOCS" mutate sync DOC_ID local_file.md --json-conflicts
    ```

*   **`--prefer-local`**: Automatically resolves conflicts by keeping the local
    changes and filtering out conflicting remote edits.

    ```bash
    "$GDOCS" mutate sync DOC_ID local_file.md --prefer-local
    ```

*   **`--local-base`**: Saves the local file content directly as the merge base,
    bypassing the translation of the remote Google Doc. This is useful when
    initializing sync on an existing document where the local file is known to
    be the correct baseline, or after a clean reset to avoid translation
    artifacts.

    ```bash
    "$GDOCS" mutate sync DOC_ID local_file.md --local-base
    ```

> [!IMPORTANT] **Never suggest overwriting or forcing a sync (by deleting the
> base file or using `--prefer-local`) without asking the user first!** If
> conflicts occur, you MUST present the differences to the user and ask them how
> they want to resolve them: 1. Keep Local changes (overwrites remote, e.g.,
> using `--prefer-local`). 2. Keep Remote changes (overwrites local). 3. Go
> through the differences together to manually merge. Always preserve the user's
> remote changes unless they explicitly tell you to discard them.

## Force Pushing and Resetting Document State

If you need to force-push local content to a Google Doc and ensure all
formatting (headings, lists, etc.) is correctly applied, do NOT use `mutate
write`. `mutate write` only writes raw text and bypasses the formatting logic,
which can lead to a document full of raw markdown syntax if a subsequent `mutate
sync` fails to detect changes.

Instead, follow this procedure to force-push and reset state:

1.  **Clear the document**: Use `"$GDOCS" mutate write DOC_ID --file
    <empty_file> --clear` to make the document empty or nearly empty.
2.  **Delete the base file**: Remove the corresponding `.base.md` file from the
    sync state directory (a `gdocs_sync/` directory under your agent's data
    directory).
3.  **Run sync**: Run `"$GDOCS" mutate sync DOC_ID local_file.md`. This will
    perform a 2-way sync and push all content as new elements with proper
    formatting.

> [!WARNING] Always ask the user for permission before performing a force-push
> or deleting base files, as this can overwrite remote changes.

## Marker-Scoped Synchronization (Body Mode)

You can restrict synchronization to a specific range within the document,
protecting the rest (like headers and footers) from being overwritten or
modified.

To enable this, pass the `--start-marker` and `--end-marker` options:

```bash
"$GDOCS" mutate sync DOC_ID local_file.md --start-marker "{{DOCUMENT_BODY}}" --end-marker "{{END_DOCUMENT_BODY}}"
```

*   **Behavior**: Diffs and syncs only the content located strictly between the
    two markers in both the remote GDoc and the local file.
*   **Safety**: If markers are not found or are found in the wrong order, the
    tool will report an error to prevent accidental full sync overwrites of
    protected zones.

## Tab-Scoped Synchronization

You can synchronize a local markdown file to a specific tab inside a Google Doc
using the `--tab` option:

```bash
"$GDOCS" mutate sync DOC_ID local_file.md --tab TAB_ID
```

This ensures that the sync operations (merging, inserting, and deleting blocks)
only target the specified tab, preventing accidental edits to other tabs.

## Automatic Image Uploads in Sync

When you run `mutate sync`, the tool automatically parses the local markdown
file for local image references (e.g. `![diagram](images/diagram.png)`).

Before performing the sync, it:

1.  Uploads the images securely to Drive (into a temporary folder or parent
    folder).
2.  Replaces the local path references in the markdown content with public Drive
    content URIs.

This ensures that images are properly rendered as inline images in the Google
Doc without requiring manual uploads first.

> [!IMPORTANT]
>
> **SVG is not supported.** Image uploads fail on `.svg` with `SVG conversion is
> not available; convert the image to PNG or JPEG first`. This applies
> everywhere images are uploaded — `mutate sync`, `mutate import-md`, `mutate
> insert-image-from-file`, and the `insert-image-from-file` batch operation.
> Convert diagrams to PNG before referencing them, and note that some diagram
> renderers emit SVG by default. See [diagrams.md](diagrams.md).

## Code Block Syntax Highlighting in Sync

The `mutate sync` command automatically applies syntax highlighting (token-level
coloring and font styles like bold/italic) to fenced code blocks in Google Docs.

Supported language tags include:

*   **C / C++**: `cpp`, `c++`, `c`
*   **Protocol Buffers**: `proto`, `prototext`, `protobuf`
*   **JSON**: `json`
*   **Shell / Bash**: `shell`, `sh`, `bash`
*   **Python**: `python`, `py`
*   **Go**: `go`, `golang`

## Diagrams in Sync

The `mutate sync` command also supports automatic rendering of code-based
diagrams (Mermaid, DOT, and Sequence Diagrams) found in the local Markdown file.
See [diagrams.md](diagrams.md) for more details.
