/* Catalog logic is shared with the dependency-free Node regression tests. */
(function () {
  'use strict';
  const repository = 'https://github.com/huytran1120/vietnam-agentic-skills';
  const agents = [
    ['antigravity', 'Antigravity', 'A'], ['codex', 'Codex', 'Co'],
    ['claude', 'Claude', 'Cl'], ['cursor', 'Cursor', 'Cu'],
    ['windsurf', 'Windsurf', 'W'], ['cline', 'Cline', 'C'],
    ['copilot', 'Copilot', 'Gh'], ['all', 'Tất cả', 'All']
  ];
  const groups = [
    { id: 'all', label: 'Tất cả kỹ năng', categories: [] },
    { id: 'web', label: 'Phát triển web', categories: ['front-end', 'frontend', 'web-development', 'full-stack', 'fullstack', 'web'] },
    { id: 'development', label: 'Development', categories: ['development'] },
    { id: 'devops', label: 'DevOps', categories: ['devops', 'ci-cd'] },
    { id: 'testing', label: 'Kiểm thử', categories: ['testing', 'test-automation'] },
    { id: 'security', label: 'Bảo mật', categories: ['security'] },
    { id: 'data-ai', label: 'Dữ liệu & AI', categories: ['ai-ml', 'data', 'data-science', 'database'] },
    { id: 'design', label: 'UI/UX & Design', categories: ['design', 'front-end', 'frontend', '3d', '3d-web'] },
    { id: 'cloud', label: 'Cloud', categories: ['cloud'] },
    { id: 'workflow', label: 'Quy trình & tiện ích', categories: ['workflow', 'productivity', 'automation'] }
  ];
  const recommended = ['ui-ux-pro-max', 'code-review', 'impeccable', 'webapp-testing', 'frontend-design', 'research', 'landing-page-design', 'writing-for-agents', 'setup-pre-commit', 'web-performance-optimization'];
  const showcases = [
    ['landing-page-design', 'Landing page design', 'Chiến lược nội dung và thiết kế landing page.', 'landing-page-design.svg', 'design'],
    ['ui-ux-pro-max', 'UI/UX Pro Max', 'Tra cứu bảng màu, font chữ và design system.', 'ui-ux-pro-max.svg', 'design'],
    ['impeccable', 'Impeccable', 'Tinh chỉnh thiết kế và chất lượng giao diện.', 'impeccable.svg', 'design'],
    ['blender-mcp', 'Blender & Three.js', 'Quy trình 3D với Blender MCP và img2threejs.', 'blender-and-3d.svg', '3d'],
    ['hyperframes', 'Video & motion', 'Video bằng code với HyperFrames và Video Shotcraft.', 'video-and-motion.svg', 'video'],
    ['diagram-design', 'Diagram design', 'Sơ đồ kiến trúc bằng HTML và SVG.', 'diagram-design.svg', 'cloud'],
    ['chrome-devtools', 'Chrome DevTools', 'Chẩn đoán hiệu năng và hành vi trình duyệt.', 'chrome-devtools.svg', 'cloud'],
    ['bigquery-sql', 'BigQuery SQL', 'Tối ưu truy vấn, phân vùng và chi phí dữ liệu.', 'bigquery-sql.svg', 'cloud'],
    ['firebase-firestore', 'Firebase Firestore', 'Thiết kế NoSQL, security rules và index.', 'firebase-firestore.svg', 'cloud'],
    ['alphafold-database-fetch-and-analyze', 'AlphaFold', 'Tra cứu và phân tích cấu trúc protein.', 'alphafold-science.svg', 'cloud']
  ];

  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  }
  function matchesGroup(skill, groupId) {
    const group = groups.find(item => item.id === groupId);
    return groupId === 'all' || Boolean(group && group.categories.includes(skill.category));
  }
  function filterSkills(skills, { query = '', group = 'all', category = 'all', sort = 'recommended' } = {}) {
    const words = normalize(query).trim().split(/\s+/).filter(Boolean);
    const matches = skills.filter(skill => {
      if (!matchesGroup(skill, group) || (category !== 'all' && skill.category !== category)) return false;
      const text = normalize([skill.id, skill.name, skill.description, skill.category, skill.source, skill.source_repo, skill.author, ...(skill.tags || [])].join(' '));
      return words.every(word => text.includes(word));
    });
    return matches.sort((a, b) => {
      if (sort === 'recommended') {
        const aRank = recommended.indexOf(a.id);
        const bRank = recommended.indexOf(b.id);
        const difference = (aRank < 0 ? recommended.length : aRank) - (bRank < 0 ? recommended.length : bRank);
        if (difference) return difference;
      }
      return a.id.localeCompare(b.id, 'en') * (sort === 'za' ? -1 : 1);
    });
  }
  function shellQuote(value) {
    return /^[a-zA-Z0-9_./-]+$/.test(value) ? value : "'" + value.replace(/'/g, "'\\''") + "'";
  }
  function installCommand(id, target) {
    if (!agents.some(agent => agent[0] === target)) throw new Error('Agent không được hỗ trợ');
    return `./vas install ${shellQuote(id)} --target ${target} --mode link`;
  }
  function skillUrl(skill) {
    const path = String(skill.path || `skills/${skill.id}`).replace(/\/SKILL\.md$/, '');
    if (!path.startsWith('skills/') || path.split('/').some(part => !part || part === '.' || part === '..' || part.includes('\\'))) {
      throw new Error(`Đường dẫn skill không hợp lệ: ${skill.id}`);
    }
    return `${repository}/blob/main/${path.split('/').map(encodeURIComponent).join('/')}/SKILL.md`;
  }
  function sourceUrl(skill) {
    if (!/^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$/.test(skill.source_repo || '')) return null;
    const root = `https://github.com/${skill.source_repo}`;
    return String(skill.source || '').startsWith(root + '/') ? skill.source : root;
  }
  function escapeHtml(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  }
  const api = { normalize, matchesGroup, filterSkills, installCommand, skillUrl, sourceUrl, groups, agents };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const state = { skills: [], query: '', group: 'all', category: 'all', sort: 'recommended', target: 'antigravity', view: 'list', page: 1, selected: null, loaded: false };
  const pageSize = 18;
  const byId = id => document.getElementById(id);
  const icon = name => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const count = number => number.toLocaleString('en-US');
  let toastTimer;
  let copyReturnFocus = null;
  let loadingPromise = null;

  function toast(message) {
    clearTimeout(toastTimer);
    byId('toast').textContent = message;
    byId('toast').hidden = false;
    toastTimer = setTimeout(() => { byId('toast').hidden = true; }, 3500);
  }
  async function copy(text, button) {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard API không khả dụng');
      await navigator.clipboard.writeText(text);
      toast('Đã sao chép lệnh. Chạy trong terminal của bạn.');
    } catch (error) {
      console.warn('Không thể sao chép tự động:', error);
      copyReturnFocus = button;
      byId('manual-copy').hidden = false;
      byId('manual-copy-text').value = text;
      byId('manual-copy-text').focus();
      byId('manual-copy-text').select();
    }
  }
  function closeManualCopy() {
    byId('manual-copy').hidden = true;
    if (copyReturnFocus && copyReturnFocus.isConnected) copyReturnFocus.focus();
  }
  function renderNavigation() {
    const buttons = groups.map(group => {
      const total = state.skills.filter(skill => matchesGroup(skill, group.id)).length;
      return `<button type="button" data-group="${group.id}" aria-pressed="${state.group === group.id && state.category === 'all'}"><span>${group.label}</span><span>${count(total)}</span></button>`;
    });
    byId('category-navigation').innerHTML = buttons.join('');
    byId('category-pills').innerHTML = groups.slice(0, 9).map(group => `<button type="button" data-group="${group.id}" aria-pressed="${state.group === group.id && state.category === 'all'}">${group.label === 'Development' ? 'Lập trình' : group.label}</button>`).join('');
  }
  function updateNavigation() {
    document.querySelectorAll('[data-group]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.group === state.group && state.category === 'all'));
    });
    byId('category-select').value = state.category;
  }
  function renderCategories() {
    const counts = new Map();
    state.skills.forEach(skill => counts.set(skill.category || 'general', (counts.get(skill.category || 'general') || 0) + 1));
    byId('category-select').innerHTML = `<option value="all">Tất cả ${counts.size} danh mục</option>` +
      [...counts].sort(([a], [b]) => a.localeCompare(b)).map(([category, total]) => `<option value="${escapeHtml(category)}">${escapeHtml(category)} (${count(total)})</option>`).join('');
  }
  function provenance(skill) {
    const source = sourceUrl(skill);
    return `<div class="skill-provenance">
      ${skill.author ? `<p>Tác giả: ${escapeHtml(skill.author)}</p>` : ''}
      ${source ? `<p>Nguồn: <a href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">${escapeHtml(skill.source_repo)}</a></p>` : ''}
      ${skill.license ? `<p>Giấy phép: ${escapeHtml(skill.license)}</p>` : '<p>Giấy phép: xem tài liệu trong skill.</p>'}
      <p class="risk-label">Metadata risk: ${escapeHtml(skill.risk || 'unknown')}</p>
    </div>`;
  }
  function installation(skill) {
    const currentAgent = agents.find(a => a[0] === state.target) || agents[0];
    const isAntigravity = state.target === 'antigravity';
    const targetDisplay = isAntigravity ? 'Antigravity (Mặc định)' : currentAgent[1];
    return `<div class="install-panel" id="install-${escapeHtml(skill.id)}">
      <div class="install-heading"><strong>Lệnh cài đặt cho ${escapeHtml(currentAgent[1])}</strong><button data-close-skill="${escapeHtml(skill.id)}" aria-label="Thu gọn ${escapeHtml(skill.id)}">×</button></div>
      <span class="agent-label">Chọn agent của bạn (Đang chọn: <strong>${escapeHtml(targetDisplay)}</strong>)</span>
      <div class="agent-options" role="group" aria-label="Agent cài đặt cho ${escapeHtml(skill.id)}">
        ${agents.map(([id, label, mark]) => `<button class="agent-option" data-agent="${id}" aria-pressed="${id === state.target}"><span aria-hidden="true">${mark}</span>${label}</button>`).join('')}
      </div>
      <div class="command-box"><code>${escapeHtml(installCommand(skill.id, state.target))}</code><button class="button primary" data-copy-skill="${escapeHtml(skill.id)}">${icon('copy')}Sao chép</button></div>
      <p class="install-footnote">Chạy tại thư mục VAS đã clone. Chưa clone? <a href="#quickstart">Xem hướng dẫn</a>.</p>
      <div class="install-links"><a href="${escapeHtml(skillUrl(skill))}" target="_blank" rel="noopener noreferrer">Đọc SKILL.md ↗</a><button class="text-button" data-show-command="${escapeHtml(skill.id)}">Sao chép lệnh xem playbook</button></div>
    </div>`;
  }
  function renderResults() {
    if (!state.loaded) return;
    const filtered = filterSkills(state.skills, state);
    const visible = filtered.slice(0, state.page * pageSize);
    const categoryLabel = state.category !== 'all' ? state.category : groups.find(group => group.id === state.group).label;
    byId('results-title').textContent = categoryLabel;
    byId('results-status').textContent = `Tìm thấy ${count(filtered.length)} kỹ năng${state.query ? ` cho “${state.query}”` : ''}`;
    byId('clear-search').hidden = !state.query;
    const hasFilters = Boolean(state.query || state.group !== 'all' || state.category !== 'all');
    byId('filter-summary').hidden = !hasFilters;
    byId('filter-description').textContent = state.category !== 'all' ? `Danh mục: ${state.category}` : `Đang lọc: ${categoryLabel}`;
    byId('empty-state').hidden = filtered.length !== 0;
    byId('skills-results').classList.toggle('is-grid', state.view === 'grid');
    byId('skills-results').innerHTML = visible.map((skill, index) => {
      const selected = skill.id === state.selected;
      const tags = [skill.category || 'general', ...(skill.tags || []).filter(tag => tag !== skill.category)].slice(0, 2);
      return `<article class="skill-row${selected ? ' is-open' : ''}" data-skill="${escapeHtml(skill.id)}">
        <span class="skill-number" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span>
        <div class="skill-symbol" aria-hidden="true">${icon(skill.category === 'design' ? 'grid' : 'code')}</div>
        <div class="skill-info">
          <h3><button class="skill-name" data-open-skill="${escapeHtml(skill.id)}" aria-expanded="${selected}"${selected ? ` aria-controls="install-${escapeHtml(skill.id)}"` : ''}>${escapeHtml(skill.id)}</button></h3>
          <div class="skill-tags">${tags.map(tag => `<span class="skill-tag">${escapeHtml(tag)}</span>`).join('')}</div>
          ${selected ? `<p class="skill-summary">${escapeHtml(skill.description || 'Xem hướng dẫn đầy đủ trong SKILL.md.')}</p><details class="description-details"><summary>Mô tả đầy đủ</summary><p class="skill-full-description">${escapeHtml(skill.description || 'Xem hướng dẫn đầy đủ trong SKILL.md.')}</p></details>${provenance(skill)}` : ''}
        </div>
        ${selected ? installation(skill) : `<p class="skill-description">${escapeHtml(skill.description || 'Xem hướng dẫn đầy đủ trong SKILL.md.')}</p><button class="icon-button skill-open" data-open-skill="${escapeHtml(skill.id)}" aria-label="Xem chi tiết và lệnh cài ${escapeHtml(skill.id)}" aria-expanded="false">${icon('arrow')}</button>`}
      </article>`;
    }).join('');
    byId('pagination-controls').hidden = visible.length === 0;
    byId('pagination-status').textContent = `Đang hiển thị ${count(visible.length)} / ${count(filtered.length)} kỹ năng`;
    byId('load-more').hidden = visible.length >= filtered.length;
    document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === state.view)));
    updateNavigation();
  }
  function applyFilters() {
    state.page = 1;
    renderResults();
  }
  function resetFilters() {
    state.query = '';
    state.group = 'all';
    state.category = 'all';
    byId('search-input').value = '';
    applyFilters();
    byId('search-input').focus({ preventScroll: true });
  }
  function focusSearch() {
    byId('search-input').focus({ preventScroll: true });
    byId('catalog').scrollIntoView({ block: 'start', behavior: 'instant' });
  }
  function setTarget(target) {
    state.target = target;
    byId('agent-select').value = target;
    byId('quickstart-command').textContent = installCommand('ui-ux-pro-max', target);
    renderResults();
  }
  function renderShowcase(category = 'all') {
    byId('showcase-grid').innerHTML = showcases.filter(item => category === 'all' || item[4] === category).map(([id, name, description, image]) => `
      <article class="showcase-card"><img src="./assets/demos/${image}" alt="Minh họa ${escapeHtml(name)}" width="480" height="300" loading="lazy">
      <h3><button data-discover="${id}">${name} <span aria-hidden="true">↗</span></button></h3><p>${description}</p></article>`).join('');
    document.querySelectorAll('[data-showcase]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.showcase === category)));
  }
  async function loadCatalog() {
    if (loadingPromise) return loadingPromise;
    byId('loading-state').hidden = false;
    byId('error-state').hidden = true;
    byId('empty-state').hidden = true;
    byId('skills-results').setAttribute('aria-busy', 'true');
    byId('results-status').textContent = 'Đang tải danh mục…';
    loadingPromise = (async () => {
      try {
        const response = await fetch('./skills.min.json');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!Array.isArray(data) || data.length === 0 || data.some(skill => !skill || typeof skill.id !== 'string' || !skill.id || typeof skill.category !== 'string' || (skill.tags && (!Array.isArray(skill.tags) || skill.tags.some(tag => typeof tag !== 'string'))))) {
          throw new Error('Dữ liệu catalog không hợp lệ');
        }
        data.forEach(skillUrl);
        state.skills = data;
        state.loaded = true;
        state.selected = recommended.find(id => data.some(skill => skill.id === id)) || data[0].id;
        renderNavigation();
        renderCategories();
        applyFilters();
        return true;
      } catch (error) {
        console.error('Lỗi tải danh mục:', error);
        byId('error-state').hidden = false;
        byId('results-status').textContent = 'Không thể tải danh mục. Vui lòng thử lại.';
        return false;
      } finally {
        byId('loading-state').hidden = true;
        byId('skills-results').setAttribute('aria-busy', 'false');
        loadingPromise = null;
      }
    })();
    return loadingPromise;
  }
  async function discover(id) {
    if (!state.loaded && !(await loadCatalog())) {
      byId('error-state').scrollIntoView({ block: 'center' });
      return;
    }
    if (!state.skills.some(skill => skill.id === id)) {
      toast(`Không tìm thấy skill “${id}” trong catalog.`);
      return;
    }
    state.query = id;
    state.group = 'all';
    state.category = 'all';
    state.selected = id;
    byId('search-input').value = id;
    applyFilters();
    focusSearch();
  }

  byId('search-form').addEventListener('submit', event => event.preventDefault());
  byId('search-input').addEventListener('input', event => { state.query = event.target.value; applyFilters(); });
  byId('clear-search').addEventListener('click', () => { state.query = ''; byId('search-input').value = ''; applyFilters(); byId('search-input').focus(); });
  byId('reset-filters').addEventListener('click', resetFilters);
  byId('empty-reset').addEventListener('click', resetFilters);
  byId('focus-search').addEventListener('click', focusSearch);
  byId('retry-load').addEventListener('click', loadCatalog);
  byId('sort-select').addEventListener('change', event => { state.sort = event.target.value; applyFilters(); });
  byId('category-select').addEventListener('change', event => { state.category = event.target.value; state.group = 'all'; applyFilters(); });
  byId('agent-select').addEventListener('change', event => setTarget(event.target.value));
  byId('load-more').addEventListener('click', () => {
    const firstNew = state.page * pageSize;
    state.page++;
    renderResults();
    const nextButton = byId('skills-results').querySelectorAll('.skill-name')[firstNew];
    if (nextButton) nextButton.focus({ preventScroll: true });
  });
  byId('matt-collection').addEventListener('click', () => {
    state.query = 'mattpocock/skills';
    state.group = 'all';
    state.category = 'all';
    byId('search-input').value = state.query;
    applyFilters();
    focusSearch();
  });
  byId('menu-toggle').addEventListener('click', () => {
    const menu = byId('mobile-menu');
    menu.hidden = !menu.hidden;
    byId('menu-toggle').setAttribute('aria-expanded', String(!menu.hidden));
  });
  byId('mobile-menu').addEventListener('click', event => {
    if (event.target.closest('a')) {
      byId('mobile-menu').hidden = true;
      byId('menu-toggle').setAttribute('aria-expanded', 'false');
    }
  });
  byId('theme-toggle').addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    byId('theme-toggle').setAttribute('aria-pressed', String(dark));
    byId('theme-toggle').setAttribute('aria-label', dark ? 'Bật giao diện sáng' : 'Bật giao diện tối');
  });
  byId('close-manual-copy').addEventListener('click', closeManualCopy);
  document.addEventListener('keydown', event => {
    const editing = event.target.closest('input, textarea, select, [contenteditable="true"]');
    if ((event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey)) || (event.key === '/' && !editing)) {
      event.preventDefault();
      focusSearch();
    } else if (event.key === 'Escape') {
      if (!byId('manual-copy').hidden) closeManualCopy();
      else if (!byId('mobile-menu').hidden) {
        byId('mobile-menu').hidden = true;
        byId('menu-toggle').setAttribute('aria-expanded', 'false');
        byId('menu-toggle').focus();
      } else if (event.target === byId('search-input')) {
        state.query = '';
        byId('search-input').value = '';
        applyFilters();
      }
    }
  });
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.group) {
      state.group = button.dataset.group;
      state.category = 'all';
      applyFilters();
    } else if (button.dataset.view) {
      state.view = button.dataset.view;
      renderResults();
    } else if (button.dataset.openSkill || button.dataset.closeSkill) {
      const id = button.dataset.openSkill || button.dataset.closeSkill;
      state.selected = state.selected === id ? null : id;
      renderResults();
      const row = [...byId('skills-results').children].find(element => element.dataset.skill === id);
      if (row) row.querySelector('.skill-name').focus({ preventScroll: true });
    } else if (button.dataset.agent) {
      const target = button.dataset.agent;
      setTarget(target);
      const selected = byId('skills-results').querySelector(`[data-agent="${target}"]`);
      if (selected) selected.focus({ preventScroll: true });
    } else if (button.dataset.copySkill) {
      copy(installCommand(button.dataset.copySkill, state.target), button);
    } else if (button.dataset.showCommand) {
      copy(`./vas show ${shellQuote(button.dataset.showCommand)}`, button);
    } else if (button.dataset.copyElement) {
      copy(byId(button.dataset.copyElement).textContent, button);
    } else if (button.dataset.discover) {
      discover(button.dataset.discover);
    } else if (button.dataset.showcase) {
      renderShowcase(button.dataset.showcase);
    }
  });
  renderShowcase();
  loadCatalog();
})();
