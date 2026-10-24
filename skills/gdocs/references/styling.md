# GDocs Styling Reference

A comprehensive guide for creating polished Google Docs programmatically with
the `mutate batch` command, based on Google Docs design best practices.

--------------------------------------------------------------------------------

## Philosophy

**Documents should feel intentionally designed.** A well-structured doc with
consistent typography, thoughtful spacing, and clear hierarchy communicates
professionalism. Every heading, table, and paragraph should reinforce the
document's purpose.

Four rules:

1.  **Consistent typography** — pick one heading font and one body font, use
    them everywhere
2.  **Clear visual hierarchy** — title > headings > body, with at least 1.5x
    size difference between levels
3.  **Density over whitespace** — information-dense pages look more professional
    and more informative than sparse ones. Use `line_spacing: 115` (not higher),
    minimize blank lines between elements, and keep paragraphs substantive (3+
    sentences). A document that feels "airy" reads as empty.
4.  **Surgical structural variety** — break monotony with a few well-placed
    callouts, goal labels, or quotes — not by fragmenting every section into
    sub-headings. Variety should serve the content, not replace it.

> [!TIP] Start every batch with `set-default-style` to avoid repeating
> `font_family`/`font_size`/`text_color` on every op:

```json
{"op":"set-default-style","font_family":"Roboto","font_size":11,"text_color":"#202124","line_spacing":115}
```

--------------------------------------------------------------------------------

## Document Structure Variety

**The biggest flaw in generated docs is monotonous structure.** A document that
alternates heading → paragraph → table → heading → paragraph → table reads like
a database dump, not a design doc. Real documents vary their rhythm.

### The Problem

Compare these two structures:

```
BAD (monotonous):                      GOOD (varied):
─────────────────                      ─────────────────
Title                                  Title
Metadata                               Metadata + links
HR                                     HR
H2: Section A                          H2: Objective
  paragraph                              2 paragraphs of prose
  table                                H2: Why is this a problem?
H2: Section B                            paragraph
  paragraph                              bold numbered principles
  table                                  paragraph (elaborates)
H2: Section C                          H2: Goals and Non Goals
  paragraph                              labeled bullets (Goal/Non-Goal)
  table                                H2: Proposals
H2: Section D                            H3: 1. Proposal title
  paragraph                                diagram image
  table                                   paragraph
                                          H4: Solutions
                                            bullet list with links
                                        H3: 2. Proposal title
                                          note/callout box
                                          table with color legend
                                          legend explanation (paragraph)
                                        H2: Testimonials
                                          italic quote bullets
                                        HR
                                        Footer
```

### Rules for Structural Variety

1.  **No two adjacent sections should have the same shape.** If Section A is
    heading + paragraph + table, then Section B should be heading + paragraph +
    bullets, or heading + paragraph + sub-sections. Only specific document types
    (roadmaps, catalogs) use back-to-back same-shaped sections.

2.  **Prose is the backbone, not tables.** Every section should have at least
    2–3 sentences of flowing prose. Tables, bullets, and diagrams support the
    narrative — they are not the entire section. A table should never be the
    first element after a heading.

3.  **Use sub-headings (H3/H4) sparingly.** Only use H3 when a section is
    genuinely long (4+ paragraphs) and covers distinct subtopics. Over-using H3
    fragments content into thin slices that feel sparse and less informative.
    Numbered proposals (e.g., "1. Make data access easier") work well as H3
    headings under a parent H2, but most sections should remain as dense H2
    blocks with flowing prose.

4.  **Mix element types within a section.** A single section can contain:
    paragraph → bullet list → paragraph → table → paragraph. This creates
    natural rhythm and keeps the reader engaged.

5.  **Interleave prose around tables.** Always introduce a table with a
    paragraph explaining what it shows, and follow it with analysis or a
    takeaway sentence. Never let a table stand alone between two headings.

6.  **Keep it dense.** A well-written page should feel packed with information.
    Prefer one 8-line paragraph over four 2-line paragraphs separated by blanks.
    Minimize `{"op":"append","text":""}` spacers — use `space_above` on headings
    instead (16–24pt). The document should look full, not airy.

### Techniques for Variety

#### Labeled Bullets (Goal / Non-Goal pattern)

Use `rich-text` to create bullets with colored labels:

```json
{"op":"rich-text","font_size":11,"runs":[
  {"text":"Goal","bold":true,"text_color":"#137333"},
  {"text":": Make it easy to prototype with production data","text_color":"#202124"}
]},
{"op":"rich-text","font_size":11,"runs":[
  {"text":"Non-Goal","bold":true,"text_color":"#D93025"},
  {"text":": Replace UX mockups","text_color":"#202124"}
]}
```

This breaks the visual monotony of plain bullets and immediately signals
importance/category. Use for: Goals/Non-Goals, Pros/Cons, Do/Don't,
Required/Optional.

#### Numbered Proposals as Sub-Sections

Instead of a flat list, promote each proposal to its own H3:

```json
{"op":"heading","text":"Proposals","level":"2","font_size":22,"text_color":"#1a73e8"},
{"op":"heading","text":"1. Make data access easier and faster","level":"3","font_size":16,"text_color":"#5f6368"},
{"op":"append","text":"Explanation paragraph..."},
{"op":"heading","text":"Solutions","level":"4","font_size":12,"bold":true},
{"op":"bullet-list","items":["Create a single endpoint server","Build client libraries for auth"]},
{"op":"heading","text":"2. Lower the process barrier","level":"3","font_size":16,"text_color":"#5f6368"},
{"op":"append","text":"Different explanation..."},
{"op":"insert-table","table_data":[["Data Source","Prototype","Research"],["External APIs","✓","✓"]]}
```

This creates a document that feels like a real proposal with depth, not a slide
deck converted to a doc.

#### Table Color Legends

After a table with colored cells, add a brief legend using rich-text:

```json
{"op":"rich-text","font_size":10,"runs":[
  {"text":"Green","bold":true,"text_color":"#137333"},
  {"text":" - No approvals needed   ","text_color":"#202124"},
  {"text":"Yellow","bold":true,"text_color":"#F09300"},
  {"text":" - Review required   ","text_color":"#202124"},
  {"text":"Red","bold":true,"text_color":"#D93025"},
  {"text":" - Blocked on legal & privacy sign-off","text_color":"#202124"}
]}
```

#### Testimonials / Quotes Section

Use italic bullets for user feedback or stakeholder quotes:

```json
{"op":"heading","text":"Testimonials","level":"2","font_size":22,"text_color":"#1a73e8"},
{"op":"bullet-list","items":[
  "\"absolutely invaluable for aligning everyone's expectations\" - Main App PM",
  "\"I feel that is a game changer\" - UX Program Manager",
  "\"This has been foundational for the team\" - Partner Team PM"
],"italic":true,"text_color":"#5f6368"}
```

#### Inline Links Within Prose

Don't isolate links as separate line items. Embed them naturally in paragraphs
using `rich-text`:

```json
{"op":"rich-text","font_size":11,"text_color":"#202124","runs":[
  {"text":"A detailed investigation is in the "},
  {"text":"design doc","text_color":"#1a73e8","url":"https://example.com/design-doc"},
  {"text":". See also the "},
  {"text":"roadmap","text_color":"#1a73e8","url":"https://example.com/roadmap"},
  {"text":" for upcoming features."}
]}
```

#### Note / Callout Boxes

Use `paragraph_bg_color` with a bold prefix for contextual notes:

```json
{"op":"rich-text","paragraph_bg_color":"#E8EAED","font_size":11,"text_color":"#202124","runs":[
  {"text":"Note: ","bold":true},
  {"text":"This table is an example of tracks and is not what the end result could look like"}
]}
```

Place these before tables or diagrams that need context. They break the
heading→paragraph→table cadence with an unexpected visual element.

#### Metadata with Inline Links

Instead of plain metadata lines, make them functional:

```json
{"op":"rich-text","font_size":10,"text_color":"#202124","runs":[
  {"text":"Authors: ","bold":true},
  {"text":"Your Name"}
]},
{"op":"rich-text","font_size":10,"text_color":"#202124","runs":[
  {"text":"Self link: ","bold":true},
  {"text":"Design doc","text_color":"#1a73e8","url":"https://docs.google.com/document/d/DOC_ID/edit"}
]},
{"op":"rich-text","font_size":10,"text_color":"#202124","runs":[
  {"text":"Slides: ","bold":true},
  {"text":"Presentation Deck","text_color":"#1a73e8","url":"https://docs.google.com/presentation/d/..."}
]}
```

### Section Rhythm Guide

For a 6–8 page design doc, aim for this rhythm:

| Section               | Primary Elements       | Variety Technique         |
| --------------------- | ---------------------- | ------------------------- |
| Title + metadata      | heading + rich-text    | Functional metadata with  |
:                       : links                  : links                     :
| Objective             | 2+ paragraphs of prose | Pure prose — no tables or |
:                       :                        : bullets                   :
| Problem statement     | paragraph + bold       | Numbered principles       |
:                       : numbered list +        : sandwiched by prose       :
:                       : paragraph              :                           :
| Goals / Non-Goals     | labeled bullets        | Color-coded Goal/Non-Goal |
:                       : (rich-text)            : labels                    :
| Proposals             | H3 sub-sections with   | Each proposal uses        |
:                       : mixed content          : different elements        :
| Comparison            | paragraph + table +    | Table wrapped in          |
:                       : paragraph              : explanatory prose         :
| Evidence / Case study | paragraph + metrics    | Data-driven narrative     |
:                       : table + analysis       :                           :
| Testimonials          | heading + italic quote | Social proof with         |
:                       : bullets                : attribution               :
| Open questions        | callout box + numbered | Warning-colored callout + |
:                       : list                   : items                     :

--------------------------------------------------------------------------------

## Color Palettes

Each palette lists Heading, Body, Accent, and Table Header colors.

Theme                  | Heading   | Body Text | Accent/Link | Table Header | Best For
---------------------- | --------- | --------- | ----------- | ------------ | --------
**Clean Blue**         | `#1a73e8` | `#202124` | `#1a73e8`   | `#e8f0fe`    | Reports, design docs
**Executive Dark**     | `#1E2761` | `#3C4043` | `#4285F4`   | `#E8EAED`    | Board decks, exec summaries
**Forest Growth**      | `#137333` | `#202124` | `#34A853`   | `#E6F4EA`    | Sustainability, growth reports
**Coral Energy**       | `#D93025` | `#3C4043` | `#F96167`   | `#FCE8E6`    | Marketing, creative briefs
**Ocean Deep**         | `#065A82` | `#202124` | `#1C7293`   | `#E1F5FE`    | Technology, data reports
**Slate Professional** | `#2F4F4F` | `#3C4043` | `#4682B4`   | `#ECEFF1`    | Consulting, ops reviews
**Warm Academic**      | `#5F4B32` | `#3C4043` | `#8B6914`   | `#FFF8E1`    | Research, academic papers
**Indigo Innovation**  | `#3F37C9` | `#202124` | `#7209B7`   | `#EDE7F6`    | AI/ML, research proposals

--------------------------------------------------------------------------------

## Typography

### Font Pairings

Stick to fonts that are available in the Google Docs font picker by default so
the document renders the same for every reader.

| Header Font          | Body Font | Mood              | Best For              |
| -------------------- | --------- | ----------------- | --------------------- |
| **Arial**            | Arial     | Clean, universal  | Safest default, any   |
:                      :           :                   : doc                   :
| **Roboto**           | Roboto    | Neutral, readable | Technical docs,       |
:                      :           :                   : reports               :
| **Montserrat Bold**  | Open Sans | Professional      | Proposals,            |
:                      :           :                   : newsletters           :
| **Lato Bold**        | Lato      | Friendly, warm    | Team updates, meeting |
:                      :           :                   : notes                 :
| **Playfair Display** | Lato      | Elegant, formal   | Executive summaries   |
| **Poppins Bold**     | Poppins   | Rounded, modern   | Product docs          |

### Size Hierarchy

Element        | Font Size   | Weight   | Notes
-------------- | ----------- | -------- | --------------------------
Document title | **28–32pt** | Bold     | Heading font (e.g. Roboto)
Subtitle       | **10–12pt** | Italic   | Muted color (gray)
Heading 1 (H1) | **24pt**    | Bold     | Section headers
Heading 2 (H2) | **18pt**    | Bold     | Subsection headers
Heading 3 (H3) | **14pt**    | Bold     | Minor sections
Body text      | **11pt**    | Regular  | Dark gray (#202124)
Bullet text    | **11pt**    | Regular  | Same as body
Table text     | **10–11pt** | Regular  | Slightly smaller OK
Table header   | **10–11pt** | **Bold** | Stand out from data
Footer/caption | **8pt**     | Italic   | Muted gray (#9aa0a6)

### Rules

-   **Left-align everything** except title (centered is OK for single-line
    titles)
-   **Use dark gray not black** for body text: `#202124` is more readable than
    `#000000`
-   **Bold for emphasis.** Italic for metadata. Underline almost never.
-   **Max 2 fonts** in a document — one for headings, one for body

--------------------------------------------------------------------------------

## Document Layout Templates

### 1. Technical Design Doc

```
Title (28pt, blue)
Status: [Draft/Review/Approved] | Author: name | Date: YYYY-MM-DD
─────────────────────────────────────────────────
Overview (H2)
  Body text...

Background (H2)
  Body text...

Design (H2)
  Body text...
  ┌─────────────────────────────────────┐
  │ Component │ Description │ Status   │  ← table with bold headers
  │ ...       │ ...         │ ...      │
  └─────────────────────────────────────┘

Alternatives Considered (H2)
  Body text...

Testing Plan (H2)
  • Unit tests
  • Integration tests
  • Manual verification

─────────────────────────────────────────────────
Confidential - Internal Use Only (8pt, centered, gray)
```

**Batch recipe:**

```json
[
  {"op":"heading","text":"Feature Name - Design Doc","level":"1","font_family":"Roboto","font_size":28,"text_color":"#1a73e8"},
  {"op":"append","text":"Status: Draft","font_size":10,"text_color":"#1a73e8","bold":true,"paragraph_bg_color":"#e8f0fe"},
  {"op":"append","text":"Author: Your Name • Created: 2026-03-06","font_size":10,"text_color":"#5f6368","italic":true},
  {"op":"horizontal-rule"},
  {"op":"heading","text":"Overview","level":"2","font_family":"Roboto","font_size":18,"text_color":"#1a73e8","space_above":16},
  {"op":"append","text":"Brief description of the feature...","font_size":11,"text_color":"#202124"},
  {"op":"heading","text":"Design","level":"2","font_family":"Roboto","font_size":18,"text_color":"#1a73e8","space_above":16},
  {"op":"insert-table","table_data":[["Component","Description","Status"],["Module A","Core logic","Done"],["Module B","API layer","In Progress"]],"table_header_bg_color":"#e8f0fe","table_header_text_color":"#1a73e8","table_header_bold":true,"table_font_family":"Roboto","table_font_size":9,"table_cell_colors":[[""],[""],["#fff2cc"]],"table_border_color":"#dadce0","table_border_width":0.5},
  {"op":"heading","text":"Testing Plan","level":"2","font_family":"Roboto","font_size":18,"text_color":"#1a73e8","space_above":16},
  {"op":"bullet-list","text":"Unit tests for all new functions","font_size":11,"text_color":"#202124"},
  {"op":"bullet-list","text":"Integration tests with mock API","font_size":11,"text_color":"#202124"},
  {"op":"horizontal-rule"},
  {"op":"append","text":"Confidential - Internal Use Only","alignment":"CENTER","font_size":8,"text_color":"#9aa0a6","italic":true}
]
```

### 2. Weekly Status Report

```
Title (28pt, blue)
Week of March 3-7, 2026
─────────────────────────────────────────────────
TL;DR (H2)
  One-line summary

Highlights (H2)
  ┌────────────────────────────────────┐
  │ Area    │ Update        │ Status  │  ← bold headers
  │ ...     │ ...           │ ...     │
  └────────────────────────────────────┘

Risks & Blockers (H2)
  • Risk 1 - mitigation
  • Risk 2 - mitigation

Next Week (H2)
  1. Action item 1
  2. Action item 2
```

### 3. Project Proposal

```
Title (32pt, executive blue)
Prepared for: Stakeholder | Date: YYYY-MM-DD
─────────────────────────────────────────────────
Executive Summary (H1)
  Body text...

Problem Statement (H2)
  Body text...

Proposed Solution (H2)
  Body text...

Timeline (H2)
  ┌────────────────────────────────────┐
  │ Phase    │ Dates       │ Deliverables │
  │ ...      │ ...         │ ...          │
  └────────────────────────────────────┘

Budget (H2)
  ┌────────────────────────────────────┐
  │ Item     │ Cost        │ Notes     │
  └────────────────────────────────────┘

─── Page Break ───

Appendix (H1)
  Supporting details...
```

### 4. Meeting Notes

```
Title (24pt)
Date: YYYY-MM-DD | Attendees: names
─────────────────────────────────────────────────
Agenda (H2)
  1. Topic 1
  2. Topic 2

Discussion (H2)
  Topic 1 (H3)
    Key points discussed...

  Topic 2 (H3)
    Key points discussed...

Action Items (H2)
  ┌────────────────────────────────────┐
  │ Action   │ Owner    │ Due Date   │
  │ ...      │ ...      │ ...        │
  └────────────────────────────────────┘

Decisions (H2)
  • Decision 1 - rationale
  • Decision 2 - rationale
```

### 5. Newsletter / Announcement

```
Title (32pt, bold, accent color)
Subtitle tagline (12pt, muted)
─────────────────────────────────────────────────
What's New (H1, large)
  Feature description paragraph...

Key Numbers (H2)
  ┌──────────────────────────────┐
  │ Metric   │ Before  │ After  │
  │ ...      │ ...     │ ...    │
  └──────────────────────────────┘

Getting Started (H2)
  1. Step one
  2. Step two
  3. Step three

Learn More (H3)
  Link to docs...
  Link to demo...
```

--------------------------------------------------------------------------------

## Advanced Patterns

These patterns use `paragraph_bg_color`, `indent_start`/`indent_end`,
`table_cell_colors`, `table_cell_urls`, `table_col_widths`, and
`table_border_color`/`table_border_width`.

### Callout / TLDR Box

Use `paragraph_bg_color` to create full-width shaded boxes:

```json
{"op":"append","text":"TLDR: Use Option A for most use cases.","paragraph_bg_color":"#fef7e0","bold":true,"font_size":10}
```

Common callout colors:

Purpose      | `paragraph_bg_color` | `text_color` | Example
------------ | -------------------- | ------------ | -----------------
Info/Note    | `#e8f0fe`            | `#202124`    | Blue info box
TLDR/Tip     | `#fef7e0`            | `#202124`    | Yellow highlight
Success      | `#e6f4ea`            | `#137333`    | Green success
Warning      | `#fce8e6`            | `#d93025`    | Red warning
Status badge | `#e8f0fe`            | `#1a73e8`    | Blue label (bold)

### Blockquote

Use `indent_start` and `indent_end` with italic + gray to simulate a blockquote:

```json
{"op":"append","text":"\"This changed how we approach the problem.\"","italic":true,"indent_start":36,"indent_end":36,"text_color":"#5f6368"}
```

### Code Block

Use `Roboto Mono` + `paragraph_bg_color` for each line of code:

```json
{"op":"append","text":"func main() {","font_family":"Roboto Mono","font_size":9,"text_color":"#37474f","paragraph_bg_color":"#f5f5f5"}
```

### Metadata Badges

Put status or labels as styled paragraphs with background shading:

```json
{"op":"append","text":"Visibility: Confidential","font_size":10,"text_color":"#1a73e8","bold":true,"paragraph_bg_color":"#e8f0fe"},
{"op":"append","text":"Status: Approved","font_size":10,"text_color":"#137333","bold":true,"paragraph_bg_color":"#e6f4ea"}
```

### Colored Comparison Matrix

Use `table_cell_colors` (2D array, row×col) to color individual cells. Use
`table_col_widths` (point values) to control column sizing. Use
`table_header_bg_color` / `table_header_text_color` for styled headers:

```json
{"op":"insert-table",
  "table_data":[["Option","Speed","Risk"],["A","Fast ✓","Low ✓"],["B","Slow ✗","High ✗"]],
  "table_header_bg_color":"#1a73e8",
  "table_header_text_color":"#ffffff",
  "table_header_bold":true,
  "table_font_family":"Roboto",
  "table_font_size":9,
  "table_cell_colors":[[""],["#d9ead3","#d9ead3"],["#f4cccc","#f4cccc"]],
  "table_col_widths":[120, 174, 174],
  "table_border_color":"#dadce0",
  "table_border_width":0.5
}
```

Common cell color meanings:

Meaning             | Color
------------------- | ------------------------
Good/Yes/Done       | `#d9ead3` (light green)
Bad/No/Blocked      | `#f4cccc` (light red)
Partial/In Progress | `#fff2cc` (light yellow)
Neutral/Header      | `#f1f3f4` (light gray)

### Rich Text Runs (Multi-Style Paragraphs)

Use `rich-text` op with `runs` array for mixed styles in one paragraph. Styling
applied to the parent `rich-text` op is inherited by all runs unless overridden:

```json
{"op":"rich-text","font_size":11,"runs":[
  {"text":"Goal: ","bold":true,"text_color":"#137333"},
  {"text":"Make it easy to spin up prototypes","text_color":"#202124"}
]}
```

For inline code within text:

```json
{"op":"rich-text","font_size":11,"text_color":"#202124","runs":[
  {"text":"Call "},
  {"text":"registerExtensions()","font_family":"Roboto Mono","font_size":10,"text_color":"#d93025"},
  {"text":" to start."}
]}
```

Each run supports text, bold, italic, underline, strikethrough, font_family,
font_size, text_color, background_color, hyperlinks (url, tab_id, heading_id,
bookmark_id), smart chips (email, date, date_format, time_zone_id), and inline
images (image_url, image_width, image_height). Runs inherit parent rich-text
properties as fallbacks.

Use `bullet_preset` on the `rich-text` op for checklist items with inline
formatting:

```json
{"op":"rich-text","runs":[{"text":"Review the "},{"text":"design doc","bold":true,"url":"https://docs.google.com/document/d/DOC_ID/edit"},{"text":" with "},{"email":"reviewer@example.com"}],"bullet_preset":"BULLET_CHECKBOX"}
```

### Per-Cell Text Styling & Hyperlinks

Use `table_cell_text_colors`, `table_cell_bold`, and `table_cell_urls` (same 2D
layout as `table_cell_colors`):

```json
{"op":"insert-table",
  "table_data":[["Criterion","Option A","Option B"],["Speed","Fast ✓","Slow ✗"]],
  "table_cell_text_colors":[[""],["#137333","#d93025"]],
  "table_cell_bold":[[false],[true,false]],
  "table_cell_urls":[[""],["","https://example.com/issues/123"]]
}
```

### Per-Cell Rich Text & Styling Fallbacks

Use `table_rich_data` (3D array of runs) for mixed styles, links, smart chips,
and images per-cell. Cell runs inherit parent `insert-table` styling defaults
(e.g., `bold`, `italic`, `background_color`):

```json
{"op":"insert-table",
  "bold":true,
  "background_color":"#fff2cc",
  "table_rich_data":[[[
    {"text":"Fallback Bold"},
    {"text":" (strikethrough & green)","strikethrough":true,"background_color":"#d9ead3"},
    {"text":" - Date: "},
    {"date":"2026-06-02T16:17:27Z"}
  ]]]
}
```

### Table with Embedded Images

Use `table_cell_images` for logo/icon columns (same row×col layout):

```json
{"op":"insert-table",
  "table_data":[["","Product","Status"],["","Gmail","GA"],["","Drive","GA"]],
  "table_cell_images":[[""],["https://...gmail_48dp.png"],["https://...drive_48dp.png"]],
  "table_cell_image_width":24,
  "table_cell_image_height":24,
  "table_col_widths":[40,160,100]
}
```

Images are inserted per-cell after all other styling. Use `""` to skip cells.
Width/height apply uniformly to all cell images in the table.

--------------------------------------------------------------------------------

## Anti-Patterns

| Mistake              | Why It's Bad          | Fix                           |
| -------------------- | --------------------- | ----------------------------- |
| **Black body text**  | Too harsh on white    | Use `#202124` (dark gray)     |
:                      : background            :                               :
| **No font            | Inconsistent default  | Always set `font_family`      |
: specified**          : fonts                 :                               :
| **Huge headings,     | Poor readability      | Body 11pt, H2 18pt max        |
: tiny body**          :                       :                               :
| **No spacing between | Feels cramped         | Use `space_above` on headings |
: sections**           :                       :                               :
| **Empty tables**     | Meaningless structure | Always use `table_data`       |
| **No table headers** | Hard to read data     | Use `table_header_bold:true`  |
| **Centered body      | Hard to scan          | Left-align all body           |
: text**               :                       : paragraphs                    :
| **No horizontal      | Sections blend        | Add a rule **after the header |
: rules**              : together              : block** and **before the      :
:                      :                       : footer** — not between every  :
:                      :                       : section; headings with        :
:                      :                       : `space_above` already         :
:                      :                       : separate sections             :
| **Horizontal rule    | Looks like            | Use at most 2 rules: one      |
: between every        : presentation slides   : after title/metadata, one     :
: section**            :                       : before footer. Let headings   :
:                      :                       : and whitespace do the work    :
| **Single-page        | Overwhelming          | Use `page-break` for appendix |
: everything**         :                       : (requires `--pageless=false`  :
:                      :                       : — docs are pageless by        :
:                      :                       : default; `page-break` is a    :
:                      :                       : no-op in pageless mode)       :
| **Slide-deck         | Feels like a          | Each section should have ≥2   |
: structure**          : slideshow, not a      : paragraphs of flowing prose.  :
:                      : document              : Tables support the narrative  :
:                      :                       : — they are not the entire     :
:                      :                       : section. Aim for 4–6 major    :
:                      :                       : sections, not 10+ tiny ones   :
| **Tables without     | Reader lacks context  | Always introduce a table with |
: surrounding          :                       : a paragraph explaining what   :
: narrative**          :                       : it shows, and follow it with  :
:                      :                       : analysis or takeaways         :
| **No footer**        | Missing attribution   | Add centered gray italic      |
:                      :                       : footer                        :
| **Plain tables**     | Lost visual impact    | Use `table_header_bg_color` + |
:                      :                       : `table_border_color`          :
| **Monochrome status  | Hard to scan          | Use `table_cell_colors` with  |
: cells**              :                       : green/red/yellow              :
| **Empty text         | Causes API error:     | Use                           |
: spacers**            : empty range           : `space_above`/`space_below`   :
: `{"text"\:""}`       :                       : instead                       :
| **Logo tables        | Looks amateur         | Use `table_cell_images` with  |
: without images**     :                       : product icons                 :
| **`line_spacing` >   | Pages feel sparse,    | Always use `line_spacing:     |
: 115**                : airy, and less        : 115`. Higher values (125+)    :
:                      : informative           : waste vertical space and make :
:                      :                       : the doc look empty            :
| **Blank `append`     | Creates excessive     | Remove most                   |
: spacers between      : whitespace, wastes    : `{"op"\:"append","text"\:""}` :
: every element**      : pages                 : lines. Use `space_above` on   :
:                      :                       : headings (16–24pt) for        :
:                      :                       : section gaps. Only use blank  :
:                      :                       : appends before tables or      :
:                      :                       : between conceptually distinct :
:                      :                       : paragraphs                    :
| **Over-fragmented H3 | Splits content into   | Use H3 only for genuinely     |
: sub-sections**       : thin, sparse slices   : long sections with distinct   :
:                      : that feel less        : subtopics. Most sections      :
:                      : informative           : should remain dense H2        :
:                      :                       : blocks. A 4-paragraph H2 is   :
:                      :                       : better than 4 H3s with 1      :
:                      :                       : paragraph each                :
| **Metadata on        | Wastes vertical space | Combine Author, Date, Status  |
: separate lines**     : in the header         : on one line with `•`          :
:                      :                       : separators using `rich-text`  :
:                      :                       : runs                          :

--------------------------------------------------------------------------------

## Quick Checklist

Before considering a doc complete:

-   [ ] **`set-default-style` is the first op** with `font_family`,
    `font_size:11`, `text_color:"#202124"`, `line_spacing:115`
-   [ ] **Every text element has `text_color` set** (use `#202124` for body)
-   [ ] **Every text element has `font_family` set** (one for headings, one for
    body)
-   [ ] **Title is 28pt+ bold**, body is 11pt
-   [ ] **Tables have styled headers** (`table_header_bold`,
    `table_header_bg_color`, `table_header_text_color`)
-   [ ] **Tables have borders** (`table_border_color: "#dadce0"`,
    `table_border_width: 0.5`)
-   [ ] **Tables use normal text font and size** — tables should use the same
    font family (e.g., `Roboto`) and size (11pt) as the body text to maintain
    consistency, unless density requirements require a smaller size (9-10pt).
-   [ ] **Heading colors match** — all H2s use same accent color
-   [ ] **Headings have `space_above` and `space_below`** — headings should have
    `space_above` (16-24pt) and `space_below` (6-10pt) for proper breathing room
    and separation from content. Headings are the primary spacing mechanism.
-   [ ] **Lists have appropriate boundary spacing** — lists should have
    `space_above` (8pt) on the first item and `space_below` (8pt) on the last
    item for breathing room, while keeping intermediate items tight
    (`space_above: 2`, `space_below: 2`).
-   [ ] **Horizontal rules** used sparingly — only after header block and before
    footer, not between sections
-   [ ] **Footer with attribution** (centered, 8pt, gray italic)
-   [ ] Callout/TLDR boxes use `paragraph_bg_color` for emphasis
-   [ ] Status cells in tables use `table_cell_colors` (green/red/yellow)
-   [ ] **Pages feel dense and informative** — not airy or sparse.
    `line_spacing` is exactly 115
-   [ ] **No excessive blank-line spacers** — removed unnecessary
    `{"op":"append","text":""}` between elements
-   [ ] **Structural variety is surgical** — 2–3 callouts/quotes per doc, not
    every section reshaped
-   [ ] **Metadata on one line** — Author • Date • Status combined, not on 3
    separate lines

--------------------------------------------------------------------------------

## Named Styles

Google Docs supports document-wide named styles (e.g., Title, Subtitle, Heading
1 - 6, Normal Text). Instead of formatting individual paragraphs, update the
document-wide style definition so that all matching headings or text are
automatically updated.

### Formatting Named Styles

Use the `mutate format-named-styles` command to modify these styles. To
configure a specific style type, specify `--style-type` and any style overrides:

*   `--style-type`: `TITLE`, `SUBTITLE`, `HEADING_1`, `HEADING_2`, `HEADING_3`,
    `HEADING_4`, `HEADING_5`, `HEADING_6`, `NORMAL_TEXT`
*   Style overrides: `--font-size`, `--text-color`, `--font-family`, `--weight`

Example:

```bash
"$GDOCS" mutate format-named-styles DOC_ID --style-type TITLE --font-size 24 --text-color "#1976D2" --font-family "Roboto" --weight 700
```

> [!TIP] Apply the same accent color and font family across `TITLE`,
> `HEADING_1`, `HEADING_2`, and `HEADING_3` (with a `--weight` of `700`) to get
> a coordinated theme in four commands, instead of styling every paragraph
> individually in a batch.

--------------------------------------------------------------------------------

## Updating Existing Documents

When updating an existing document (not creating from scratch), use these
commands instead of rebuilding with `batch`:

### Quick Text Replacements

```bash
# sed replaces ALL occurrences by default; pass --first to change only the first
"$GDOCS" mutate sed DOC_ID 's/Draft/Final/g'
# -i is --case-insensitive (it does NOT mean "in place" — all edits are in place)
"$GDOCS" mutate sed DOC_ID -e 's/v1.0/v2.0/' -e 's/TBD/Confirmed/' -i
"$GDOCS" mutate sed DOC_ID -f weekly_updates.sed
```

### Section Replacement

1.  Use `structure` to see the document layout
2.  Use `batch --after/--before` to replace a section with styled content

```bash
"$GDOCS" readonly structure DOC_ID
"$GDOCS" mutate batch DOC_ID -f new_metrics.json --after "## Metrics" --before "## Design"
```

### Full Document Overwrite

> [!CAUTION] Every `mutate` command applies its changes to the document
> immediately — nothing is staged for review and there is no accept/reject
> safety net. `--clear` and `--replace-all` destroy the existing body. Export a
> copy (`readonly export DOC_ID --format md -o backup.md`) before overwriting
> anything you might need to restore.

```bash
"$GDOCS" mutate write DOC_ID -f report.md --clear
"$GDOCS" mutate batch DOC_ID -f full_doc.json --replace-all
```

### Table Data Updates

```bash
"$GDOCS" mutate update-table DOC_ID --headers "Metric,Target,Current" --data-file data.json
```

--------------------------------------------------------------------------------

## Document Creation Recipe

1.  **Outline**: Decide sections, content types (text, tables, lists, images),
    and style.
2.  **Palette**: Pick font + colors (e.g., Roboto + `#1a73e8` blue headings).
3.  **Generate batch JSON**: Start with `set-default-style` (Roboto, 11pt,
    `#202124`, `line_spacing:115`). All ops in one file — headings, text, lists,
    tables. Keep pages dense: minimize blank `append` spacers, use `space_above`
    on headings (16–24pt) for section gaps. Add 2–3 callouts or goal labels for
    structural variety, but don't fragment every section into sub-headings.
    Combine metadata (Author • Date • Status) on one line.
4.  **Create doc**:

    ```bash
    DOC_ID=$("$GDOCS" mutate create --title "Report" --json | jq -r .documentId)
    ```

5.  **Execute batch**:

    ```bash
    "$GDOCS" mutate batch "$DOC_ID" -f batch.json
    ```

6.  **Export for review**: Export all pages as PNG by iterating `--page 1`,
    `--page 2`, etc.:

    ```bash
    "$GDOCS" readonly export "$DOC_ID" --format png --output p1.png --page 1
    ```

    (Repeat until the command errors, meaning no more pages).

7.  **Review ALL pages visually** (view every PNG). Check that pages feel dense
    and informative, not airy. Fix via second batch if needed.

8.  **Share**: Grant access to collaborators as needed:

    ```bash
    "$GDOCS" mutate share "$DOC_ID" --email person@example.com --role writer
    ```

### Complete Batch JSON Example

See [batch_operations.md](batch_operations.md) for a full example.
