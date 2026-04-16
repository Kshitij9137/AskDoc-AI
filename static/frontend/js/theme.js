/* ═══════════════════════════════════════════════
   AskDocs AI — Theme Toggle
   Saves preference to localStorage
   Applies on page load instantly (no flash)
═══════════════════════════════════════════════ */

(function () {
    // Apply saved theme immediately on load
    // This runs before the page renders to prevent flash
    const saved = localStorage.getItem('askdocs_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
})();

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';

    // Apply theme
    html.setAttribute('data-theme', next);

    // Save preference
    localStorage.setItem('askdocs_theme', next);

    // Update canvas dot color if canvas exists
    updateCanvasDots(next);

    console.log(`Theme switched to: ${next}`);
}

function updateCanvasDots(theme) {
    // The canvas animation reads CSS variables
    // We just need to signal it to refresh
    const canvas = document.getElementById('bgCanvas');
    if (canvas) {
        // Dispatch custom event so canvas can update
        canvas.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }
}
