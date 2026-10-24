# GSlides Styling Reference

A comprehensive guide for creating visually impressive presentations with the
GSlides skill. Adapted from industry best practices, WCAG accessibility
guidelines, and battle-tested patterns.

--------------------------------------------------------------------------------

## Philosophy

**Don't create boring slides.** Plain text on a white background is forgettable.
Every slide should feel intentionally designed, as if a human designer placed
each element. The agent's job is to match or exceed that bar programmatically.

Three rules that matter most:

1.  **Every text element needs an explicit `--color`** — the default is black,
    which vanishes on dark backgrounds
2.  **Every slide needs a visual element** — image, table, icon, shape, or
    colored block. Text-only slides are forgettable
3.  **Vary layouts across slides** — repeating the same structure screams
    "machine-generated"

--------------------------------------------------------------------------------

## Color

### Picking a Palette

Choose colors that match your topic. If swapping your palette into a different
presentation would still "work," you haven't made specific enough choices.

**Palette structure:**

-   One dominant color (60-70% visual weight)
-   One or two supporting tones
-   One sharp accent for callouts, highlights, stats

**Never give all colors equal weight.** Dominance creates hierarchy.

### Ready-to-Use Palettes

Each palette below lists Background, Text, and Accent colors with proven
contrast ratios.

| Theme          | Background | Text      | Accent    | Best For        |
| -------------- | ---------- | --------- | --------- | --------------- |
| **Midnight     | `#1E2761`  | `#CADCFC` | `#FFFFFF` | Enterprise,     |
: Executive**    :            :           :           : strategy,       :
:                :            :           :           : finance         :
| **Forest &     | `#2C5F2D`  | `#F5F5F5` | `#97BC62` | Sustainability, |
: Moss**         :            :           :           : growth, nature  :
| **Coral        | `#FFFFFF`  | `#2F3C7E` | `#F96167` | Marketing,      |
: Energy**       :            :           :           : creative,       :
:                :            :           :           : startups        :
| **Warm         | `#B85042`  | `#E7E8D1` | `#A7BEAE` | Brand, culture, |
: Terracotta**   :            :           :           : wellness        :
| **Ocean        | `#065A82`  | `#FFFFFF` | `#1C7293` | Technology,     |
: Gradient**     :            :           :           : data, cloud     :
| **Charcoal     | `#36454F`  | `#F2F2F2` | `#FFFFFF` | Minimalism,     |
: Minimal**      :            :           :           : product, design :
| **Teal Trust** | `#028090`  | `#FFFFFF` | `#02C39A` | Healthcare,     |
:                :            :           :           : trust, fintech  :
| **Berry &      | `#6D2E46`  | `#ECE2D0` | `#A26769` | Luxury, wine,   |
: Cream**        :            :           :           : hospitality     :
| **Sage Calm**  | `#84B59F`  | `#FFFFFF` | `#50808E` | Meditation,     |
:                :            :           :           : education, HR   :
| **Cherry       | `#990011`  | `#FCF6F5` | `#FFFFFF` | Announcements,  |
: Bold**         :            :           :           : urgency, news   :
| **Slate        | `#2F4F4F`  | `#F0F0F0` | `#4682B4` | Consulting,     |
: Professional** :            :           :           : engineering,    :
:                :            :           :           : ops             :
| **Sunrise      | `#FF6B35`  | `#FFFFFF` | `#004E89` | Energy,         |
: Warm**         :            :           :           : startups,       :
:                :            :           :           : events          :
| **Indigo       | `#3F37C9`  | `#E0E0FF` | `#7209B7` | AI, ML,         |
: Deep**         :            :           :           : research,       :
:                :            :           :           : innovation      :
| **Golden       | `#1B1B2F`  | `#E4C580` | `#B0A090` | Awards,         |
: Hour**         :            :           :           : premium,        :
:                :            :           :           : finance         :
| **Arctic       | `#FFFFFF`  | `#1A1A2E` | `#4361EE` | Clean tech,     |
: Clean**        :            :           :           : diagrams, docs  :

### Slide Structure: The Sandwich

Use a **dark → light → dark** pattern across the deck:

```
Slide 1: Title        → Dark background (sets mood)
Slide 2: Overview     → Light background (easy reading)
Slide 3: Content      → Light background
Slide 4: Data/Chart   → Dark background (dramatic emphasis)
Slide 5: Content      → Light background
Slide 6: Summary      → Dark background
Slide 7: Closing/CTA  → Dark background (memorable ending)
```

Or commit to **dark throughout** for a premium, modern feel.

### Contrast Rules (WCAG 2.0)

| Scenario             | Minimum Contrast Ratio | Example                   |
| -------------------- | ---------------------- | ------------------------- |
| Body text (14pt and  | **4.5:1**              | `#FFFFFF` on `#1E2761` =  |
: below)               :                        : **13.5\:1** ✅             :
| Large text (18pt+ or | **3:1**                | `#CADCFC` on `#1E2761` =  |
: 14pt bold)           :                        : **8.2\:1** ✅              :
| Decorative /         | No minimum             | Accent shapes, watermarks |
: non-essential        :                        :                           :

**Quick check:** If you can't instantly read the text when you squint, the
contrast is too low.

### Dangerous Color Combinations

Avoid these — they fail for color blindness or low contrast:

Combination               | Why It Fails
------------------------- | ------------------------------------
Red + Green               | 8% of men are red-green colorblind
Blue + Purple             | Nearly identical under many displays
Light gray + White        | Contrast ratio < 2:1
Yellow text + White bg    | Invisible
Black text + Dark blue bg | **This is the #1 agent mistake**
Green + Brown             | Indistinguishable for deuteranopia

--------------------------------------------------------------------------------

## Typography

### Font Selection

Use **sans-serif fonts** for screen readability. Serif fonts look elegant in
print but pixelate on projectors and screens.

**Recommended pairings (available in Google Slides):**

Header Font          | Body Font       | Mood
-------------------- | --------------- | ----------------------
**Roboto Bold**      | Roboto Light    | Clean, modern
**Montserrat Bold**  | Open Sans       | Professional, startup
**Lato Black**       | Lato Regular    | Friendly, readable
**Oswald**           | Source Sans Pro | Strong, editorial
**Playfair Display** | Lato            | Elegant, sophisticated
**Poppins Bold**     | Poppins Regular | Rounded, approachable
**Arial Black**      | Arial           | Safe, universal
**Roboto Slab**      | Roboto          | Technical, structured

### Size Hierarchy

Maintain consistent sizing to create clear visual hierarchy:

| Element           | Size Range  | Weight         | Notes                    |
| ----------------- | ----------- | -------------- | ------------------------ |
| Slide title       | **36–44pt** | Bold           | Center or left-align     |
| Big stat / hero   | **60–72pt** | Bold           | For emphasis slides      |
: number            :             :                :                          :
| Section header    | **20–24pt** | Bold           | Subsections on content   |
:                   :             :                : slides                   :
| Body text         | **14–16pt** | Regular        | Left-align, never center |
| Bullet points     | **14–16pt** | Regular        | Max 5-6 per slide        |
| Captions / labels | **10–12pt** | Regular, muted | Use lighter color, not   |
:                   :             :                : bold                     :
| Footer / source   | **8–10pt**  | Regular, muted | Bottom edge, minimal     |

**Rule:** Titles should be at least **2x the size** of body text. If your body
is 14pt, your title must be 28pt+. This creates instant visual hierarchy.

### Text Rules

-   **Left-align body text.** Only center titles and single-line labels.
    Centered paragraphs are hard to scan.
-   **One idea per slide.** If you need more than 6 bullets, split across
    slides.
-   **Use keywords, not sentences.** The agent's audience reads the slide, not a
    teleprompter. Keep bullets to 6 words or fewer.
-   **Never use ALL CAPS for body.** Reserve caps for short labels or acronyms.
-   **Use bold for emphasis.** Not underline, not italics, not color alone. Bold
    is universally understood.

--------------------------------------------------------------------------------

## Layout

### Slide Dimensions

Google Slides uses a `720 × 405 pt` canvas (16:9 aspect ratio).

Zone         | X Range | Y Range | Purpose
------------ | ------- | ------- | -----------------------
Safe margin  | 30–690  | 20–385  | Keep all content inside
Title strip  | 30–690  | 15–65   | Top of slide
Main content | 30–690  | 70–340  | Central area
Footer       | 30–690  | 355–395 | Bottom edge

### Layout Templates

Vary layouts across slides. Here are 10 proven structures:

<!-- mdformat off(reason: preserving ASCII layout diagrams) -->

**1. Title Slide (Full Bleed)**

```
┌────────────────────────────────────┐
│              [dark bg]             │
│                                    │
│        PRESENTATION TITLE          │
│           subtitle text            │
│                                    │
│           [icon/logo]              │
└────────────────────────────────────┘
```

**2. Two-Column (Text + Image)**

```
┌─────────────────┬──────────────────┐
│  Title          │                  │
│                 │    [IMAGE]       │
│  • Bullet 1     │                  │
│  • Bullet 2     │                  │
│  • Bullet 3     │                  │
└─────────────────┴──────────────────┘
```

**3. Three Cards / Columns**

```
┌────────────────────────────────────┐
│              Title                 │
│  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │ Icon │  │ Icon │  │ Icon │    │
│  │ Text │  │ Text │  │ Text │    │
│  └──────┘  └──────┘  └──────┘    │
└────────────────────────────────────┘
```

**4. Big Stat Callout**

```
┌────────────────────────────────────┐
│                                    │
│            72pt                    │
│         "87%"                      │
│   of users prefer dark mode        │
│                                    │
│     -- Source: User Research 2024   │
└────────────────────────────────────┘
```

**5. Comparison / Before-After**

```
┌─────────────────┬──────────────────┐
│     BEFORE      │      AFTER       │
│                 │                  │
│  [content]      │   [content]      │
│                 │                  │
└─────────────────┴──────────────────┘
```

**6. Full-Width Table**

```
┌────────────────────────────────────┐
│              Title                 │
│  ┌──────────────────────────────┐ │
│  │  Header  │  Header │ Header │ │
│  │  data    │  data   │ data   │ │
│  │  data    │  data   │ data   │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘
```

**7. Icon + Text Rows**

```
┌────────────────────────────────────┐
│              Title                 │
│  [●] Feature Name -- Description   │
│  [●] Feature Name -- Description   │
│  [●] Feature Name -- Description   │
│  [●] Feature Name -- Description   │
└────────────────────────────────────┘
```

**8. Timeline / Process Flow**

```
┌────────────────────────────────────┐
│              Title                 │
│  ①──────②──────③──────④──────⑤    │
│  Step   Step   Step   Step   Step  │
│  desc   desc   desc   desc   desc  │
└────────────────────────────────────┘
```

**9. Half-Bleed Image**

```
┌──────────────────┬─────────────────┐
│                  │                 │
│    [FULL         │  Title          │
│     IMAGE]       │  Body text      │
│                  │  • Bullet       │
│                  │                 │
└──────────────────┴─────────────────┘
```

**10. Quote / Testimonial**

```
┌────────────────────────────────────┐
│                                    │
│     "Quote text goes here in       │
│      large italic font"           │
│                                    │
│            -- Attribution           │
└────────────────────────────────────┘
```

<!-- mdformat on -->

### Spacing Rules

Rule                     | Value        | Notes
------------------------ | ------------ | ---------------------------
Minimum margin from edge | **30pt**     | All sides
Between content blocks   | **20–30pt**  | Vertically
Between columns          | **20pt**     | Horizontally
After title              | **15–20pt**  | Before content begins
Line height              | **1.2–1.5×** | Default is usually fine
Padding inside cards     | **15–20pt**  | If using colored rectangles

**Leave breathing room.** An empty slide with one great visual is more impactful
than a crowded slide with five mediocre ones.

### Batch JSON Coordinates for Each Layout

Ready-to-use batch JSON snippets. Replace `SLIDE` with your slide ID, customize
colors from a palette above, and adjust text content.

**Title Slide** (Layout 1):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#1E2761"},
{"op":"add-textbox", "slide":"SLIDE", "text":"PRESENTATION TITLE", "x":60, "y":120, "width":600, "height":80, "font_size":48, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Subtitle goes here", "x":60, "y":210, "width":600, "height":30, "font_size":20, "color":"#CADCFC", "font_family":"Roboto", "alignment":"center"},
{"op":"add-shape", "slide":"SLIDE", "shape_type":"RECTANGLE", "x":260, "y":340, "width":200, "height":4, "background_color":"#CADCFC"},
{"op":"set-notes", "slide":"SLIDE", "text":"Welcome slide. Introduce the topic and set context."}
```

**Two-Column** (Layout 2, text left + content right):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#F2F2F2"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Section Title", "x":30, "y":15, "width":660, "height":45, "font_size":36, "bold":true, "color":"#1E2761", "font_family":"Roboto"},
{"op":"add-textbox", "slide":"SLIDE", "text":"• Point one\n• Point two\n• Point three", "x":30, "y":75, "width":310, "height":260, "font_size":14, "color":"#333333", "font_family":"Roboto", "line_spacing":160},
{"op":"add-image", "slide":"SLIDE", "url":"IMAGE_URL", "x":370, "y":75, "width":310, "height":260}
```

**Three Cards** (Layout 3, header + body combo):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#1E2761"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Our Approach", "x":30, "y":15, "width":660, "height":45, "font_size":36, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Step 1", "x":30, "y":80, "width":200, "height":35, "font_size":20, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#3D4A9C", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Description of first item\nwith supporting details", "x":30, "y":120, "width":200, "height":80, "font_size":13, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#2D3A8C"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Step 2", "x":250, "y":80, "width":200, "height":35, "font_size":20, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#3D4A9C", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Description of second item\nwith supporting details", "x":250, "y":120, "width":200, "height":80, "font_size":13, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#2D3A8C"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Step 3", "x":470, "y":80, "width":200, "height":35, "font_size":20, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#3D4A9C", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Description of third item\nwith supporting details", "x":470, "y":120, "width":200, "height":80, "font_size":13, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#2D3A8C"},
{"op":"add-shape", "slide":"SLIDE", "shape_type":"RECTANGLE", "x":260, "y":270, "width":200, "height":3, "background_color":"#CADCFC"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Each step builds on the previous", "x":130, "y":290, "width":460, "height":25, "font_size":13, "color":"#8899BB", "font_family":"Roboto", "alignment":"center"}
```

**Big Stat** (Layout 4):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#1E2761"},
{"op":"add-textbox", "slide":"SLIDE", "text":"87%", "x":60, "y":80, "width":600, "height":120, "font_size":72, "bold":true, "color":"#FFFFFF", "font_family":"Roboto", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"of users now complete tasks in under 30 seconds", "x":60, "y":210, "width":600, "height":40, "font_size":18, "color":"#CADCFC", "font_family":"Roboto", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Source: User Research Q4 2024", "x":60, "y":360, "width":600, "height":20, "font_size":10, "color":"#8899BB", "font_family":"Roboto", "alignment":"center"}
```

**Full-Width Table** (Layout 6):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#F2F2F2"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Key Metrics", "x":30, "y":15, "width":660, "height":45, "font_size":36, "bold":true, "color":"#1E2761", "font_family":"Roboto"},
{"op":"add-table", "slide":"SLIDE", "rows":4, "cols":3, "id":"TABLE_1"},
{"op":"set-table-cell", "table":"TABLE_1", "row":0, "col":0, "text":"Metric", "bold":true, "color":"#1E2761", "font_family":"Roboto"},
{"op":"set-table-cell", "table":"TABLE_1", "row":0, "col":1, "text":"Q3", "bold":true, "color":"#1E2761", "font_family":"Roboto"},
{"op":"set-table-cell", "table":"TABLE_1", "row":0, "col":2, "text":"Q4", "bold":true, "color":"#1E2761", "font_family":"Roboto"}
```

**Closing / CTA Slide** (Layout 10):

```json
{"op":"set-background", "slide":"SLIDE", "color":"#990011"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Thank You", "x":60, "y":120, "width":600, "height":80, "font_size":48, "bold":true, "color":"#FFFFFF", "font_family":"Montserrat", "alignment":"center"},
{"op":"add-textbox", "slide":"SLIDE", "text":"Questions? → contact@example.com", "x":60, "y":225, "width":600, "height":30, "font_size":16, "color":"#FCF6F5", "font_family":"Montserrat", "alignment":"center"},
{"op":"add-shape", "slide":"SLIDE", "shape_type":"RECTANGLE", "x":260, "y":280, "width":200, "height":4, "background_color":"#FCF6F5"}
```

--------------------------------------------------------------------------------

## Visual Elements

### Images

-   **Use high-quality images.** Pixelated images destroy credibility.
-   **Maintain aspect ratio.** Never stretch images.
-   **Use `"$GSLIDES" mutate add-image` for URLs, `"$GSLIDES" mutate
    insert-image-from-file` for local files.**

### Tables

Tables are powerful visual elements when styled well:

-   **Header row:** Bold text, darker background color (tables inherit default
    white backgrounds in Google Slides)
-   **Keep tables compact:** Don't let them fill the entire slide
-   **Data tables:** Max 6-8 rows visible. More than that → split across slides
-   **Use `"$GSLIDES" mutate set-table-cell` to update individual cells after
    creation**

### Shapes as Visual Accents

Use `background_color` on `add-textbox` to create cards in a single step:

```json
{"op":"add-textbox", "slide":"SLIDE", "text":"Card Title\nCard body text", "x":30, "y":80, "width":300, "height":250, "font_size":14, "color":"#FFFFFF", "font_family":"Roboto", "background_color":"#2D3A8C"}
```

Use `add-shape` for pure visual accents (dividers, decorations):

```json
{"op":"add-shape", "slide":"SLIDE", "shape_type":"RECTANGLE", "x":260, "y":340, "width":200, "height":4, "background_color":"#CADCFC"}
```

### Font + Palette Pairings

Palette            | Header Font          | Body Font
------------------ | -------------------- | ---------------
Midnight Executive | **Roboto Bold**      | Roboto
Ocean Gradient     | **Montserrat Bold**  | Open Sans
Cherry Bold        | **Oswald**           | Source Sans Pro
Golden Hour        | **Playfair Display** | Lato
Indigo Deep        | **Poppins Bold**     | Poppins
Charcoal Minimal   | **Lato Black**       | Lato

--------------------------------------------------------------------------------

## Visual Motifs

Pick ONE distinctive design element and repeat it across every slide. This
creates cohesion. Examples:

| Motif                      | How to Implement (batch JSON)                  |
| -------------------------- | ---------------------------------------------- |
| **Accent divider**         | `{"op":"add-shape", "shape_type":"RECTANGLE",  |
:                            : "x"\:260, "y"\:340, "width"\:200, "height"\:4, :
:                            : "background_color"\:"#CADCFC"}`                :
| **Card grid**              | Use `background_color` on `add-textbox` for    |
:                            : each card                                      :
| **Colored sidebar**        | `{"op":"add-shape", "shape_type":"RECTANGLE",  |
:                            : "x"\:0, "y"\:0, "width"\:30, "height"\:405,    :
:                            : "background_color"\:"#CADCFC"}`                :
| **Numbered badges**        | Bold numbers (① ② ③) in accent color before    |
:                            : items                                          :
| **Dark/light alternation** | Alternate `set-background` colors every 2-3    |
:                            : slides                                         :

--------------------------------------------------------------------------------

## Anti-Patterns (What NOT to Do)

### Critical Mistakes

| Mistake                 | Why It's Bad            | Fix                      |
| ----------------------- | ----------------------- | ------------------------ |
| **No `color` on         | Default black text      | Always set `color`       |
: textbox**               : vanishes on dark        : explicitly               :
:                         : backgrounds             :                          :
| **Same layout every     | Looks auto-generated,   | Use 3-4 different layout |
: slide**                 : boring                  : templates                :
| **Generic blue          | Feels lazy, doesn't     | Pick topic-specific      |
: palette**               : match content           : colors                   :
| **Centered body text**  | Hard to scan, looks     | Left-align all body text |
:                         : unprofessional          :                          :
| **Text-only slides**    | Forgettable, no visual  | Add image, table, or     |
:                         : anchor                  : icon                     :
| **Too many bullets**    | Audience stops reading  | Max 5-6 bullets, then    |
:                         : after 5                 : split                    :
| **Tiny text (<12pt)**   | Unreadable on           | Minimum 14pt for body    |
:                         : projectors              :                          :
| **All content at once** | Cognitive overload      | One idea per slide       |
| **Decorative vs         | Stock photos that don't | Use diagrams,            |
: functional images**     : support content         : screenshots, icons       :

### Subtle Mistakes

| Mistake                 | Why It's Bad            | Fix                      |
| ----------------------- | ----------------------- | ------------------------ |
| **Inconsistent          | Looks unpolished        | Pick one gap size: 20pt  |
: spacing**               :                         : or 30pt                  :
| **Mixing fonts          | Visual chaos            | Max 2 fonts: one header, |
: randomly**              :                         : one body                 :
| **Color as sole         | Fails for colorblind    | Reinforce with text,     |
: information**           : users                   : icons                    :
| **Forgetting speaker    | Presenter has no script | Include `set-notes` in   |
: notes**                 :                         : batch                    :
| **Styling one slide,    | Unfinished look         | Commit to styling        |
: leaving rest plain**    :                         : throughout               :
| **Elements too close to | Feels cramped           | Maintain 30pt margin     |
: edge**                  :                         :                          :
| **No `font_family`**    | Generic look, every     | Always set `font_family` |
:                         : deck identical          :                          :
| **No `background_color` | Cards look flat, no     | Use `background_color`   |
: on cards**              : visual depth            : for card layouts         :

--------------------------------------------------------------------------------

## Complete Example: 5-Slide Batch Deck

Save as `batch.json`, run `"$GSLIDES" mutate create --title "..."` then
`"$GSLIDES" mutate batch PRES_ID -f batch.json`:

```json
[
  {"op":"set-background","slide":"p","color":"#1E2761"},
  {"op":"add-textbox","slide":"p","text":"Project Alpha","x":60,"y":120,"width":600,"height":80,"font_size":48,"bold":true,"color":"#FFFFFF","font_family":"Roboto","alignment":"center"},
  {"op":"add-textbox","slide":"p","text":"Q4 2024 Review & Roadmap","x":60,"y":210,"width":600,"height":30,"font_size":20,"color":"#CADCFC","font_family":"Roboto","alignment":"center"},
  {"op":"add-shape","slide":"p","shape_type":"RECTANGLE","x":260,"y":340,"width":200,"height":4,"background_color":"#CADCFC"},
  {"op":"set-notes","slide":"p","text":"Welcome. Introduce team and agenda."},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_1"},
  {"op":"set-background","slide":"SLIDE_1","color":"#F2F2F2"},
  {"op":"add-textbox","slide":"SLIDE_1","text":"Key Metrics","x":30,"y":15,"width":660,"height":45,"font_size":36,"bold":true,"color":"#1E2761","font_family":"Roboto"},
  {"op":"add-table","slide":"SLIDE_1","rows":4,"cols":3,"id":"TABLE_1"},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_2"},
  {"op":"set-background","slide":"SLIDE_2","color":"#065A82"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"New Features","x":30,"y":15,"width":660,"height":45,"font_size":36,"bold":true,"color":"#FFFFFF","font_family":"Roboto"},
  {"op":"add-textbox","slide":"SLIDE_2","text":"Batch Operations\nReduce API calls by 10x","x":30,"y":80,"width":310,"height":280,"font_size":14,"color":"#FFFFFF","font_family":"Roboto","line_spacing":160},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_3"},
  {"op":"set-background","slide":"SLIDE_3","color":"#1E2761"},
  {"op":"add-textbox","slide":"SLIDE_3","text":"87%","x":60,"y":80,"width":600,"height":120,"font_size":72,"bold":true,"color":"#FFFFFF","font_family":"Roboto","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_3","text":"of agent tasks complete in under 30 seconds","x":60,"y":210,"width":600,"height":40,"font_size":18,"color":"#CADCFC","font_family":"Roboto","alignment":"center"},

  {"op":"add-slide","layout":"BLANK","id":"SLIDE_4"},
  {"op":"set-background","slide":"SLIDE_4","color":"#990011"},
  {"op":"add-textbox","slide":"SLIDE_4","text":"Thank You","x":60,"y":120,"width":600,"height":80,"font_size":48,"bold":true,"color":"#FFFFFF","font_family":"Montserrat","alignment":"center"},
  {"op":"add-textbox","slide":"SLIDE_4","text":"Questions? → team@example.com","x":60,"y":225,"width":600,"height":30,"font_size":16,"color":"#FCF6F5","font_family":"Montserrat","alignment":"center"}
]
```

--------------------------------------------------------------------------------

## Quick Checklist

Before considering a presentation complete, verify:

-   [ ] **Every textbox has `--color` set** (no default black)
-   [ ] **Background + text contrast ratio ≥ 4.5:1** for body text
-   [ ] **At least 3 different layout structures** across the deck
-   [ ] **Every slide has a visual element** (image, table, icon, shape)
-   [ ] **No accent lines under titles**
-   [ ] **Body text is left-aligned** (only titles centered)
-   [ ] **Title text is 36pt+ bold** and body is 14-16pt
-   [ ] **Margins ≥ 30pt from all edges**
-   [ ] **Speaker notes on every slide** (even if brief)
-   [ ] **Color palette matches the topic** (not generic blue)
-   [ ] **Max 5-6 bullets per slide**
-   [ ] **Consistent spacing** (pick 20pt or 30pt gaps)
