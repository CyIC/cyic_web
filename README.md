# cyic.club

Website for the [Cypress Investment Club](https://cyic.club), built with Jekyll
and Tailwind CSS and hosted on GitHub Pages.

## How the build works

GitHub Pages builds the Jekyll site natively — there is no Actions workflow and
nothing to configure. The one wrinkle is Tailwind: Pages cannot run it, so the
compiled stylesheet at `css/tailwind.css` **is committed to the repository**.

That means: if you change any class in a template, you must rebuild the CSS and
commit the result, or your change will not appear on the live site.

```bash
npm install
npm run css
```

Use `npm run css:watch` while you are working. Node is only needed for this
step; it is not needed to serve or deploy the site.

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

Run `npm run css:watch` in a second terminal so stylesheet changes pick up as
you edit.

## Where things live

| Path | What it is |
| --- | --- |
| `src/tailwind.css` | Design tokens and component classes. The real stylesheet source. |
| `css/tailwind.css` | Compiled output. Generated — never edit by hand. |
| `_data/` | Site content: nav, goals, steps, facts, principles, FAQ, resources. |
| `_includes/` | Head, nav, footer, CTA band, inline SVG icons and logo. |
| `_layouts/` | `default.html` (chrome) and `page.html` (inner page header). |
| `js/site.js` | The only script: theme toggle, mobile menu, FAQ filter. |
| `img/logo/` | Brand assets. `cyic-*.svg` are generated from `Cypress Logo Final.svg`. |

### Editing content

Most copy lives in `_data/*.yml` rather than in markup, so adding an FAQ entry
or a resource link means editing YAML, not HTML. Club facts that appear in more
than one place (the monthly minimum, the member cap, the target return) are
defined once under `club:` in `_config.yml`.

## Design notes

Brand colours were sampled from the logo artwork: maroon `#652325` and charcoal
`#222222`. The maroon ramp in `src/tailwind.css` is generated in OKLCH at the
brand hue so the steps are perceptually even.

Light and dark themes are driven by semantic custom properties (`--c-bg`,
`--c-fg`, `--c-accent`, …) redefined under `:root.dark`. The theme is resolved
before first paint by an inline script in `_includes/head.html`, which follows
the OS setting unless the visitor has chosen explicitly; `js/site.js` handles
switching afterwards. All text meets WCAG AA contrast in both themes.

The old Start Bootstrap "Creative" theme (Bootstrap 3, jQuery, Font Awesome,
wow.js) has been removed entirely. Icons are inline SVG and there are no
third-party scripts.
