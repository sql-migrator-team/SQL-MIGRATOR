function renderSidebar() {
  const user = getUserInfo();
  if (!user) return;
  buildSidebarLinks(user.role);
}

function initSidebar() {
  const sidebarContainer = document.getElementById('sidebar-container');
  if (!sidebarContainer) return;
  loadSharedComponent('sidebar', () => {
    renderSidebar();
    bindLogout();
    const collapseBtn = document.querySelector('.sidebar-collapse');
    const mainContent = document.querySelector('.page-content');
    const sidebar = document.querySelector('.sidebar');
    if (collapseBtn && mainContent && sidebar) {
      collapseBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('collapsed');
      });
    }
  });
}
