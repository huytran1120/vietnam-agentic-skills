const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const catalog = require('../docs/catalog.js');
const skills = require('../docs/skills.min.json');
const root = path.resolve(__dirname, '..');

test('all 2,921 real skills remain discoverable without filters', () => {
  assert.equal(catalog.filterSkills(skills).length, skills.length);
  assert.equal(new Set(catalog.filterSkills(skills).map(skill => skill.id)).size, skills.length);
});

test('recommendations are real skills, not fictional popularity rankings', () => {
  const sorted = catalog.filterSkills(skills);
  assert.equal(sorted[0].id, 'ui-ux-pro-max');
  assert.equal(sorted[1].id, 'code-review');
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('không phải xếp hạng lượt tải'));
  assert.ok(!html.includes('125K'));
});

test('source discovery finds all 35 Matt Pocock skills', () => {
  assert.equal(catalog.filterSkills(skills, { query: 'mattpocock/skills' }).length, 35);
  assert.ok(catalog.filterSkills(skills, { query: 'Matt Pocock' }).some(skill => skill.id === 'code-review'));
});

test('multi-token search matches across fields and ignores diacritics', () => {
  const fixtures = [{ id: 'web-test', category: 'testing', description: 'Kiểm thử giao diện', tags: ['browser'], author: 'Huy Trần' }];
  assert.equal(catalog.filterSkills(fixtures, { query: 'kiem thu browser' }).length, 1);
  assert.equal(catalog.filterSkills(fixtures, { query: 'huy tran' }).length, 1);
  assert.equal(catalog.filterSkills(fixtures, { query: 'browser absent' }).length, 0);
});

test('group filters use explicit categories and exact category remains available', () => {
  const security = catalog.filterSkills(skills, { group: 'security' });
  assert.equal(security.length, skills.filter(skill => skill.category === 'security').length);
  assert.ok(catalog.filterSkills(skills, { group: 'web' }).some(skill => skill.id === 'frontend-design'));
  for (const category of new Set(skills.map(skill => skill.category))) {
    assert.equal(catalog.filterSkills(skills, { category }).length, skills.filter(skill => skill.category === category).length);
  }
});

test('filter combinations can produce a recoverable empty state', () => {
  assert.equal(catalog.filterSkills(skills, { query: 'impossible-skill-name-8743' }).length, 0);
  assert.equal(catalog.filterSkills(skills, { category: 'security', query: 'mattpocock/skills' }).length, 0);
});

test('sorting is deterministic and does not mutate the catalog', () => {
  const before = skills.map(skill => skill.id);
  const az = catalog.filterSkills(skills, { sort: 'az' });
  const za = catalog.filterSkills(skills, { sort: 'za' });
  assert.deepEqual(az.map(skill => skill.id), za.map(skill => skill.id).reverse());
  assert.deepEqual(before, skills.map(skill => skill.id));
});

test('every agent generates the explicit target and link mode', () => {
  for (const [target] of catalog.agents) {
    assert.equal(catalog.installCommand('code-review', target), `./vas install code-review --target ${target} --mode link`);
  }
  assert.throws(() => catalog.installCommand('code-review', 'invalid'));
  assert.equal(catalog.installCommand("test'; whoami", 'codex'), "./vas install 'test'\\''; whoami' --target codex --mode link");
});

test('all links use actual catalog paths, including nested skills', () => {
  for (const skill of skills) {
    const url = catalog.skillUrl(skill);
    assert.ok(url.startsWith('https://github.com/huytran1120/vietnam-agentic-skills/blob/main/skills/'));
    assert.ok(url.endsWith('/SKILL.md'));
    assert.ok(fs.existsSync(path.join(root, skill.path, 'SKILL.md')));
  }
  assert.equal(catalog.skillUrl({ id: 'x', path: 'skills/nested/x' }), 'https://github.com/huytran1120/vietnam-agentic-skills/blob/main/skills/nested/x/SKILL.md');
  assert.throws(() => catalog.skillUrl({ id: 'x', path: 'skills/../outside' }));
});

test('upstream links cannot be replaced by unrelated or executable URLs', () => {
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'javascript:alert(1)' }), 'https://github.com/mattpocock/skills');
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'https://github.com/mattpocock/skills-evil/x' }), 'https://github.com/mattpocock/skills');
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'https://github.com/mattpocock/skills/tree/main/pr' }), 'https://github.com/mattpocock/skills/tree/main/pr');
  assert.equal(catalog.sourceUrl({}), null);
});

test('the static page ships local assets, structured data and accessible controls', () => {
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(!html.includes('cdn.tailwindcss.com'));
  assert.ok(!html.includes('fonts.googleapis.com'));
  for (const match of html.matchAll(/(?:src|href)="\.\/([^"#]+)"/g)) {
    assert.ok(fs.existsSync(path.join(root, 'docs', match[1])), match[1]);
  }
  for (const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    assert.doesNotThrow(() => JSON.parse(match[1]));
  }
  assert.ok(html.includes('role="search"'));
  assert.ok(html.includes('aria-live="polite"'));
  assert.ok(html.includes('<noscript>'));
  assert.ok(html.includes('id="retry-load"'));
  assert.ok(html.includes('id="manual-copy"'));
});

function browserRuntime(fetch) {
  const elements = new Map();
  const errors = [];
  const document = {
    getElementById(id) {
      if (!elements.has(id)) {
        const classes = new Set();
        elements.set(id, {
          hidden: ['error-state', 'empty-state'].includes(id),
          textContent: '',
          innerHTML: '',
          value: '',
          attributes: new Map(),
          listeners: new Map(),
          addEventListener(name, handler) { this.listeners.set(name, handler); },
          setAttribute(name, value) { this.attributes.set(name, value); },
          classList: {
            toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); }
          }
        });
      }
      return elements.get(id);
    },
    querySelectorAll: () => [],
    addEventListener() {}
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'docs/catalog.js'), 'utf8'), {
    document, fetch, console: { error: (...args) => errors.push(args) },
    setTimeout, clearTimeout
  });
  return { document, elements, errors };
}

test('an initial HTTP failure shows an explicit error and retry recovers', async () => {
  let requests = 0;
  const runtime = browserRuntime(async () => {
    requests++;
    return requests === 1 ? { ok: false, status: 503 } : { ok: true, json: async () => skills };
  });
  await new Promise(setImmediate);
  assert.equal(runtime.elements.get('error-state').hidden, false);
  assert.equal(runtime.elements.get('empty-state').hidden, true);
  assert.equal(runtime.elements.get('skills-results').attributes.get('aria-busy'), 'false');
  assert.equal(runtime.errors.length, 1);
  await runtime.elements.get('retry-load').listeners.get('click')();
  assert.equal(runtime.elements.get('error-state').hidden, true);
  assert.ok(runtime.elements.get('results-status').textContent.includes('2,921'));
});

test('search typed while loading is applied once the catalog arrives', async () => {
  let release;
  const runtime = browserRuntime(() => new Promise(resolve => { release = resolve; }));
  const input = runtime.elements.get('search-input');
  input.listeners.get('input')({ target: { value: 'mattpocock/skills' } });
  assert.equal(runtime.elements.get('empty-state').hidden, true);
  assert.equal(runtime.elements.get('skills-results').attributes.get('aria-busy'), 'true');
  release({ ok: true, json: async () => skills });
  await new Promise(setImmediate);
  assert.ok(runtime.elements.get('results-status').textContent.includes('35'));
  assert.equal(runtime.elements.get('loading-state').hidden, true);
});

test('malformed catalog data never turns into a success-shaped empty state', async () => {
  for (const data of [{ invalid: true }, [], [{ id: 'bad', category: 'test', tags: 'not-an-array' }]]) {
    const runtime = browserRuntime(async () => ({ ok: true, json: async () => data }));
    await new Promise(setImmediate);
    assert.equal(runtime.elements.get('error-state').hidden, false);
    assert.equal(runtime.elements.get('empty-state').hidden, true);
    assert.equal(runtime.errors.length, 1);
  }
});
