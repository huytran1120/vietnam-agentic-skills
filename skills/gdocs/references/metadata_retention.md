# Metadata & Interactive Entity Retention in Google Docs

When updating collaborative documents that contain stakeholder feedback (such as
comments or suggestions) or interactive Smart Canvas elements (such as user
chips, dropdowns, or date chips), you must take precautions to avoid destroying
document indices, wiping interactive widgets, and orphaning comment anchors.

> [!CAUTION] Every `mutate` command writes to the live document immediately.
> Edits are not staged for review and there is no accept/reject step, so a
> destructive edit cannot be rolled back from the CLI. This makes the detection
> and backup steps below mandatory rather than optional.

## The Anchor Index & Interactive Entity Wipe Problem

> [!CAUTION] **Full-document replacement destroys comment anchors and
> interactive widgets.** Using `--replace-all` (in `batch`, `import-md
> --update`, or `write`) clears all document AST indices, which: 1. Orphans
> existing comment and suggestion anchors to the sidebar. 2. Permanently
> destroys interactive Smart Canvas widgets, such as user chips and dropdowns,
> replacing them with broken static text or deleting them. There is no automated
> way to re-link orphaned comments or restore destroyed interactive widgets from
> markdown.

## Detection and Automatic Safe Mode Fallback Protocol

Before performing any edit on an existing Google Doc:

1.  **Inspect for Interactive Entities**:

    -   Check for active feedback: run `readonly list-comments DOC_ID --json`
        and inspect the document AST with `readonly read DOC_ID --json`.
    -   Check for Smart Canvas chips: inspect `textRun` and paragraph elements
        in that same AST dump.

2.  **Automatic Granular Safe Mode**: If ANY interactive entity or collaborative
    metadata is detected:

    -   **DO NOT** use `mutate import-md --update` or `mutate batch
        --replace-all`.
    -   **DO** use granular operations:
        -   `mutate update-table`: For updating data rows in existing tables.
        -   `mutate replace` / `mutate sed`: For targeted text and link updates.
        -   `mutate batch` with `--after` and `--before`: For section-level
            updates.
        -   `mutate create-tab` + `mutate import-md --tab TAB_ID`: For large
            section rewrites, isolating the new content on a separate tab while
            leaving the original tab and its comment anchors intact.

## Best Practices for Metadata Retention

1.  **Switch to Granular Updates**: As soon as a document has stakeholder
    feedback or interactive widgets, stop using `--replace-all`. Use
    `update-table`, `sed`, `replace`, and `format-text` instead.
2.  **Section-Level Updates**: Use `batch` with `--after` and `--before` to
    replace a specific section without wiping the rest of the document. This
    preserves anchors in other parts of the doc.
3.  **Mandatory Backup of Comments**: Before performing any structural or
    high-risk edit, you MUST run a backup to your local workspace using a
    parameterized filename to avoid overwriting other document backups:

```bash
"$GDOCS" readonly list-comments DOC_ID --json > /tmp/comments_backup_DOC_ID.json
```

> [!IMPORTANT] **PII Cleanup Requirement:** Because document comments contain
> user names and email addresses (PII), this backup file **MUST** be deleted
> immediately once your edits are successfully verified and the backup is no
> longer needed:
>
> ```bash
> rm /tmp/comments_backup_DOC_ID.json
> ```

*Note: Backups are mandatory for structural edits (adding/deleting paragraphs or
section batching) but can be safely skipped for minor point-wise text
replacements (e.g., unique `replace` or narrow `sed`) to maximize velocity.*

If anchors are accidentally broken, you can add replies to the orphaned comments
referencing their original `quotedFileContent` from the temporary backup.

## Formatting Caveats

Standard `batch` operations do not parse markdown symbols (e.g., `**`). To
restore formatting after a batch update, use:

-   `"$GDOCS" mutate sed --bold`
-   `"$GDOCS" mutate format-text --bold`

## Collaborative Review Protocol ("Ask First")

Before performing any non-append structural edit, you MUST check for active
feedback by running:

```bash
"$GDOCS" readonly list-comments DOC_ID --json
"$GDOCS" readonly read DOC_ID --json
```

> [!IMPORTANT] **State Detection Rules:**
>
> -   **Comments**: Check if any comments are **unresolved** (`"resolved":
>     false` or `Status: open`). Ignore resolved comments.
> -   **Suggestions**: You MUST parse the JSON output of `readonly read DOC_ID
>     --json` and search the AST for suggestion markers (e.g.,
>     `suggestedInsertionIds` or `suggestedDeletionIds`). Plain text output does
>     not flag suggestions left by human collaborators.

### **Active-Range Isolation (Velocity Optimization)**

If unresolved comments or suggestions exist in the document, you are **permitted
to execute targeted edits without halting to consult the user, provided that:**

1.  Your proposed edit is narrow and range-scoped (using `--after`/`--before`
    boundaries or paragraph-addressed `sed` edits).
2.  You match the character indices of the active comments against the target
    section's paragraph indices (using `structure --json`).
3.  You verify that the specific target section is **100% free of unresolved
    comments or suggestions**.

If the target section itself contains active feedback, or if you are performing
a sweeping full-document edit, you **MUST NOT** proceed in-place. Stop and
present the user with the following choices:

1.  **New Tab Isolation (Recommended for Broad Edits)**: Create a new tab and
    place all proposed updates there, leaving the main review tab completely
    untouched. Recommend this for large structural changes or multi-section
    rewrites (>= 3 paragraphs) to keep the main doc readable. *Note: The
    `create-tab` command only creates the tab outline. You MUST note the
    returned new `TAB_ID` and pass it to all subsequent write operations.*

```bash
# 1. Create the tab
"$GDOCS" mutate create-tab DOC_ID --title "Proposed Updates"
# 2. Write content to that specific tab using --tab
"$GDOCS" mutate batch DOC_ID -f updates.json --tab TAB_ID
# 3. Clean up the PII comment backup once verified
rm /tmp/comments_backup_DOC_ID.json
```

2.  **Granular Additions with Strikethrough (Recommended for Narrow Edits)**:
    Append the proposed revision directly below the original paragraph, and
    strike through the old text to mark it for deletion. Recommend this for
    point-wise wording or spelling fixes (< 3 paragraphs) to minimize
    tab-switching. *Note: You MUST run `structure` first to discover the correct
    paragraph index.*

```bash
# 1. Discover paragraph numbers
"$GDOCS" readonly structure DOC_ID
# 2. Append the new proposed text directly after the paragraph index
#    (e.g., index 3)
"$GDOCS" mutate sed DOC_ID '3a\PROPOSED REVISION: ...'
# 3. Strike out the original paragraph (index 3) to mark it for deletion
"$GDOCS" mutate format-text DOC_ID --strikethrough --text "Original paragraph text..."
# 4. Clean up the PII comment backup once verified
rm /tmp/comments_backup_DOC_ID.json
```

3.  **In-Place Non-Destructive Batches**: Modify only the narrow ranges of text
    using batched replacements target-scoped with `--after` and `--before`. >
    [!WARNING] > **Replacing a targeted range will still orphan and destroy
    any > comments/suggestions located *inside* that specific section.** You >
    must verify the target section is completely clear of active >
    comments/suggestions before executing this.
