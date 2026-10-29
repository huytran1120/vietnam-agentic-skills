# UI Cheatsheet

| Problem                            | Solution                                                     |
| ---------------------------------- | ------------------------------------------------------------ |
| Old timestamps read "340 days ago" | Switch to an absolute date after a week                      |
| Numbers jitter when they change    | `font-variant-numeric: tabular-nums`                         |
| Large headings look off            | Tighter tracking like `-0.02em`                              |
| Body text looks awkward            | Cap the line at about 65 characters with `max-width: 65ch`   |
| Button feels unresponsive          | `transform: scale(0.97)` on `:active`                        |
| Avatar squished into an oval       | `flex-shrink: 0` on the avatar                               |
| Gradient fade has a visible edge   | Use an eased gradient: extra color stops along an ease curve |
| Transition still feels off         | Add `filter: blur(2px)` during the transition                |
| Dropdown feels sluggish            | `ease-out` under 300ms, never `ease-in`                      |
| Popover grows from the wrong spot  | `transform-origin` at the trigger (modals stay centered)     |
| Count reads "1 members"            | Pluralize with `Intl.PluralRules`                            |

