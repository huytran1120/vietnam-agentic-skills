# Full List of Commands

This reference file contains the complete list of commands available in the
`gdocs` skill. Every command is invoked as `"$GDOCS" readonly <command>` or
`"$GDOCS" mutate <command>`.

Global flags accepted by every command: `--json`, `--ignore-sharing-checks`,
`--legacy-mode`, and `--project` (env `GDOCS_PROJECT_ID`). `-v` / `--version`
works at the root.

> [!CAUTION] Every `mutate` command writes directly to the live document as soon
> as it runs. There is no staging step and no accept/reject safety net, so
> collaborators see the change immediately. Destructive commands (`clear`,
> `delete`, `delete-doc`, `delete-tab`) require `--confirm` — read the document
> with `readonly read` or `readonly structure` before running them.

| Command                          | Description                              |
| -------------------------------- | ---------------------------------------- |
| `readonly read`                  | Read document content (supports `--tab`; |
:                                  : `--comments` inlines open comments as    :
:                                  : footnotes, default true)                 :
| `readonly info`                  | Get document info                        |
| `mutate create`                  | Create document (`--title`, `--folder`;  |
:                                  : `--pageless` defaults to true — pass     :
:                                  : `--pageless=false` for a paginated doc)  :
| `mutate copy`                    | Copy document                            |
| `mutate append`                  | Append text (supports `--tab`)           |
| `mutate insert`                  | Insert text at position (supports        |
:                                  : `--tab`)                                 :
| `mutate replace`                 | Find and replace (supports `--tab`)      |
| `mutate heading`                 | Insert heading (supports `--tab`)        |
| `mutate delete`                  | Permanently delete a content range       |
:                                  : (requires `--confirm`, supports `--tab`) :
| `mutate delete-doc`              | Delete a Google Doc permanently          |
| `mutate format-text`             | Format text range (`--start/--end`,      |
:                                  : `--text`, `--url`, `--strikethrough`,    :
:                                  : `--background-color`, `--font-family`,   :
:                                  : `--font-size`)                           :
| `mutate format-paragraph`        | Format paragraph style: `--level`,       |
:                                  : `--indent`, `--alignment`,               :
:                                  : `--space-above`, `--space-below`         :
| `mutate format-named-styles`     | Format document-wide named styles        |
:                                  : (`--style-type`                          :
:                                  : TITLE/SUBTITLE/HEADING_1..6/NORMAL_TEXT, :
:                                  : `--font-family`, `--font-size`,          :
:                                  : `--text-color`, `--weight`, `--tab`)     :
| `mutate bullets`                 | Apply or remove paragraph bullets        |
| `mutate insert-table`            | Insert a table (`--rows`, `--cols`,      |
:                                  : `--index` or `--after "text"`)           :
| `mutate insert-page-break`       | Insert page break                        |
| `mutate insert-image`            | Insert image by URL (`--replace`)        |
| `mutate insert-image-from-file`  | Insert local image (`--replace`)         |
| `mutate insert-chip`             | Insert a person smart chip (`--email`,   |
:                                  : positioned with `--after`,               :
:                                  : `--replace-text`, or `--index`; supports :
:                                  : `--tab`)                                 :
| `mutate set-alt-text`            | Set alt text on an inline image          |
:                                  : (`--image-id`, `--description`,          :
:                                  : `--title`, `--tab`)                      :
| `mutate import-md`               | Convert a markdown file to a native      |
:                                  : Google Doc (`--title`, `--folder`,       :
:                                  : `--update`, `--tab`,                     :
:                                  : `--auto-fit-tables`, `--strict-math`;    :
:                                  : `--pageless` defaults to true)           :
| `readonly parse-md`              | Parse markdown into internal JSON blocks |
:                                  : with fingerprints                        :
| `readonly pull`                  | Pull Google Doc content into a local     |
:                                  : Markdown file (supports `--tab`;         :
:                                  : `--suggestions-mode` controls how        :
:                                  : collaborators' tracked suggestions       :
:                                  : render\: `SUGGESTIONS_INLINE`,           :
:                                  : `PREVIEW_SUGGESTIONS_ACCEPTED`,          :
:                                  : `PREVIEW_WITHOUT_SUGGESTIONS`)           :
| `mutate sync`                    | Synchronize a local markdown file with a |
:                                  : Google Doc (3-way merge)                 :
| `mutate create-from-template`    | Create from template, replacing          |
:                                  : `{{KEY}}` placeholders                   :
| `mutate add-comment`             | Add comment (`--quote` to anchor,        |
:                                  : `--assignee`, supports `--tab`;          :
:                                  : `--native` defaults to true)             :
| `readonly list-comments`         | List comments and replies                |
| `mutate reply-comment`           | Reply to an existing comment             |
| `mutate resolve-comment`         | Resolve comment                          |
| `mutate delete-comment`          | Delete a comment (`delete-comment DOC_ID |
:                                  : COMMENT_ID`)                             :
| `readonly list-revisions`        | List revisions                           |
| `readonly diff-revisions`        | Diff two revisions                       |
| `readonly pull-revision`         | Download a document revision as markdown |
| `readonly export`                | Export to `pdf`, `zip`, `docx`, `txt`,   |
:                                  : `md`, or `png` (`--format`,              :
:                                  : `-o/--output`, `--tab`; `--page` is      :
:                                  : png-only)                                :
| `readonly get-url`               | Generate a shareable web URL (`--tab`,   |
:                                  : `--heading`, `--bookmark`, `--comment`,  :
:                                  : `--action`, `--export`, `--revision`,    :
:                                  : `--offline`)                             :
| `mutate share`                   | Share document with a user or domain     |
| `readonly permissions`           | List permissions                         |
| `readonly word-count`            | Count words/chars (supports `--tab`)     |
| `readonly toc`                   | Extract table of contents (supports      |
:                                  : `--tab`)                                 :
| `readonly list-tabs`             | List document tabs                       |
| `mutate create-tab`              | Create a new tab (supports `--parent`)   |
| `mutate delete-tab`              | Delete a tab (requires `--confirm`)      |
| `mutate rename-tab`              | Rename a tab                             |
| `readonly read-tab`              | Read a specific tab's text               |
| `mutate duplicate-tab`           | Duplicate an existing tab (supports      |
:                                  : `--parent`)                              :
| `mutate move-tab`                | Move a tab (supports `--parent`,         |
:                                  : `--root`, `--index`)                     :
| `readonly footnotes`             | Extract footnotes                        |
| `readonly style`                 | Show document style info (margins, page  |
:                                  : size)                                    :
| `readonly list-images`           | List inline images                       |
| `readonly download-image`        | Download an inline image by object ID    |
:                                  : (`--output` required, supports `--tab`)  :
| `readonly extract-tables`        | Extract all tables as structured JSON    |
:                                  : (supports `--tab`)                       :
| `readonly extract-links`         | Extract all links (supports `--tab`)     |
| `mutate batch`                   | Execute batch operations (`-f/--file`,   |
:                                  : `--after`, `--after-inside`, `--before`, :
:                                  : `--replace-all`, `--tab`, `--index`)     :
| `readonly structure`             | Show document structure with numbered    |
:                                  : elements (supports `--tab`, `--json`,    :
:                                  : `-v`)                                    :
| `readonly dump-body`             | Dump raw document body JSON (supports    |
:                                  : `--tab`)                                 :
| `mutate sed`                     | Sed-style operations: substitution,      |
:                                  : delete, append, insert, positional       :
:                                  : (`-e`, `-f`, `--regex`, `--dry-run`,     :
:                                  : `--tab`; `-i` is `--case-insensitive`).  :
:                                  : Replaces **all** occurrences unless      :
:                                  : `--first` is passed                      :
| `mutate clear`                   | Clear all document content (requires     |
:                                  : `--confirm`)                             :
| `mutate write`                   | Write/overwrite document from a plain    |
:                                  : text file (`-f/--file`, `--clear`,       :
:                                  : `--tab`)                                 :
| `mutate update-table`            | Find table by headers and replace data   |
:                                  : rows                                     :
| `mutate merge-cells`             | Merge table cells (`--table`, `--row`,   |
:                                  : `--col`, `--row-span`, `--col-span`)     :
| `mutate unmerge-cells`           | Unmerge previously merged table cells    |
:                                  : (`--table`, `--row`, `--col`,            :
:                                  : `--row-span`, `--col-span`)              :
| `mutate add-column`              | Insert a column into a table (`--left`   |
:                                  : for left)                                :
| `mutate delete-column`           | Delete a column from a table             |
| `mutate add-row`                 | Insert a row into a table (`--above` for |
:                                  : above)                                   :
| `mutate delete-row`              | Delete a row from a table                |
| `mutate style-table`             | Style cells of an existing table         |
:                                  : (`--table`, `--bg-color`, `--row`,       :
:                                  : `--row-span`, `--col`, `--col-span`)     :
| `mutate style-table-columns`     | Set column widths of an existing table   |
:                                  : (`--table`, `--col-widths`,              :
:                                  : `--total-width`)                         :
| `mutate auto-fit-tables`         | Auto-optimize table column widths from   |
:                                  : cell content (`--table`,                 :
:                                  : `--target-width`, `--tab`)               :
| `mutate replace-image`           | Replace an inline image by object ID     |
:                                  : **with URL**                             :
| `mutate replace-image-from-file` | Replace an inline image by object ID     |
:                                  : with a local image file                  :
| `mutate replace-image-safe`      | Replace an inline image by object ID     |
:                                  : using delete+insert to prevent cropping  :
:                                  : (requires local file)                    :
| `mutate pageless`                | Make a document pageless                 |
| `mutate rename`                  | Rename a document title                  |
