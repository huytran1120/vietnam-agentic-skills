# Working with Tabs in Google Docs

Many Google Docs have multiple tabs. The `--tab TAB_ID` flag lets you target a
specific tab for both reading and writing.

## Protocol

1.  **Mandatory Discovery:** Before performing any read or write operation, you
    should proactively check if the document contains multiple tabs by running
    `"$GDOCS" readonly list-tabs DOC_ID`.
2.  **Multi-tab Detection:** If you read a document without a tab flag and it
    has multiple tabs, the CLI will prefix the output with `[gdocs]` lines
    listing the tabs. **Do not ignore these warnings.**
3.  **Explicit Targeting:** If the document is multi-tabbed, you MUST identify
    the correct target tab for your operation. Operating without `--tab`
    defaults to the first tab, which can lead to reading the wrong context or
    corrupting the wrong section of the document.
4.  **Pervasive Flag Usage:** Ensure you append `--tab TAB_ID` to *every*
    supporting command when working on a specific tab. Use `readonly list-tabs`
    first to discover tab IDs:

```bash
"$GDOCS" readonly list-tabs DOC_ID
# Tab ID          Title        Index  Nesting
# t.dprlqxjpel7u  Overview     0      0
# t.iqg1w3dc9q0   Design Doc   1      0
# t.j30h49q6knfa  Appendix     0      1

"$GDOCS" readonly read DOC_ID --tab t.dprlqxjpel7u
"$GDOCS" readonly toc DOC_ID --tab t.iqg1w3dc9q0
"$GDOCS" readonly word-count DOC_ID --tab t.j30h49q6knfa
"$GDOCS" readonly extract-tables DOC_ID --tab t.iqg1w3dc9q0
"$GDOCS" readonly extract-links DOC_ID --tab t.dprlqxjpel7u
"$GDOCS" mutate batch DOC_ID -f ops.json --tab t.iqg1w3dc9q0 --index 1  # batch at index
"$GDOCS" mutate create-tab DOC_ID --title "New Section" --index 0       # create at index 0
"$GDOCS" mutate create-tab DOC_ID --title "Nested Tab" --parent PARENT_TAB_ID
"$GDOCS" mutate move-tab DOC_ID TAB_ID --parent NEW_PARENT_TAB_ID
"$GDOCS" mutate move-tab DOC_ID TAB_ID --index 0
"$GDOCS" mutate duplicate-tab DOC_ID --source TAB_ID --title "Copy of Notes"
```

## Supported Commands

Commands that support `--tab`:

*   `readonly read`
*   `mutate delete`
*   `mutate append`
*   `mutate insert`
*   `mutate heading`
*   `mutate batch`
*   `mutate import-md`
*   `readonly export`
*   `readonly extract-tables`
*   `readonly extract-links`
*   `readonly toc`
*   `readonly word-count`
*   `readonly structure`
*   `mutate sed`
*   `mutate insert-image-from-file`
*   `readonly pull`
*   `mutate add-row`
*   `mutate delete-row`
*   `mutate style-table`
*   `mutate update-table`

Without `--tab`, commands operate on the document's default (first) tab.

## Linking Directly to Tabs (Internal Anchors)

Use the `tab_id` property in `mutate batch` operations to link to other tabs.

### Target a Tab in Runs

Specify `tab_id` (discovered via `list-tabs`) on a run or parent operation:

```json
[
  {"op":"rich-text","runs":[
    {"text":"See the "},
    {"text":"Design Proposal Tab","tab_id":"t.iqg1w3dc9q0","bold":true}
  ]}
]
```

### Parent Tab ID Fallbacks

If parent op has `tab_id` or `url`, individual runs inherit it as a fallback:

```json
{"op":"rich-text","tab_id":"t.iqg1w3dc9q0","runs":[
  {"text":"Click "},
  {"text":"here","bold":true},
  {"text":" to open."}
]}
```
