document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const menuButton = document.querySelector('.menu-button');
  const scrim = document.querySelector('.nav-scrim');
  const search = document.querySelector('#chapter-search');
  const progress = document.querySelector('.reading-progress span');

  const setMenu = (open) => {
    body.classList.toggle('nav-open', open);
    menuButton?.setAttribute('aria-expanded', String(open));
  };

  menuButton?.addEventListener('click', () => setMenu(!body.classList.contains('nav-open')));
  scrim?.addEventListener('click', () => setMenu(false));

  search?.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    document.querySelectorAll('.nav-section').forEach((section) => {
      let visible = 0;
      section.querySelectorAll('.nav-link').forEach((link) => {
        const matches = !query || link.dataset.search.includes(query);
        link.hidden = !matches;
        visible += Number(matches);
      });
      section.hidden = visible === 0;
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && document.activeElement !== search) {
      event.preventDefault();
      search?.focus();
      if (window.matchMedia('(max-width: 980px)').matches) setMenu(true);
    }
    if (event.key === 'Escape') {
      setMenu(false);
      search?.blur();
    }
  });

  const updateProgress = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
    if (progress) progress.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  document.querySelectorAll('pre').forEach((block) => {
    const button = document.createElement('button');
    button.className = 'copy-code';
    button.type = 'button';
    button.textContent = 'COPY';
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(block.innerText);
        button.textContent = 'COPIED';
        window.setTimeout(() => { button.textContent = 'COPY'; }, 1400);
      } catch {
        button.textContent = 'SELECT';
      }
    });
    block.appendChild(button);
  });
});
