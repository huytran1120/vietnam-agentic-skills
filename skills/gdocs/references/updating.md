# Updating Existing Google Docs

The update commands let you modify existing documents without rebuilding from
scratch.

## Recommended Workflow

1.  **Inspect** — use `readonly structure` to see numbered paragraphs and
    headings.
2.  **Edit** — use `mutate sed` for text changes, `mutate batch` for styled
    content.
3.  **Verify** — use `readonly read` or `readonly export` to check results.

> [!IMPORTANT] Every `mutate` command applies to the live document
> **immediately** — nothing is staged for review and there is no accept/reject
> step, so an unwanted edit has to be undone by another edit. Preview risky text
> changes with `"$GDOCS" mutate sed DOC_ID 's/old/new/' --dry-run` before
> running them for real.

## Common Workflows

```bash
"$GDOCS" readonly structure DOC_ID
"$GDOCS" mutate sed DOC_ID 's/Draft/Final/g'

"$GDOCS" mutate batch DOC_ID -f new_status.json --after "## Status" --before "## Design"

"$GDOCS" mutate update-table DOC_ID --headers "Metric,Target,Current" --data-file metrics.json

"$GDOCS" mutate batch DOC_ID -f full_doc.json --replace-all
```

> [!TIP] Use `readonly structure --json` to get exact character indices for each
> element. The `mutate batch` command handles the delete+insert dance
> automatically — you only need to specify heading text with `--after` and
> `--before`.

> [!TIP] **Targeted Batch Formatting**: Use `"op": "style-text"` inside batch
> JSON files to search for a specific string and style it (change color, bold,
> or add an internal heading/bookmark link) natively in-place without modifying
> the surrounding paragraph text.

> [!IMPORTANT] **Structural edits (adding/removing paragraphs):** Use sed
> `Na\text` (append after paragraph N) or `Ni\text` (insert before paragraph N)
> to add new paragraphs — not `s/old/old\nnew/` which creates literal `\n` text.
> Use `readonly structure` first to find the right paragraph numbers. These
> commands work with TABLE paragraphs too (the CLI automatically adjusts the
> insertion index for tables).

> [!IMPORTANT] **`readonly structure` vs `read --json` — choosing the right
> tool:** `readonly structure` (and `structure -v`) gives a quick numbered
> overview of paragraphs, headings, and tables — use it for orientation and
> finding paragraph numbers. For **precise information** (bullet/list
> properties, inline object IDs, exact formatting, paragraph style details), use
> `readonly read DOC_ID --json` and parse the JSON output. The raw JSON contains
> everything the API returns: bullet configs, named styles, indent levels,
> inline images with object IDs, etc.

> [!TIP] **Filling empty table cells:** Use `s/|T.R.C|/new text/` to write into
> empty cells (e.g. after `mutate add-row`). The CLI inserts text at the cell
> start position even when the cell contains only a newline.

> [!TIP] **Targeted Paragraph Formatting Workaround:** Because the Google Docs
> API does not support direct formatting of a paragraph by index range, use the
> sequential **unique-prefix workaround** in batch JSON files to style specific
> paragraphs cleanly: 1. **Insert prefix**: Use `{"op": "insert", "start":
> <startIndex>, "text": "[temp-N] "}`. 2. **Style text**: Use `{"op":
> "style-text", "find": "[temp-N]"}` with your styling fields (e.g.,
> `"indent_start": 90.0`, `"indent_first_line": 72.0`). 3. **Delete prefix**:
> Use `{"op": "delete-range", "start": <startIndex>, "end": <startIndex> +
> len(prefix)}`.
>
> Always execute these operations **one paragraph at a time** (sequentially) to
> prevent index-shift drift between insertions and deletions.

## Replacing Images

There are three ways to replace images in a Google Doc, depending on
bounding-box requirements:

1.  **Safe Atomic Replacement by ID (`mutate replace-image-safe`)**:

    *   **Behavior**: Deletes the old image and inserts the new image at the
        exact character index. This resets the bounding box to match the natural
        dimensions and aspect ratio of the new image.

2.  **Replace by Object ID (`mutate replace-image-from-file` or
    `replace-image`)**:

    *   **Behavior**: Replaces the image content but retains the existing
        bounding box of the original image using the API's `CENTER_CROP`
        mechanism. If the aspect ratio differs, the image is cropped to fit the
        original bounding box.

3.  **Manual Replace by Index (`mutate insert-image-from-file --replace --index
    N` or `insert-image --replace`)**:

    *   **Behavior**: Deletes the element exactly at index `N` and inserts the
        new image at the same position. Requires pre-calculating the exact
        character index.

## Externally Created Documents

When modifying documents that were created outside your own Workspace domain
(such as external collaborators or third-party organizations):

-   **Google Docs API Restrictions**: The Google Docs API does not support
    native anchored comments across external domain boundaries, so `mutate
    add-comment --quote` may fail on a document owned by another organization.
-   **Preemptive Recognition**: Check document ownership before attempting
    anchored comments — the **gdrive** skill's `readonly info` reports the owner
    of a file ID. The gdrive skill comes from the **Google Drive** plugin; if it
    isn't installed, skip this check or ask the user to install it.
-   **Applying Changes**: Ordinary edits still work. `mutate replace DOC_ID
    "old" "new"`, `mutate append DOC_ID "text"`, and `mutate sed` all write
    directly to the document as long as the signed-in account has edit access.
-   **Alternatives**: When encountering an externally created document where the
    user wants comments, report this situation preemptively and provide the
    alternatives:
    1.  Create a copy of the document in your own Drive with the **gdrive**
        skill's `mutate copy` (needs the Google Drive plugin). The copy enables
        native anchored comments.
    2.  Use unanchored comments (`"$GDOCS" mutate add-comment DOC_ID "comment
        text"` without `--quote`, or with `--native=false`).
    3.  Edit the document directly with `mutate replace` or `mutate sed`, and
        summarize the changes for the user afterwards.
    4.  Create a separate review document or output listing the problems
        (`"$GDOCS" mutate create` or `"$GDOCS" mutate import-md`).

## High-Fidelity Structured Formatting (Resumes & Technical Briefs)

For complex documents with deep bullet hierarchies, numbered sub-stages, and
rich metadata links (such as resumes, incident summaries, or architecture
briefs):

-   **Markdown Importer Behavior:** Tools like `mutate import-md` or `mutate
    sync` may flatten nested bullet lists or drop indentation distinctions when
    converting mixed markdown (e.g., numbered steps nested under disc bullets).
-   **Atomic Transactional Pattern:** For exact layout control, use an atomic
    REST API batch payload (`mutate batch` or direct REST `batchUpdate`) with:
    1.  `deleteContentRange` to clear existing body or tab content.
    2.  `insertText` at index 1 with all body prose, headings, and tab-prefixed
        sub-bullets (`\t`).
    3.  `createParagraphBullets` applied per list group with cumulative tab
        offset tracking (see [batch_operations.md](batch_operations.md)).
    4.  `updateParagraphStyle` for heading styles, line spacing (`115`), and
        space above/below.
    5.  `updateTextStyle` for color (`#1a73e8` for headings), bolding run-in
        prefixes, and embedding clickable links.
