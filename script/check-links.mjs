#!/usr/bin/env node
/*
 * Internal link and asset checker for the built site.
 *
 *   node script/check-links.mjs [siteDir]      (default: _site)
 *
 * Verifies, across every built HTML page:
 *   - internal href/src targets resolve to a file that exists
 *   - in-page fragments (#id, page.html#id) point at an id that exists
 *   - no link is left as a bare "#" placeholder
 *
 * Deliberately dependency-free: html-proofer would be the obvious tool, but it
 * fights the github-pages gem over pinned nokogiri versions. External URLs are
 * not requested - this stays fast, offline, and deterministic in CI.
 */

import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, resolve, dirname, posix } from 'node:path';

const siteDir = resolve(process.argv[2] ?? '_site');

if (!existsSync(siteDir)) {
  console.error(`check-links: site directory not found: ${siteDir}`);
  console.error('Build the site first (bundle exec jekyll build).');
  process.exit(2);
}

/** Every .html file under the built site. */
function htmlFiles(dir) {
  const found = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) found.push(...htmlFiles(full));
    else if (entry.endsWith('.html')) found.push(full);
  }
  return found;
}

/** Site-root-relative URL path for a built file, e.g. /faq.html */
const toUrlPath = (file) =>
  '/' + file.slice(siteDir.length + 1).split(/[\\/]/).join('/');

const pages = htmlFiles(siteDir);
const idsByPage = new Map();   // url path -> Set of element ids
const problems = [];

// Pass 1: collect every id on every page, so fragments can be resolved.
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  const ids = new Set();
  for (const match of html.matchAll(/\sid=["']([^"']+)["']/g)) ids.add(match[1]);
  idsByPage.set(toUrlPath(file), ids);
}

const EXTERNAL = /^(https?:|mailto:|tel:|data:|javascript:)/i;

/** Resolve a link to a path on disk, following directory-index conventions. */
function resolveTarget(urlPath) {
  const rel = decodeURIComponent(urlPath.replace(/^\//, ''));
  const candidates = rel === ''
    ? ['index.html']
    : [rel, join(rel, 'index.html'), `${rel}.html`];
  for (const candidate of candidates) {
    const full = join(siteDir, candidate);
    if (existsSync(full) && statSync(full).isFile()) {
      return '/' + candidate.split(/[\\/]/).join('/');
    }
  }
  return null;
}

// Pass 2: check each link.
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  const from = toUrlPath(file);
  const pageDir = posix.dirname(from);

  for (const match of html.matchAll(/\s(?:href|src)=["']([^"']*)["']/g)) {
    const raw = match[1].trim();

    if (raw === '') continue;
    if (EXTERNAL.test(raw)) continue;
    if (raw.startsWith('//')) continue;          // protocol-relative, external

    if (raw === '#') {
      problems.push({ from, link: raw, why: 'placeholder link goes nowhere' });
      continue;
    }

    const [pathPart, fragment] = raw.split('#');

    // Pure fragment: must exist on this page.
    if (pathPart === '') {
      if (fragment && !idsByPage.get(from)?.has(fragment)) {
        problems.push({ from, link: raw, why: `no element with id "${fragment}" on this page` });
      }
      continue;
    }

    const absolute = pathPart.startsWith('/')
      ? pathPart
      : posix.normalize(posix.join(pageDir, pathPart));

    const target = resolveTarget(absolute);
    if (!target) {
      problems.push({ from, link: raw, why: `target not found: ${absolute}` });
      continue;
    }

    if (fragment && target.endsWith('.html')) {
      const ids = idsByPage.get(target);
      if (ids && !ids.has(fragment)) {
        problems.push({ from, link: raw, why: `${target} has no element with id "${fragment}"` });
      }
    }
  }
}

const linkCount = pages.reduce(
  (total, file) => total + [...readFileSync(file, 'utf8').matchAll(/\s(?:href|src)=["'][^"']*["']/g)].length,
  0,
);

if (problems.length === 0) {
  console.log(`check-links: OK - ${pages.length} pages, ${linkCount} links, no broken internal references.`);
  process.exit(0);
}

console.error(`check-links: ${problems.length} problem(s) across ${pages.length} pages:\n`);
for (const { from, link, why } of problems) {
  console.error(`  ${from}`);
  console.error(`    ${link}  ->  ${why}`);
  if (process.env.GITHUB_ACTIONS) {
    console.error(`::error::${from}: ${link} - ${why}`);
  }
}
process.exit(1);
