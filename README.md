# Jianxin Zhao — personal website

A static Jekyll site, published by GitHub Pages from the root of `master`.
The custom layouts and `assets/site.css` control the design; Minima remains the
Pages-compatible theme dependency. No JavaScript is needed for the profile pages.

## Local preview

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open http://127.0.0.1:4000. To build without serving:

```sh
bundle exec jekyll build
python3 scripts/check_site.py _site
python3 -m unittest discover -s tests
node --test tests/activity.test.mjs
```

`_site/` is generated output and must not be committed. GitHub Pages builds the
source on publication; making local edits does not publish them.

## Updating content

- `index.markdown`: introduction and selected work.
- `_data/projects.yml` and `projects/*.markdown`: project summaries and detailed
  contributions, experiments and limitations. Keep simulated results distinct
  from deployment measurements, and API pricing distinct from token usage.
- `_data/publications.yml`: complete publication list, grouped by year.
- `_data/selected_publications.yml`: the short homepage and research selection.
- `_data/books.yml`: book metadata and publisher links. Real cover images live in
  `assets/books/`; these come from the book's cover PDF and publisher catalogues.
- `about.markdown`: career history, education, teaching and contact details.
- `learning.markdown` and `cert.markdown`: coursework and verification links.
- `_config.yml`: navigation, contact details, SEO metadata and `content_updated`.
  Update the profile date when making substantive content changes.

The English two-page CV is `files/cv.pdf`; the full English CV is
`files/cv-full.pdf`. Chinese equivalents are `files/cv-zh.pdf` and
`files/cv-zh-full.pdf`. Replace these with exports from the maintained CV source;
do not edit PDF copies independently. Historical research URLs remain available.

## Codex Activity

The [Codex Activity setup](docs/codex-activity.md) documents the daily usage page,
official data collector, and local automatic publishing timer. Its collector,
JSON data, JavaScript, tests and publishing scripts are independent of the profile
refresh. Running the publishing script can commit and push activity data; it is
not needed to preview or validate the website.
