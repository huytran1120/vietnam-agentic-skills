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
    ['landing-page-design', '🚀 landing-page-design', 'Kiến trúc trang đích chuyển đổi cao & Fluid Nav', 'landing-page-design.svg', 'design'],
    ['ui-ux-pro-max', '🎨 ui-ux-pro-max', 'Hệ thống Design System, 192 bảng màu & font pairing', 'ui-ux-pro-max.svg', 'design'],
    ['impeccable', '🛡️ impeccable', 'Bộ công cụ chống AI-slop với 62 quy tắc định lượng', 'impeccable.svg', 'design'],
    ['blender-mcp', '🧊 blender-mcp & img2threejs', 'Điều khiển Blender 3D & Three.js thuần code', 'blender-and-3d.svg', '3d'],
    ['hyperframes', '🎬 video-shotcraft, hyperframes, remotion', 'Lập trình video trong React/HTML', 'video-and-motion.svg', 'video'],
    ['diagram-design', '📊 diagram-design', 'Sơ đồ kiến trúc cloud HTML+SVG', 'diagram-design.svg', 'cloud'],
    ['chrome-devtools', '🛠️ chrome-devtools', 'Gỡ lỗi LCP, rò rỉ bộ nhớ & A11y', 'chrome-devtools.svg', 'cloud'],
    ['bigquery-sql', '⚡ bigquery-sql', 'Tối ưu hóa chi phí & hiệu năng BigQuery', 'bigquery-sql.svg', 'cloud'],
    ['firebase-firestore', '🔒 firebase-firestore', 'Kiểm toán bảo mật rules & data model', 'firebase-firestore.svg', 'cloud'],
    ['alphafold-database-fetch-and-analyze', '🧬 alphafold-fetch', 'Phân tích sinh học phân tử 3D & pLDDT', 'alphafold-science.svg', 'cloud']
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
        if (words.length) {
          const relevance = skill => {
            const names = [normalize(skill.id), normalize(skill.name)];
            const phrase = normalize(query).trim();
            if (names.includes(phrase)) return 0;
            if (names.some(name => name.startsWith(phrase))) return 1;
            if (names.some(name => words.every(word => name.includes(word)))) return 2;
            const tags = normalize([skill.category, ...(skill.tags || [])].join(' '));
            if (words.every(word => tags.includes(word))) return 3;
            return 4;
          };
          const difference = relevance(a) - relevance(b);
          if (difference) return difference;
        }
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
  const targetFolders = { antigravity: '.agents/skills', codex: '.codex/skills', claude: '.claude/skills', cursor: '.cursor/skills', windsurf: '.windsurf/skills', cline: '.cline/skills', copilot: '.github/skills' };
  function installCommand(id, target, { scope = 'repository', projectPath = '' } = {}) {
    if (!agents.some(agent => agent[0] === target)) throw new Error('Agent không được hỗ trợ');
    const command = agent => `./vas install ${shellQuote(id)} --target ${agent} --mode link`;
    if (scope === 'repository') return command(target);
    if (scope === 'global') {
      if (target === 'all') throw new Error('Chọn một agent để cài toàn máy.');
      return command(target) + ' --global';
    }
    if (scope !== 'project') throw new Error('Nơi cài không được hỗ trợ.');
    let root = projectPath.trim();
    if (!root || /[\x00-\x1f\x7f]/.test(root) || !(/^(\/|[A-Za-z]:[\\/])/.test(root))) {
      throw new Error('Nhập đường dẫn tuyệt đối đến dự án, ví dụ /Users/ban/my-project hoặc C:/Projects/my-app.');
    }
    if (/^[A-Za-z]:/.test(root)) root = root.replace(/\\/g, '/');
    root = root.replace(/\/+$/, '');
    const targets = target === 'all' ? Object.keys(targetFolders) : [target];
    return targets.map(agent => command(agent) + ' --dest ' + shellQuote(`${root}/${targetFolders[agent]}`)).join('\n');
  }
  function readCatalogState(search) {
    const params = new URLSearchParams(search);
    return {
      query: params.get('q') || '', selected: params.get('skill') || null,
      target: agents.some(agent => agent[0] === params.get('agent')) ? params.get('agent') : 'antigravity',
      group: groups.some(group => group.id === params.get('group')) ? params.get('group') : 'all',
      category: params.get('category') || 'all',
      sort: ['az', 'za'].includes(params.get('sort')) ? params.get('sort') : 'recommended',
      view: params.get('view') === 'grid' ? 'grid' : 'list'
    };
  }
  function catalogParams(value) {
    const params = new URLSearchParams();
    if (value.query) params.set('q', value.query);
    if (value.selected) params.set('skill', value.selected);
    if (value.target && value.target !== 'antigravity') params.set('agent', value.target);
    if (value.group && value.group !== 'all') params.set('group', value.group);
    if (value.category && value.category !== 'all') params.set('category', value.category);
    if (value.sort && value.sort !== 'recommended') params.set('sort', value.sort);
    if (value.view === 'grid') params.set('view', 'grid');
    return params.toString();
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
  const api = { normalize, matchesGroup, filterSkills, installCommand, skillUrl, sourceUrl, groups, agents, targetFolders, readCatalogState, catalogParams };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const state = { skills: [], query: '', group: 'all', category: 'all', sort: 'recommended', target: 'antigravity', view: 'list', page: 1, selected: null, loaded: false, scope: 'project', projectPath: '' };
  if (typeof window !== 'undefined') Object.assign(state, readCatalogState(window.location.search));
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
  async function copy(text, button, message = 'Đã sao chép lệnh. Chạy trong terminal của bạn.') {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard API không khả dụng');
      await navigator.clipboard.writeText(text);
      toast(message);
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
  function commandPreview(id) {
    try { return { command: installCommand(id, state.target, state) }; }
    catch (error) { return { error: error.message }; }
  }
  function syncInstallation() {
    byId('agent-select').value = state.target;
    byId('install-scope').value = state.scope;
    byId('project-path-field').hidden = state.scope !== 'project';
    const preview = commandPreview(state.selected || 'ui-ux-pro-max');
    byId('quickstart-command').textContent = state.selected ? (preview.command || preview.error) : 'Chọn một skill trong catalog để tạo lệnh cài.';
    document.querySelectorAll('[data-copy-element="quickstart-command"]').forEach(button => { button.disabled = !state.selected || !preview.command; });
    document.querySelectorAll('[data-install-command]').forEach(code => { code.textContent = preview.command || preview.error; });
    document.querySelectorAll('[data-copy-skill]').forEach(button => { button.disabled = !preview.command; });
    byId('project-path').setAttribute('aria-invalid', String(state.scope === 'project' && Boolean(state.projectPath) && !preview.command));
    byId('install-location-help').textContent = state.scope === 'global'
      ? (state.target === 'all' ? preview.error : 'Cài vào thư mục skill toàn máy của agent đã chọn bằng --global. Giữ kho VAS tại vị trí đã clone khi dùng chế độ link.')
      : (preview.command ? 'Lệnh dùng --dest trỏ đến thư mục skill trong dự án. Đường dẫn chỉ dùng trong phiên này và không được đưa vào liên kết chia sẻ.' : preview.error);
  }
  function syncUrl(push = false) {
    if (typeof window === 'undefined' || !state.loaded) return;
    const params = catalogParams(state);
    const url = window.location.pathname + (params ? '?' + params : '') + window.location.hash;
    if (url !== window.location.pathname + window.location.search + window.location.hash) {
      window.history[push ? 'pushState' : 'replaceState'](null, '', url);
    }
  }
  function installation(skill) {
    const currentAgent = agents.find(a => a[0] === state.target) || agents[0];
    const preview = commandPreview(skill.id);
    return `<div class="install-panel" id="install-${escapeHtml(skill.id)}">
      <div class="install-heading"><strong>Lệnh cài đặt cho ${escapeHtml(currentAgent[1])}</strong><button data-close-skill="${escapeHtml(skill.id)}" aria-label="Thu gọn ${escapeHtml(skill.id)}">×</button></div>
      <label class="agent-label" for="skill-agent">Agent sử dụng</label>
      <select id="skill-agent" data-install-agent>${agents.map(([id, label]) => `<option value="${id}"${id === state.target ? ' selected' : ''}>${label}</option>`).join('')}</select>
      <p class="install-destination">${state.scope === 'global' ? 'Toàn máy' : 'Dự án cụ thể'} · <a href="#install-scope">Đổi nơi cài</a></p>
      <div class="command-box"><code data-install-command>${escapeHtml(preview.command || preview.error)}</code><button class="button primary" data-copy-skill="${escapeHtml(skill.id)}"${preview.command ? '' : ' disabled'}>${icon('copy')}Sao chép lệnh</button></div>
      <p class="install-footnote">Chạy tại thư mục VAS đã clone. Chưa clone? <a href="#quickstart">Xem hướng dẫn</a>.</p>
      <div class="install-links"><a href="${escapeHtml(skillUrl(skill))}" target="_blank" rel="noopener noreferrer">Đọc SKILL.md ↗</a><button class="text-button" data-share-skill="${escapeHtml(skill.id)}">Sao chép liên kết</button><button class="text-button" data-show-command="${escapeHtml(skill.id)}">Sao chép lệnh xem playbook</button></div>
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
    syncInstallation();
  }
  function applyFilters() {
    state.page = 1;
    if (state.loaded && !filterSkills(state.skills, state).some(skill => skill.id === state.selected)) state.selected = null;
    renderResults();
    syncUrl();
  }
  function restoreLocation() {
    Object.assign(state, readCatalogState(window.location.search));
    if (!state.skills.some(skill => skill.category === state.category)) state.category = 'all';
    if (state.selected && !state.skills.some(skill => skill.id === state.selected)) {
      toast('Skill trong liên kết không còn trong catalog. Bạn có thể tìm lại bên dưới.');
      state.selected = null;
    }
    const params = new URLSearchParams(window.location.search);
    if (state.selected && !params.has('q') && !params.has('group') && !params.has('category')) state.query = state.selected;
    byId('search-input').value = state.query;
    byId('sort-select').value = state.sort;
    const selectedIndex = filterSkills(state.skills, state).findIndex(skill => skill.id === state.selected);
    state.page = Math.max(1, Math.ceil((selectedIndex + 1) / pageSize));
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
    renderResults();
    syncUrl();
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
        if (typeof window === 'undefined' || !new URLSearchParams(window.location.search).has('skill')) {
          state.selected = recommended.find(id => data.some(skill => skill.id === id)) || data[0].id;
        }
        renderNavigation();
        renderCategories();
        if (typeof window !== 'undefined' && window.location.search) restoreLocation();
        else {
          byId('search-input').value = state.query;
          renderResults();
        }
        if (typeof window !== 'undefined' && state.selected && new URLSearchParams(window.location.search).has('skill')) {
          const row = [...byId('skills-results').children].find(element => element.dataset.skill === state.selected);
          if (row) row.scrollIntoView({ block: 'start', behavior: 'instant' });
        }
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
  byId('install-scope').addEventListener('change', event => {
    state.scope = event.target.value;
    renderResults();
  });
  byId('project-path').addEventListener('input', event => {
    state.projectPath = event.target.value;
    syncInstallation();
  });
  document.addEventListener('change', event => {
    if (event.target.matches('[data-install-agent]')) {
      setTarget(event.target.value);
      byId('skill-agent').focus({ preventScroll: true });
    }
  });
  if (typeof window !== 'undefined') window.addEventListener('popstate', () => { if (state.loaded) restoreLocation(); });
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
      syncUrl();
    } else if (button.dataset.openSkill || button.dataset.closeSkill) {
      const id = button.dataset.openSkill || button.dataset.closeSkill;
      state.selected = state.selected === id ? null : id;
      renderResults();
      syncUrl(true);
      const row = [...byId('skills-results').children].find(element => element.dataset.skill === id);
      if (row) row.querySelector('.skill-name').focus({ preventScroll: true });
    } else if (button.dataset.agent) {
      const target = button.dataset.agent;
      setTarget(target);
      const selected = byId('skills-results').querySelector(`[data-agent="${target}"]`);
      if (selected) selected.focus({ preventScroll: true });
    } else if (button.dataset.copySkill) {
      const preview = commandPreview(button.dataset.copySkill);
      if (preview.command) copy(preview.command, button);
    } else if (button.dataset.shareSkill) {
      const url = new URL(window.location.href);
      url.search = catalogParams({ selected: button.dataset.shareSkill, target: state.target });
      url.hash = '';
      copy(url.href, button, 'Đã sao chép liên kết đến skill.');
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
  byId('search-input').value = state.query;
  renderShowcase();
  loadCatalog();
})();
