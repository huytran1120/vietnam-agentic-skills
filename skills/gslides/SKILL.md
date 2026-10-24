---
name: gslides
category: productivity
description: Read, create, and edit Google Slides presentations. Use when creating presentations, when the user shares a slides.google.com URL, asks to summarize or extract content from a deck, wants slides drafted or updated, or wants a presentation exported. Don't use for Google Docs, Sheets, or Drive file management.
---

# Google Slides

Work with a Google Slides presentation the user names or links to. Everything
here assumes you already have the **presentation ID** — the segment between
`/d/` and `/edit` in a
`https://docs.google.com/presentation/d/<PRESENTATION_ID>/edit` URL.

## Setup and Authentication

`gslides auth status` is the only way to tell whether you are logged in. Do not
run `--help`, search the filesystem or environment for tokens, check another
plugin's login, or run an operational command before logging in. Follow these
steps exactly.

**1. Register and check.** Run this skill's script with `auth status`. It
downloads the CLI, registers `gslides` on the agent's `PATH` (not the user's
shell), and reports whether you are logged in:

```bash
<path/to/this/skill>/scripts/gslides auth status
```

```powershell
# Windows (PowerShell)
& "<path\to\this\skill>\scripts\gslides.cmd" auth status
```

Every later call is just `gslides`. Never ask the user to run it; they cannot.
If it reports `Logged in`, you are ready.

**2. Log in for the user.** Start this as a background command:

```bash
gslides auth login
```

It prints an authorization URL and exits on its own once the user approves. Read
the URL from the task's log, open it in the user's browser or hand them the
link, then stop and wait. Confirm with `gslides auth status`.

## Usage

Do every Google Slides operation — reading, creating, editing, exporting,
extracting images — through `gslides`. Run `gslides --help` to discover the
available commands and their flags.

Two rules the CLI's own help will not tell you:

-   **Never delete a slide the user did not ask you to delete.** A removed slide
    takes its speaker notes and layout with it, and the user cannot get them
    back.
-   **Edit the elements you were asked about, not the whole deck.** Rebuilding a
    slide from scratch loses the theme, placeholder wiring, and notes that made
    it consistent with the rest of the presentation.

> [!CAUTION]
>
> `gslides mutate delete-slide` and `gslides mutate delete-element` permanently
> remove content from a presentation. **Never** run a destructive command unless
> the user explicitly asks.
>
> **Never** share a presentation with a broad audience, a public link, or a
> whole organization. The user already has access to anything created on their
> behalf — let them handle sharing unless they explicitly instruct otherwise.

## Recipes

**Read and inspect:**

```bash
gslides readonly read PRESENTATION_ID               # all slides as text (or --json for presentation AST)
gslides readonly read-all PRESENTATION_ID           # all slides as text (or --json for presentation AST)
gslides readonly info PRESENTATION_ID               # presentation metadata (or --json for full presentation AST)
gslides readonly list-slides PRESENTATION_ID        # list slides (or --json for slides array)
gslides readonly list-elements PRESENTATION_ID SLIDE_ID
gslides readonly get-page PRESENTATION_ID SLIDE_ID
gslides readonly get-notes PRESENTATION_ID SLIDE_ID
gslides readonly extract-images PRESENTATION_ID
```

**Create and organize:**

```bash
gslides mutate create --title "My Presentation"
gslides mutate copy PRESENTATION_ID "Copy Title"
gslides mutate add-slide PRESENTATION_ID
gslides mutate duplicate PRESENTATION_ID SLIDE_ID
gslides mutate delete-slide PRESENTATION_ID SLIDE_ID
gslides mutate reorder-slide PRESENTATION_ID SLIDE_ID --position 0
```

**Add content:**

```bash
gslides mutate add-textbox PRESENTATION_ID --slide SLIDE_ID --text "Hello" --x 100 --y 100 --width 300 --height 50 --content-alignment MIDDLE
gslides mutate add-text PRESENTATION_ID "More text" --textbox ELEMENT_ID
gslides mutate update-text PRESENTATION_ID --element ELEMENT_ID --text "New text"
gslides mutate add-image PRESENTATION_ID --slide SLIDE_ID --url "https://..." --x 100 --y 200 --width 200 --height 150
gslides mutate insert-image-from-file PRESENTATION_ID --slide SLIDE_ID --file /path/to/image.png
gslides mutate add-table PRESENTATION_ID --slide SLIDE_ID --rows 3 --cols 4
gslides mutate set-table-cell PRESENTATION_ID --table TABLE_ID --row 0 --col 0 --text "Header"
gslides mutate delete-element PRESENTATION_ID ELEMENT_ID
gslides mutate move-element PRESENTATION_ID ELEMENT_ID --x 200 --y 150
gslides mutate resize-element PRESENTATION_ID ELEMENT_ID --width 400 --height 300
gslides mutate update-shape PRESENTATION_ID --element ELEMENT_ID --text "New text" --background-color "#FF0000" --bold
```

**Styling and export:**

```bash
gslides mutate set-background PRESENTATION_ID --slide SLIDE_ID --color "#4285F4"
gslides mutate set-notes PRESENTATION_ID --slide SLIDE_ID --text "Speaker notes here"
gslides readonly export PRESENTATION_ID /tmp/pres.pdf --format pdf
gslides readonly export-thumbnail PRESENTATION_ID /tmp/slide.png
gslides mutate share PRESENTATION_ID --email user@example.com --role writer
gslides mutate batch PRESENTATION_ID requests.json
```

## Commands

Command                                 | Description
--------------------------------------- | --------------------------------
`gslides readonly read`                 | Read slide content
`gslides readonly read-all`             | Read all slides as text
`gslides readonly info`                 | Presentation info
`gslides mutate create`                 | Create presentation
`gslides mutate copy`                   | Copy presentation
`gslides readonly list-slides`          | List slides
`gslides mutate add-slide`              | Add slide
`gslides mutate duplicate`              | Duplicate slide
`gslides mutate delete-slide`           | Delete slide
`gslides mutate reorder-slide`          | Reorder slide
`gslides mutate add-textbox`            | Add text box
`gslides mutate add-text`               | Add text to element
`gslides mutate update-text`            | Update text
`gslides mutate delete-element`         | Delete element
`gslides mutate add-image`              | Add image by URL
`gslides mutate insert-image-from-file` | Insert local image
`gslides mutate add-table`              | Add table
`gslides mutate set-table-cell`         | Set table cell text
`gslides mutate set-background`         | Set background color
`gslides mutate set-notes`              | Set speaker notes
`gslides readonly get-notes`            | Get speaker notes
`gslides mutate move-element`           | Move element
`gslides mutate resize-element`         | Resize element
`gslides mutate update-shape`           | Update shape properties and text
`gslides readonly export`               | Export to PDF/PPTX
`gslides readonly export-thumbnail`     | Export slide as image
`gslides mutate share`                  | Share presentation
`gslides readonly list-elements`        | List elements on slide
`gslides readonly get-page`             | Get page details
`gslides readonly extract-images`       | Extract all images
`gslides mutate batch`                  | Execute raw batchUpdate

## Tips

-   **CRITICAL:** Never attempt to scrape Google Slides URLs (e.g.,
    `docs.google.com/presentation/...`) using web reading tools. Always use the
    GSlides CLI commands (`gslides readonly read`, `gslides readonly read-all`)
    to access presentation contents, as the URLs require authentication and will
    return permission errors.
-   `gslides mutate set-table-cell` and `gslides mutate set-notes` safely handle
    empty content (no need to pre-populate)
-   Use `gslides readonly list-elements PRES_ID SLIDE_INDEX` to discover element
    IDs for tables, textboxes, etc. The SLIDE_INDEX is 0-based (0=first slide,
    1=second, etc.)
-   **Reordering slides index shift**: When using `gslides mutate
    reorder-slide`, the `--position` (which maps to `InsertionIndex` in Slides
    API) is evaluated *before* the source slide is removed.
    -   If moving a slide to a *later* position (`source < target`): specify
        `position = target + 1` to make it end up at index `target`. (e.g., to
        move Slide 4 (index 3) to end up at index 15, use `--position 16`).
    -   If moving a slide to an *earlier* position (`source > target`): specify
        `position = target` to make it end up at index `target`.
-   The `gslides mutate batch` command reads a JSON file of operations for
    efficient bulk updates. Use `--file -` to pipe from stdin.
-   **Removing Default Slide Elements:** Newly created presentations (via
    `gslides mutate create`) contain a single title slide `p` with default
    placeholders (centered title `i0` and subtitle `i1`). To start with a
    completely blank first slide, delete them at the beginning of your batch
    JSON file:

    ```json
    [
      {"op": "delete-element", "element": "i0"},
      {"op": "delete-element", "element": "i1"}
    ]
    ```

-   **Recommended workflow:** Use `gslides readonly export-thumbnail PRES_ID
    output.png --slide SLIDE_ID` to export a slide as an image, review it
    visually, then iterate. This is the best way to verify layout, colors, and
    readability before sharing. Note: `--slide` takes a slide **object ID**
    (e.g. `p`, `slide_xxx`), not a 0-based index. Use `gslides mutate batch
    --json` or `gslides readonly list-slides --json` to get slide IDs.

### Placeholder IDs (Single-Batch Workflows)

Use `"id"` on `add-slide` and `add-table` to create placeholder IDs that
subsequent ops can reference **within the same batch**:

```json
[
  {"op":"add-slide","layout":"BLANK","id":"SLIDE_1"},
  {"op":"set-background","slide":"SLIDE_1","color":"#1E2761"},
  {"op":"add-table","slide":"SLIDE_1","rows":3,"cols":3,"id":"TABLE_1"},
  {"op":"set-table-cell","table":"TABLE_1","row":0,"col":0,"text":"Header"}
]
```

This eliminates the need for multi-pass workflows. The CLI resolves placeholders
to API-generated IDs at runtime.

`set-notes` for newly-created slides is automatically deferred to a second API
call (the CLI handles this transparently).

### Batch `--json` Response

Use `gslides mutate batch PRES_ID -f file.json --json` to get created IDs. The
`resolved_ids` map is needed for any follow-up commands (e.g. `gslides readonly
export-thumbnail`, `gslides mutate insert-image-from-file`) that target created
slides:

```json
{"operations":12,"api_requests":30,"created_slides":["slide_xxx"],"created_tables":["table_xxx"],"resolved_ids":{"SLIDE_1":"slide_xxx","TABLE_1":"table_xxx"}}
```

### Card Design Tips (from Testing)

-   **Use header + body combo** — two textboxes (bold 20pt header + 13-14pt
    body) instead of one tall card. This avoids empty space and gives visual
    hierarchy.
-   **Accent dividers**: thin rectangles (3-4px height) between card sections
    add polish.
-   **Bottom taglines**: centered muted text below cards fills vertical
    whitespace.
-   **Stat call-outs**: rounded rectangles with big numbers (36pt+) make
    overview slides more visual.

## Batch Operations Reference

The batch command supports **27 operations**:

| Op                            | Key Fields                    | Description                   |
| :---------------------------- | :---------------------------- | :---------------------------- |
| `set-background`              | `slide`, `color`              | Slide background color        |
| `add-text`                    | `element`, `textbox`, `text`  | Insert text into element. Use |
:                               :                               : this to safely insert text    :
:                               :                               : into empty                    :
:                               :                               : placeholders/shapes, as       :
:                               :                               : `update-text` may fail.       :
| `add-textbox`                 | `slide`, `text`, `x`, `y`,    | Create textbox with text and  |
:                               : `width`, `height`,            : styling                       :
:                               : `font_size`, `bold`,          :                               :
:                               : `italic`, `underline`,        :                               :
:                               : `strikethrough`, `color`,     :                               :
:                               : `background_color`, `alpha`,  :                               :
:                               : `font_family`, `alignment`,   :                               :
:                               : `content_alignment`,          :                               :
:                               : `line_spacing`, `link`        :                               :
| `add-image`                   | `slide`, `url`, `x`, `y`,     | Insert image from URL         |
:                               : `width`, `height`             :                               :
| `add-slide`                   | `layout`, `id`                | Add slide (default: BLANK).   |
:                               :                               : 'layout' supports standard    :
:                               :                               : enums or custom layout IDs    :
:                               :                               : (e.g. `g43cb3ecfc4_0_85`).    :
:                               :                               : Hint\: Discover custom IDs by :
:                               :                               : running the `gslides readonly :
:                               :                               : info --json` command on       :
:                               :                               : reference deck. 'id' creates  :
:                               :                               : a placeholder for use by      :
:                               :                               : later ops                     :
| `add-table`                   | `slide`, `rows`, `cols`,      | Create table with optional    |
:                               : `id`, `width`, `height`, `x`, : size and coordinates. `id`    :
:                               : `y`                           : creates a placeholder for     :
:                               :                               : `set-table-cell`              :
| `add-line`                    | `slide`, `line_category`,     | Create a straight line,       |
:                               : `x`, `y`, `width`, `height`,  : arrow, or shape-anchored      :
:                               : `start_arrow`, `end_arrow`,   : connector. Set                :
:                               : `line_weight`, `color`,       : `start_connect`/`end_connect` :
:                               : `dash_style`,                 : to shape element IDs (with    :
:                               : `start_connect`,              : `start_site`/`end_site` edge  :
:                               : `end_connect`, `start_site`,  : index) to anchor and          :
:                               : `end_site`, `id`              : auto-route between shapes;    :
:                               :                               : connected lines default to    :
:                               :                               : `BENT`. `id` creates a        :
:                               :                               : placeholder for use by later  :
:                               :                               : ops                           :
| `set-table-cell`              | `table`, `row`, `col`,        | Set + style table cell        |
:                               : `text`, `color`, `bold`,      :                               :
:                               : `font_size`, `font_family`,   :                               :
:                               : `underline`, `strikethrough`, :                               :
:                               : `background_color`, `alpha`   :                               :
| `style-text`                  | `element`, `color`, `bold`,   | Restyle existing text         |
:                               : `italic`, `underline`,        :                               :
:                               : `strikethrough`, `font_size`, :                               :
:                               : `font_family`, `link`,        :                               :
:                               : `start`, `end`                :                               :
| `style-table-cell`            | `table`, `row`, `col`,        | Restyle table cell text or    |
:                               : `color`, `bold`, `font_size`, : alignment (optional range     :
:                               : `font_family`, `underline`,   : `start`/`end`)                :
:                               : `strikethrough`, `alignment`, :                               :
:                               : `start`, `end`                :                               :
| `set-notes`                   | `slide`, `text`               | Set speaker notes             |
| `delete-element`              | `element`                     | Delete element by ID          |
| `delete-text`                 | `element`, `start`, `end`     | Delete text range             |
| `move-element`                | `element`, `x`, `y`           | Move element                  |
| `resize-element`              | `element`, `width`, `height`, | Resize element                |
:                               : `x`, `y`                      :                               :
| `update-text`                 | `element`, `text`             | Replace text in element       |
| `update-alt-text`             | `element`, `description`,     | Replace alt text in element   |
:                               : `title`                       :                               :
| `add-shape`                   | `slide`, `shape_type`, `x`,   | Create shape (RECTANGLE,      |
:                               : `y`, `width`, `height`,       : ELLIPSE, etc.)                :
:                               : `background_color`, `alpha`   :                               :
| `style-shape`                 | `element`,                    | Change shape fill color,      |
:                               : `background_color`, `alpha`,  : border/outline color and      :
:                               : `outline_color`,              : weight                        :
:                               : `outline_weight`              :                               :
| `duplicate-slide`             | `slide`, `id`, `elements`     | Duplicate a slide             |
| `reorder-slide`               | `slide`, `position`           | Move slide to position        |
| `skip-slide`                  | `slide`                       | Skip (hide) a slide from      |
:                               :                               : presentation mode             :
| `unskip-slide`                | `slide`                       | Unskip (unhide) a slide to    |
:                               :                               : make it visible               :
| `replace-all-text`            | `contains`, `replace_text`    | Find-and-replace across deck  |
| `create-bullets`              | `element`, `start`, `end`     | Add bullet points             |
| `update-shape`                | `element`, `text`,            | Update shape properties and   |
:                               : `background_color`, `alpha`,  : text                          :
:                               : `color`, `font_size`, `bold`, :                               :
:                               : `content_alignment`           :                               :
| `updateTableColumnProperties` | `updateTableColumnProperties` | Update table column           |
:                               :                               : properties (e.g. column       :
:                               :                               : width)                        :

### Key Features

-   **`background_color`**: Sets shape fill on textboxes and shapes (card
    layouts, visual accents). Can be set to `"transparent"` to remove fill
    color.
-   **`alpha`**: Sets fill opacity (0.0 to 1.0, e.g. `0.85` for 85% opacity) on
    shape, textbox, and table cell background colors.
-   **`outline_color`**: Hex color (e.g., `"#FF0000"`) to style the shape's
    outline/border.
-   **`outline_weight`**: Line weight in points (e.g. `1.5`) for the shape's
    outline/border.
-   **`font_family`**: Set font (e.g., "Roboto", "Montserrat", "Oswald")
-   **`link`**: Add hyperlinks to text
-   **`strikethrough`**: Applies strikethrough styling to text (boolean, e.g.
    `true`)
-   **`line_spacing`**: Set line height (percentage, e.g., 150 = 1.5× spacing)
-   **`start`/`end`**: Style a range of text (not just all text) in `style-text`
-   **`content_alignment`**: Vertical text alignment inside shape/textbox.
    Allowed values: `"TOP"`, `"MIDDLE"`, `"BOTTOM"`.
-   **`line_category`**: Type of line to create (e.g. `"STRAIGHT"`, `"BENT"`,
    `"CURVED"`, defaults to `"STRAIGHT"`).
-   **`start_arrow` / `end_arrow`**: Arrowhead style (e.g. `"NONE"`,
    `"FILL_ARROW"`, `"STEALTH_ARROW"`, `"CHEVRON_ARROW"`, `"DIAMOND_ARROW"`,
    defaults to `"NONE"`).
-   **`line_weight`**: Line weight/thickness in points (e.g. `2.5`).
-   **`dash_style`**: Line dash pattern (e.g. `"SOLID"`, `"DASH"`, `"DOT"`,
    `"DASH_DOT"`, `"LONG_DASH"`, `"LONG_DASH_DOT"`).
-   **`start_connect` / `end_connect`**: Element ID of a shape to anchor each
    end of the line to, turning it into a connector that auto-routes and stays
    attached as shapes move. Accepts real element IDs (from `gslides readonly
    list-elements`) or in-batch placeholder IDs. When either is set,
    `line_category` defaults to `"BENT"`.
-   **`start_site` / `end_site`**: Connection site (edge midpoint) index on the
    connected shape: `0` = Top, `1` = Left, `2` = Bottom, `3` = Right (verified
    for `RECTANGLE`/`ROUND_RECTANGLE`). A left-to-right connector uses
    `start_site: 3`, `end_site: 1`.
-   **`updateTableColumnProperties`**: Update column widths for a table by
    passing `columnIndices` and `tableColumnProperties.columnWidth`:

    ```json
    {
      "op": "updateTableColumnProperties",
      "updateTableColumnProperties": {
        "objectId": "TABLE_1",
        "columnIndices": [0],
        "tableColumnProperties": {
          "columnWidth": {"magnitude": 65, "unit": "PT"}
        },
        "fields": "columnWidth"
      }
    }
    ```

## Slide Creation Recipe

1.  **Outline**: Decide N slides, types (title, content, stat, table, closing),
    and palette
2.  **Palette**: Pick from `references/styling.md` (Midnight Executive, Ocean
    Gradient, Cherry Bold, etc.)
3.  **Generate batch JSON**: All ops in one file, using the sandwich pattern
    (dark → light → dark)
4.  **Execute**: `gslides mutate create` then `gslides mutate batch PRES_ID -f
    batch.json`
5.  **Review**: `gslides readonly export-thumbnail` each slide, review PNG
6.  **Fix**: Second batch or individual commands
7.  **Notes**: Include `set-notes` in batch for every slide
8.  **Share**: `gslides mutate share PRES_ID --email ...`

### Complete Batch JSON Example

This creates a polished 5-slide deck. Save as `batch.json` and run: `gslides
mutate create --title "Demo"` then `gslides mutate batch PRES_ID -f batch.json`

```json
[
  {"op":"set-background","slide":"p","color":"#1E2761"},
  {"op":"add-textbox","slide":"p","text":"Project Alpha","x":60,"y":120,"width":600,"height":80,"font_size":48,"bold":true,"color":"#FFFFFF","font_family":"Roboto","alignment":"center"},
  {"op":"add-textbox","slide":"p","text":"Q4 2024 Review & Roadmap","x":60,"y":210,"width":600,"height":30,"font_size":20,"color":"#CADCFC","font_family":"Roboto","alignment":"center"},
  {"op":"add-shape","slide":"p","shape_type":"RECTANGLE","x":260,"y":340,"width":200,"height":4,"background_color":"#CADCFC"},
  {"op":"set-notes","slide":"p","text":"Welcome slide. Introduce the team and agenda."},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_1"},
  {"op":"set-background","slide":"SLIDE_1","color":"#F2F2F2"},
  {"op":"add-textbox","slide":"SLIDE_1","text":"Key Results","x":30,"y":15,"width":660,"height":45,"font_size":36,"bold":true,"color":"#1E2761","font_family":"Roboto"},
  {"op":"add-textbox","slide":"SLIDE_1","text":"• 50% faster releases\n• 3x API throughput\n• 99.9% uptime SLA","x":30,"y":75,"width":310,"height":260,"font_size":14,"color":"#333333","font_family":"Roboto","line_spacing":160},
  {"op":"set-notes","slide":"SLIDE_1","text":"Key results from Q4."},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_2"},
  {"op":"set-background","slide":"SLIDE_2","color":"#1E2761"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"Architecture","x":30,"y":15,"width":660,"height":45,"font_size":36,"bold":true,"color":"#FFFFFF","font_family":"Roboto","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"Frontend","x":30,"y":80,"width":200,"height":35,"font_size":20,"bold":true,"color":"#FFFFFF","font_family":"Roboto","background_color":"#2D3A8C","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"React + TypeScript","x":30,"y":120,"width":200,"height":80,"font_size":13,"color":"#CADCFC","font_family":"Roboto","background_color":"#232E73"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"API Layer","x":250,"y":80,"width":200,"height":35,"font_size":20,"bold":true,"color":"#FFFFFF","font_family":"Roboto","background_color":"#2D3A8C","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"Go + gRPC","x":250,"y":120,"width":200,"height":80,"font_size":13,"color":"#CADCFC","font_family":"Roboto","background_color":"#232E73"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"Storage","x":470,"y":80,"width":200,"height":35,"font_size":20,"bold":true,"color":"#FFFFFF","font_family":"Roboto","background_color":"#2D3A8C","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"PostgreSQL + Redis","x":470,"y":120,"width":200,"height":80,"font_size":13,"color":"#CADCFC","font_family":"Roboto","background_color":"#232E73"},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_3"},
  {"op":"set-background","slide":"SLIDE_3","color":"#065A82"},
  {"op":"add-textbox","slide":"SLIDE_3","text":"87%","x":60,"y":80,"width":600,"height":120,"font_size":72,"bold":true,"color":"#FFFFFF","font_family":"Roboto","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_3","text":"of agent tasks complete in under 30 seconds","x":60,"y":210,"width":600,"height":40,"font_size":18,"color":"#CADCFC","font_family":"Roboto","alignment":"center"},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_4"},
  {"op":"set-background","slide":"SLIDE_4","color":"#990011"},
  {"op":"add-textbox","slide":"SLIDE_4","text":"Thank You","x":60,"y":120,"width":600,"height":80,"font_size":48,"bold":true,"color":"#FFFFFF","font_family":"Montserrat","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_4","text":"Questions? → alpha@example.com","x":60,"y":225,"width":600,"height":30,"font_size":16,"color":"#FCF6F5","font_family":"Montserrat","alignment":"center"}
]
```

> **Note:** `SLIDE_1`..`SLIDE_4` are resolved by the CLI at runtime via the
> `"id"` field on `add-slide`. The first slide (`p`) is created by `gslides
> mutate create` and always has ID `p`. Use `gslides mutate batch --json` to see
> the resolved IDs.

## Global Flags

-   `--json` — output as JSON (supported on `gslides readonly read`, `gslides
    readonly read-all`, `gslides readonly info`, `gslides readonly list-slides`,
    `gslides readonly list-elements`, `gslides readonly get-page`, `gslides
    readonly extract-images`, `gslides mutate batch`).
    -   Note: For programmatic inspection, both `gslides readonly read PRES_ID
        --json` and `gslides readonly info PRES_ID --json` emit the full Google
        Slides Presentation API JSON object (including `slides`, `pageElements`,
        `shapes`, and `textElements`). Bare `gslides readonly read PRES_ID`
        emits extracted plain-text.
-   `-v`, `--version` — print the CLI build version
-   `--legacy-mode` — how deprecated/renamed commands are handled: `allowed`
    (default) | `deprecated` | `banned`

## Generating UI Links for Humans

Whenever referencing Google Slides presentations or specific slides:

-   **Entire Presentation**:
    `https://docs.google.com/presentation/d/<deck_id>/edit`
-   **Specific Slide**:
    `https://docs.google.com/presentation/d/<deck_id>/edit#slide=id.<slide_id>`
-   **Prose & Markdown**: Write
    `https://docs.google.com/presentation/d/<deck_id>/edit` or `[Presentation
    Slide](https://docs.google.com/presentation/d/<deck_id>/edit#slide=id.<slide_id>)`.
