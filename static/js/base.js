document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const toggles = document.querySelectorAll('[data-sidebar-toggle]');
    const closers = document.querySelectorAll('[data-sidebar-close]');

    const openSidebar = () => body.classList.add('sidebar-open');
    const closeSidebar = () => body.classList.remove('sidebar-open');

    toggles.forEach((toggle) => {
        toggle.addEventListener('click', openSidebar);
    });

    closers.forEach((closer) => {
        closer.addEventListener('click', closeSidebar);
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeSidebar();
        }
    });
});
