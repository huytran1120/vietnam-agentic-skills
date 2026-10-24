# Batch Operations

The `batch` command is the **recommended way to generate documents**. It
executes multiple styled operations in a single API call, producing professional
output with full control over formatting. Always prefer `batch` over `import-md`
or individual CLI commands.

Pass a JSON array of operations via `--file (-f)`. Before writing batch JSON,
**read [styling.md](styling.md)** for templates, color palettes, font pairings,
and anti-patterns.

| Op                         | Required      | Optional Fields            | Description                      |
:                            : Fields        :                            :                                  :
| -------------------------- | ------------- | -------------------------- | -------------------------------- |
| `set-default-style`        | —             | `bold`, `italic`,          | Set defaults for subsequent ops  |
:                            :               : `underline`,               : (no API call — acts as a macro)  :
:                            :               : `font_family`,             :                                  :
:                            :               : `font_size`, `text_color`, :                                  :
:                            :               : `alignment`,               :                                  :
:                            :               : `line_spacing`,            :                                  :
:                            :               : `space_above`,             :                                  :
:                            :               : `space_below`              :                                  :
| `append`                   | `text`        | `bold`, `italic`,          | Append styled text               |
:                            :               : `underline`,               :                                  :
:                            :               : `strikethrough`,           :                                  :
:                            :               : `font_family`,             :                                  :
:                            :               : `font_size`, `text_color`, :                                  :
:                            :               : `alignment`,               :                                  :
:                            :               : `paragraph_bg_color`,      :                                  :
:                            :               : `indent_start`,            :                                  :
:                            :               : `indent_end`,              :                                  :
:                            :               : `indent_first_line`        :                                  :
| `append-inline`            | `text`        | `bold`, `italic`,          | Append styled text inline        |
:                            :               : `underline`,               : without forcing a newline break  :
:                            :               : `strikethrough`,           :                                  :
:                            :               : `font_family`,             :                                  :
:                            :               : `font_size`, `text_color`, :                                  :
:                            :               : `alignment`,               :                                  :
:                            :               : `paragraph_bg_color`,      :                                  :
:                            :               : `indent_start`,            :                                  :
:                            :               : `indent_end`,              :                                  :
:                            :               : `indent_first_line`        :                                  :
| `heading`                  | `text`,       | `bold`, `italic`,          | Insert heading (1-6, TITLE,      |
:                            : `level`       : `font_family`,             : SUBTITLE)                        :
:                            :               : `font_size`, `text_color`, :                                  :
:                            :               : `alignment`,               :                                  :
:                            :               : `space_above`,             :                                  :
:                            :               : `space_below`              :                                  :
| `replace`                  | `find`,       | —                          | Find and replace text            |
:                            : `text`        :                            :                                  :
| `bullet-list`              | `text`        | `bullet_preset`, `bold`,   | Insert bullet item               |
:                            :               : `italic`, `font_size`,     :                                  :
:                            :               : `text_color`,              :                                  :
:                            :               : `space_above`,             :                                  :
:                            :               : `space_below`              :                                  :
| `numbered-list`            | `text`        | `bullet_preset`, `bold`,   | Insert numbered item             |
:                            :               : `italic`, `font_size`,     :                                  :
:                            :               : `text_color`,              :                                  :
:                            :               : `space_above`,             :                                  :
:                            :               : `space_below`              :                                  :
| `insert-table`             | —             | `rows`, `cols`,            | Insert table (with data, styled  |
:                            :               : `table_data`,              : headers, per-cell                :
:                            :               : `table_header_bold`,       : colors/text/bold/URL/alignments, :
:                            :               : `table_header_bg_color`,   : images, column widths, borders,  :
:                            :               : `table_header_text_color`, : rich text formatting)            :
:                            :               : `table_font_family`,       :                                  :
:                            :               : `table_font_size`,         :                                  :
:                            :               : `table_cell_colors`,       :                                  :
:                            :               : `table_cell_text_colors`,  :                                  :
:                            :               : `table_cell_bold`,         :                                  :
:                            :               : `table_cell_urls`,         :                                  :
:                            :               : `table_cell_alignments`,   :                                  :
:                            :               : `table_col_widths`,        :                                  :
:                            :               : `table_border_color`,      :                                  :
:                            :               : `table_border_width`,      :                                  :
:                            :               : `table_border_dash_style`, :                                  :
:                            :               : `table_cell_images`,       :                                  :
:                            :               : `table_cell_image_width`,  :                                  :
:                            :               : `table_cell_image_height`, :                                  :
:                            :               : `table_rich_data`,         :                                  :
:                            :               : `tab_id`                   :                                  :
| `horizontal-rule`          | —             | —                          | Insert visual separator          |
| `page-break`               | —             | —                          | Insert page break (**no-op in    |
:                            :               :                            : pageless mode** — docs are       :
:                            :               :                            : pageless by default; use         :
:                            :               :                            : `--pageless=false` on `create`   :
:                            :               :                            : if you need page breaks)         :
| `link`                     | `text`, `url` | `bold`, `italic`,          | Insert hyperlinked text          |
:                            :               : `font_size`, `text_color`  :                                  :
| `insert-image`             | `image_uri`   | `image_width`,             | Insert inline image              |
:                            : or `url`      : `image_height`             :                                  :
| `rich-text`                | `runs`        | `bold`, `italic`,          | Multi-style paragraph (bold +    |
:                            :               : `underline`,               : normal + code in one line).      :
:                            :               : `strikethrough`,           : Styling and link targets (URL,   :
:                            :               : `font_family`,             : tab_id) applied to the parent op :
:                            :               : `font_size`, `text_color`, : are inherited by all runs as     :
:                            :               : `background_color`,        : fallbacks. Runs support person   :
:                            :               : `bullet_preset`,           : smart chips (email), date chips  :
:                            :               : `alignment`,               : (date, date_format,              :
:                            :               : `paragraph_bg_color`,      : time_zone_id), inline images     :
:                            :               : `indent_start`,            : (image_url, image_width,         :
:                            :               : `indent_end`,              : image_height), and styled text   :
:                            :               : `indent_first_line`,       : (text, bold, italic, underline,  :
:                            :               : `tab_id`                   : strikethrough, font_family,      :
:                            :               :                            : font_size, text_color,           :
:                            :               :                            : background_color, url, tab_id,   :
:                            :               :                            : heading_id, bookmark_id).        :
| `style-table`              | `bg_color`    | `table_num`, `row`,        | Style cells of an existing table |
:                            :               : `row_span`, `col`,         : (background color). **Validates  :
:                            :               : `col_span`                 : row/col bounds before sending    :
:                            :               :                            : requests.**                      :
| `style-text`               | `find`        | `bold`, `italic`,          | Find the first occurrence of a   |
:                            :               : `underline`,               : string inside the document and   :
:                            :               : `strikethrough`,           : apply styling/hyperlinks.        :
:                            :               : `font_family`,             :                                  :
:                            :               : `font_size`, `text_color`, :                                  :
:                            :               : `background_color`, `url`, :                                  :
:                            :               : `heading_id`,              :                                  :
:                            :               : `bookmark_id`,             :                                  :
:                            :               : `named_style_type`         :                                  :
| `style`                    | `start`,      | `bold`, `italic`,          | Apply styling (bold, italic,     |
:                            : `end`         : `underline`,               : underline, strikethrough, font   :
:                            :               : `strikethrough`,           : family, font size,               :
:                            :               : `font_family`,             : text/background color,           :
:                            :               : `font_size`, `text_color`, : URL/heading/bookmark/tab link)   :
:                            :               : `background_color`, `url`, : to a specific character index    :
:                            :               : `heading_id`,              : range.                           :
:                            :               : `bookmark_id`, `tab_id`    :                                  :
| `delete-range`             | `start`,      | —                          | Delete content within a specific |
:                            : `end`         :                            : character range (0 <= start <    :
:                            :               :                            : end).                            :
| `delete-bullets`           | `start`,      | —                          | Delete paragraph bullet          |
:                            : `end`         :                            : formatting from all paragraphs   :
:                            :               :                            : overlapping the specified        :
:                            :               :                            : character range.                 :
| `delete-paragraph-by-text` | `find`        | —                          | Find the first paragraph         |
:                            :               :                            : containing the `find` string,    :
:                            :               :                            : and delete the entire paragraph  :
:                            :               :                            : content (including its newline   :
:                            :               :                            : mark).                           :
| `insert`                   | `start`,      | —                          | Insert unstyled plain text at    |
:                            : `text`        :                            : the specified character index.   :
| `raw`                      | `raw_request` | —                          | Send an arbitrary Google Docs    |
:                            :               :                            : API request.                     :

IMPORTANT: When using `rich-text` and applying styles like `bold`, `italic`, or
`font_family` to a run, these styles may leak into subsequent runs or paragraphs
if not explicitly turned off. To prevent this, always specify `"bold": false`,
`"italic": false`, and the desired default `"font_family"` (e.g., `"Roboto"`) on
all runs that should *not* inherit the style.

### Replacing Document or Tab Content

To replace the entire content of a document or a specific tab before applying
the batch operations, use the `--replace-all` flag with the `batch` command.

When updating a specific tab, combine `--replace-all` with `--tab`:

```bash
"$GDOCS" mutate batch DOC_ID --replace-all --tab TAB_ID -f batch.json
```

This is the recommended way to overwrite a tab's content with new styled content
in a single operation. Do not use `mutate write` with `--clear` if you need to
apply styled batch operations, as `write` only supports plain text.

### Batch Writes Apply Immediately

Every operation in the batch file is written straight into the live document as
soon as the command runs. There is no staging step and no review queue.

> [!CAUTION] `batch` is immediately destructive when combined with
> `--replace-all`, and there is no accept/reject safety net for any batch
> operation. Verify the target `DOC_ID` (and `--tab TAB_ID`) before running, and
> inspect the document with `"$GDOCS" readonly structure` or `"$GDOCS" readonly
> read` first so your indices and find-strings are correct. Collaborators see
> the changes right away.

```bash
"$GDOCS" mutate batch DOC_ID -f batch.json
```

### Numbered List Limitation & Workaround

The `numbered-list` operation uses Google Docs' native paragraph bulleting.
However, calling `numbered-list` multiple times in a sequence of batch
operations often causes Google Docs to restart numbering from 1 for each item,
rather than continuing the list.

**Workaround:** If you need a continuous numbered list, do not use
`numbered-list`. Instead, use `rich-text` with a bullet preset and manual bold
step prefixes:

```json
  {"op":"rich-text","bullet_preset":"BULLET_DISC_CIRCLE_SQUARE","runs":[{"text":"Step 1","bold":true},{"text":": First action item."}]},
  {"op":"rich-text","bullet_preset":"BULLET_DISC_CIRCLE_SQUARE","runs":[{"text":"Step 2","bold":true},{"text":": Second action item."}]}
```

Using manual numbering in `rich-text` runs gives you full control and avoids
Google Docs resetting the list numbering.

### Nested Bullet Lists & Multi-Level Hierarchy

Google Docs represents bullet hierarchies using `createParagraphBullets` with a
bullet preset (such as `BULLET_DISC_CIRCLE_SQUARE`). Glyphs progress by list
nesting level:

-   **Level 0 (`nestingLevel: 0`)**: Solid Disc (`•`)
-   **Level 1 (`nestingLevel: 1`)**: Open Circle (`o`)
-   **Level 2 (`nestingLevel: 2`)**: Square (`■`)

#### Generating Sub-Bullets via Leading Tabs (`\t`)

To generate true native Level 1 sub-bullets (`o`) or Level 2 nested items (`■`):

1.  **Prepend `\t` characters**: Each leading `\t` character in paragraph text
    increments the list nesting level by 1 (e.g., `"\t1. Sub-stage..."` or `"\t*
    Artifact..."` creates a Level 1 bullet).
2.  **Execute `createParagraphBullets`**: Apply the operation over the text
    range containing the bulleted paragraphs.

> [!WARNING] **Paragraph Indentation vs. List Nesting:** Applying `indent_start:
> 72` or `updateParagraphStyle.indentStart` without `\t` +
> `createParagraphBullets` only shifts the text block horizontally. The bullet
> glyph remains at Level 0 (solid disc `•`), creating a visually misaligned
> hanging bullet rather than a true nested circle glyph (`o`).

### Batch Index Accounting & Tab Character Consumption

When `createParagraphBullets` processes paragraphs with leading `\t` characters,
Google Docs **strips each leading tab character from the document AST**,
shortening the document length by 1 code unit per consumed tab.

In multi-request atomic batch updates (e.g., inserting document text and then
applying styles and bullets across multiple sections sequentially):

1.  **Calculate Baseline Indices:** Compute the original 1-based start and end
    offsets of each paragraph/run in the un-bulleted text.
2.  **Track Cumulative Tabs Consumed:** Maintain a running count of all `\t`
    characters stripped by preceding `createParagraphBullets` requests.
3.  **Adjust Downstream Ranges:** Subtract `cumulative_tabs` from both `start`
    and `end` for all subsequent operations:
    -   `adj_start = start - cumulative_tabs`
    -   `adj_end = end - cumulative_tabs`

```python
# Example batch index adjustment in Python
cumulative_tabs = 0
for group in bullet_groups:
  adj_start = group.start - cumulative_tabs
  adj_end = group.end - cumulative_tabs
  requests.append({
      "createParagraphBullets": {
          "range": {
              "startIndex": adj_start,
              "endIndex": adj_end,
              "tabId": tab_id,
          },
          "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
      }
  })
  cumulative_tabs += group.tab_count
```

> [!CAUTION] If downstream `updateTextStyle` or `createParagraphBullets` ranges
> fail to subtract consumed tabs, the API fails with: `400 Bad Request: Invalid
> range: Range (X, Y) extends beyond document`.

### Styling Fields

Any text operation supports inline styling:

| Field                | Type   | Example            | Effect                  |
| -------------------- | ------ | ------------------ | ----------------------- |
| `bold`               | bool   | `true`             | Bold text               |
| `italic`             | bool   | `true`             | Italic text             |
| `underline`          | bool   | `true`             | Underline text          |
| `strikethrough`      | bool   | `true`             | Strikethrough           |
| `font_family`        | string | `"Roboto"`         | Font family             |
| `font_size`          | float  | `14`               | Font size (pt)          |
| `text_color`         | hex    | `"#1a73e8"`        | Text color              |
| `background_color`   | hex    | `"#e8f0fe"`        | Text highlight color    |
| `alignment`          | string | `"CENTER"`         | Paragraph alignment     |
| `space_above`        | float  | `12`               | Space above paragraph   |
:                      :        :                    : (pt)                    :
| `space_below`        | float  | `6`                | Space below paragraph   |
:                      :        :                    : (pt)                    :
| `line_spacing`       | float  | `115`              | Line spacing            |
:                      :        :                    : (100=single)            :
| `paragraph_bg_color` | hex    | `"#fef7e0"`        | Paragraph shading       |
:                      :        :                    : (full-width background) :
| `indent_start`       | float  | `36`               | Left indent in points   |
| `indent_end`         | float  | `36`               | Right indent in points  |
| `indent_first_line`  | float  | `36`               | First line indent in    |
:                      :        :                    : points                  :
| `heading_id`         | string | `"h.f7nvfqmov0f2"` | Link to internal        |
:                      :        :                    : document heading        :
| `bookmark_id`        | string | `"k.bookmark_id"`  | Link to internal        |
:                      :        :                    : document bookmark       :
| `tab_id`             | string | `"t.iqg1w3dc9q0"`  | Link to internal        |
:                      :        :                    : document tab            :

### Table-Specific Fields

These fields apply only to `insert-table` operations:

Field                     | Type         | Example                          | Effect
------------------------- | ------------ | -------------------------------- | ------
`table_header_bg_color`   | hex          | `"#e8f0fe"`                      | Header row background
`table_header_text_color` | hex          | `"#1a73e8"`                      | Header row text color
`table_header_bold`       | bool         | `true`                           | Bold header row
`table_font_family`       | string       | `"Roboto"`                       | Font for all table cells
`table_font_size`         | float        | `9`                              | Font size for table cells
`table_cell_colors`       | `[][]string` | `[[""],["#d9ead3"]]`             | Per-cell background colors (row×col, "" = no color)
`table_rich_data`         | `[][][]run`  | `[[[{"text":"A"}]]]`             | Per-cell rich text runs
`table_cell_text_colors`  | `[][]string` | `[[""],["#137333"]]`             | Per-cell text colors (row×col, "" = default)
`table_cell_bold`         | `[][]bool`   | `[[false],[true]]`               | Per-cell bold (row×col)
`table_cell_urls`         | `[][]string` | `[[""],["https://example.com"]]` | Per-cell hyperlinks (row×col)
`table_cell_alignments`   | `[][]string` | `[["CENTER"],["RIGHT"]]`         | Per-cell paragraph alignments (row×col, "" = default)
`table_col_widths`        | `[]float`    | `[100, 200, 168]`                | Column widths in points
`table_border_color`      | hex          | `"#dadce0"`                      | Border color for all edges
`table_border_width`      | float        | `0.5`                            | Border width in points
`table_border_dash_style` | string       | `"DOT"`                          | Border dash style (`"SOLID"`, `"DOT"`, `"DASH"`)
`table_cell_images`       | `[][]string` | `[[""],["https://..."]`          | Per-cell image URLs (row×col, "" = no image)
`table_cell_image_width`  | float        | `32`                             | Image width in points (applies to all cell images)
`table_cell_image_height` | float        | `32`                             | Image height in points

> **📖 See [styling.md](styling.md)** for color palettes, font pairings, 5
> document layout templates, and anti-patterns.

### Complete Batch JSON Example

This creates a styled design doc with colored tables, callout boxes, and
blockquotes. Save the JSON below as `batch.json` and run:

```bash
"$GDOCS" mutate create --title "Design Doc"
"$GDOCS" mutate batch DOC_ID -f batch.json
```

```json
[
  {"op":"set-default-style","font_family":"Roboto","font_size":11,"text_color":"#202124","line_spacing":115},
  {"op":"heading","text":"Feature Design Doc","level":"1","font_size":28,"text_color":"#1a73e8"},
  {"op":"append","text":"Status: Draft","font_size":10,"text_color":"#1a73e8","bold":true,"paragraph_bg_color":"#e8f0fe"},
  {"op":"append","text":"Author: username  •  Created: 2026-03-06","font_size":10,"text_color":"#5f6368","italic":true},
  {"op":"horizontal-rule"},
  {"op":"heading","text":"Overview","level":"2","font_family":"Roboto","text_color":"#1a73e8","space_above":16},
  {"op":"append","text":"Brief description of the feature..."},
  {"op":"rich-text","font_size":11,"runs":[{"text":"✅ Goal: ","bold":true,"text_color":"#137333"},{"text":"Make it easy to build and ship within 1 day","text_color":"#202124"}]},
  {"op":"rich-text","font_size":11,"runs":[{"text":"❌ Non-Goal: ","bold":true,"text_color":"#d93025"},{"text":"Replace existing frameworks","text_color":"#202124"}]},
  {"op":"append","text":"\"This approach would save us months of development time.\"","italic":true,"indent_start":36,"indent_end":36,"text_color":"#5f6368"},
  {"op":"heading","text":"📊 Comparison","level":"2","font_family":"Roboto","text_color":"#1a73e8","space_above":16},
  {"op":"insert-table","table_data":[["Option","Speed","Cost","Risk"],["Option A","Fast","Low","Medium"],["Option B","Slow","High","Low"]],"table_header_bg_color":"#e8f0fe","table_header_text_color":"#1a73e8","table_header_bold":true,"table_font_family":"Roboto","table_font_size":11,"table_cell_colors":[[""],["#d9ead3","#d9ead3","#fff2cc"],["#f4cccc","#f4cccc","#d9ead3"]],"table_col_widths":[120,120,120,108],"table_border_color":"#dadce0","table_border_width":0.5},
  {"op":"append","text":"TLDR: Option A is recommended for most teams.","paragraph_bg_color":"#fef7e0","bold":true,"font_size":10},
  {"op":"heading","text":"❓ Open Questions","level":"2","font_family":"Roboto","text_color":"#1a73e8","space_above":16},
  {"op":"insert-table","table_data":[["Question","Status","Owner"],["API design review","Open","Alice"],["Security review","Pending","Bob"]],"table_header_bg_color":"#fce8e6","table_header_text_color":"#d93025","table_header_bold":true,"table_font_family":"Roboto","table_font_size":11,"table_col_widths":[260,60,60],"table_border_color":"#dadce0","table_border_width":0.5},
  {"op":"append","text":"Confidential - Internal Use Only","alignment":"CENTER","font_size":8,"text_color":"#9aa0a6","italic":true}
]
```

### GDocs-Native Internal Anchors

Use internal anchors in text operations or `rich-text` runs to link inside the
document:

*   `heading_id`: Link to a heading (e.g., `"h.f7nvfqmov0f2"`)
*   `bookmark_id`: Link to a bookmark (e.g., `"k.bookmark_id"`)
*   `tab_id`: Link to another tab (e.g., `"t.iqg1w3dc9q0"`)

> [!IMPORTANT] **Cross-Tab Heading & Bookmark Linking (Tabs Enabled)**
>
> When working with tabbed Google Docs, if you want to link to a heading or
> bookmark residing on a **different tab** than the text range being modified:
>
> 1.  **Native API Solution (Recommended)**: You must specify both the target
>     heading/bookmark ID *and* the target `tab_id` in the same operation. This
>     instructs the API to use the modern, non-legacy `Link.heading` or
>     `Link.bookmark` fields, which resolve the target unambiguously:
>
>     ```json
>     {"op": "style", "start": 10, "end": 20, "heading_id": "h.yyyyyy", "tab_id": "t.xxxxxx"}
>     ```
>
>     *If you omit `tab_id`, the API falls back to the legacy `heading_id` /
>     `bookmark_id` fields, which fail with a `400 Bad Request` for cross-tab
>     targets because those legacy fields only resolve within the same tab.*
>
> 2.  **Relative URL Alternative**: Alternatively, you can use the `url`
>     property with a relative URL containing both the tab ID and the target
>     anchor ID. This is how the GDocs UI represents cross-tab links:
>
>     ```json
>     {"op": "style", "start": 10, "end": 20, "url": "?tab=t.xxxxxx#heading=h.yyyyyy"}
>     ```
>
> For details on the underlying model and the differences between legacy and
> modern fields, refer to the
> [Link Resource Reference](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents#link).

**Rich-text runs with fallback:**

```json
{"op":"rich-text","tab_id":"t.iqg1w3dc9q0","runs":[
  {"text":"See "},
  {"text":"Methodology","heading_id":"h.f7nvfqmov0f2","bold":true},
  {"text":" or "},
  {"text":"Appendix","tab_id":"t.j30h49q6knfa","bold":true},
  {"text":", otherwise "},
  {"text":"click here","bold":true}
]}
```

*(Runs without links fall back to the parent's `tab_id`)*

**Style-text example:**

```json
{"op":"style-text","find":"Telemetry","bookmark_id":"k.telemetry_bookmark","text_color":"#1155cc","underline":true}
```

### style-table Bounds Validation

The `style-table` operation performs strict bounds checks on `row` and `col`
indices before making API requests. Verify table dimensions using `"$GDOCS"
readonly structure` first to avoid index errors.

### Raw API Requests (`raw`)

The `raw` operation allows you to execute arbitrary Google Docs API requests
(i.e. `docs.Request` structures) directly via the `batch` command.

#### When to Use

Use this operation **only** as a fallback for features that are not natively
supported by other batch operations. For standard formatting, text appending,
lists, or tables, always prefer the dedicated native operations as they handle
index tracking and bounds verification automatically.

#### Schema

The `raw` operation requires a single field:

*   `raw_request` (object): A Google Docs API `Request` object (matching the
    schema of the
    [Google Docs API Reference](https://developers.google.com/docs/api/reference/rest/v1/documents/request)).

#### Example

To update table cell borders:

```json
{
  "op": "raw",
  "raw_request": {
    "updateTableCellStyle": {
      "tableCellStyle": {
        "borderBottom": {
          "color": {"color": {"rgbColor": {"blue": 0.9, "green": 0.1, "red": 0.1}}},
          "width": {"magnitude": 2, "unit": "PT"},
          "dashStyle": "SOLID"
        }
      },
      "fields": "borderBottom",
      "tableStartLocation": {
        "index": 120
      }
    }
  }
}
```
