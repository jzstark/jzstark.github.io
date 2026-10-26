#!/usr/bin/env python3
"""Check generated profile HTML for broken local links and missing metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.errors = [], set(), []
        self.h1 = 0
        self.in_main_nav = False
        self.main_links = []
        self.description = False
        self.canonical = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'nav':
            self.in_main_nav = attrs.get('aria-label') == 'Main navigation'
        if tag == 'a' and self.in_main_nav:
            self.main_links.append(attrs.get('href'))
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = bool(attrs.get('content', '').strip())
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href', '').startswith('https://jianxin.ocaml.xyz/')
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('image lacks alt attribute')
        key = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script') else None
        if key and attrs.get(key):
            self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_main_nav = False


def check(root):
    pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
    errors = []
    links = 0
    for path, page in pages.items():
        name = path.relative_to(root).as_posix()
        url = '/' + name.removesuffix('index.html')
        issues = list(page.errors)
        if '/activity/' not in page.main_links:
            issues.append('Codex Activity missing from main navigation')
        if page.h1 != 1:
            issues.append(f'expected one h1, found {page.h1}')
        if not page.description or not page.canonical:
            issues.append('missing description or canonical URL')
        for href in page.links:
            parsed = urlsplit(href)
            # Fully qualified links include other independently hosted projects.
            if parsed.scheme or parsed.netloc:
                continue
            target_url = urlsplit(urljoin(url, href))
            target = root / unquote(target_url.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            links += 1
            if not target.is_file():
                issues.append(f'missing link target: {href}')
            elif target_url.fragment and target in pages:
                fragment = unquote(target_url.fragment)
                if fragment not in pages[target].ids:
                    issues.append(f'missing anchor: {href}')
        errors.extend(f'{name}: {issue}' for issue in issues)
    for error in errors:
        print(error, file=sys.stderr)
    print(f'Checked {len(pages)} HTML pages and {links} local links; {len(errors)} errors.')
    return bool(errors) or not pages


if __name__ == '__main__':
    sys.exit(check(Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()))
