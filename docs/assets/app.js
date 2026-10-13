'use strict';
(() => {
  const search = document.querySelector('#search');
  const pagesOnly = document.querySelector('#pages-only');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.post-card')];
  const sections = [...document.querySelectorAll('.topic-section')];
  const empty = document.querySelector('.empty-state');
  const count = document.querySelector('#result-count');
  const params = new URLSearchParams(location.search);
  const allowed = new Set(buttons.map(button => button.dataset.filter));
  let kind = allowed.has(params.get('type')) ? params.get('type') : 'all';
  search.value = params.get('q') || '';
  pagesOnly.checked = params.get('pages') === '1';
  function filter(updateUrl = true) {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    cards.forEach(card => {
      const match = (kind === 'all' || card.dataset.kind === kind)
        && (!pagesOnly.checked || card.dataset.published === 'true')
        && terms.every(term => card.dataset.search.includes(term));
      card.hidden = !match;
      shown += Number(match);
    });
    sections.forEach(section => { section.hidden = ![...section.querySelectorAll('.post-card')].some(card => !card.hidden); });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === kind)));
    count.textContent = `${shown} of ${cards.length} entries`;
    empty.hidden = shown !== 0;
    document.querySelectorAll('.collection-nav nav a').forEach(link => {
      const section = document.querySelector(link.getAttribute('href'));
      link.hidden = section.hidden;
    });
    if (updateUrl) {
      const url = new URL(location.href);
      search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
      kind !== 'all' ? url.searchParams.set('type', kind) : url.searchParams.delete('type');
      pagesOnly.checked ? url.searchParams.set('pages', '1') : url.searchParams.delete('pages');
      history.replaceState(null, '', url);
    }
  }
  search.addEventListener('input', () => filter());
  pagesOnly.addEventListener('change', () => filter());
  buttons.forEach(button => button.addEventListener('click', () => { kind = button.dataset.filter; filter(); }));
  document.querySelector('#reset').addEventListener('click', () => {
    search.value = ''; kind = 'all'; pagesOnly.checked = false; filter(); search.focus();
  });
  document.querySelector('.tools').hidden = false;
  filter(false);
})();
