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

The Gemfile depends on the **`github-pages`** gem rather than on `jekyll`
directly. Pages ignores this Gemfile and builds with its own pinned toolchain,
so matching it here keeps local, CI and production on the same Jekyll version.
`Gemfile.lock` is intentionally not committed: the old one was pinned to
Windows-only platforms and broke Linux CI, and Pages resolves its own versions
anyway.

## Continuous integration

[`.github/workflows/build.yml`](.github/workflows/build.yml) runs on every push
and pull request. It does not deploy — Pages still publishes on its own — it
just catches the things that would otherwise break the live site silently:

- **Stylesheet is current.** Recompiles Tailwind and fails if
  `css/tailwind.css` differs from what is committed. This is the easiest
  mistake to make: change a class, forget `npm run css`, and the live site
  silently keeps the old styles.
- **Jekyll build.** Installs the `github-pages` gem and builds with
  `--strict_front_matter`, so a malformed front matter block fails instead of
  silently dropping a page.
- **Link check.** [`script/check-links.mjs`](script/check-links.mjs) walks the
  built `_site` and verifies every internal link, image and `#anchor` resolves,
  and that no link is left as a bare `#`. Run it yourself with:

  ```bash
  node script/check-links.mjs _site
  ```

  It is dependency-free and does not touch the network, so it is fast and
  deterministic. External URLs are not checked.

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
