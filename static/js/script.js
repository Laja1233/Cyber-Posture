// State management
let currentState = 'ready';

// Toggle sidebar section collapse
function toggleSidebarSection(header) {
    const sidebarItems = header.nextElementSibling;
    const isCollapsed = header.classList.contains('collapsed');
    
    if (isCollapsed) {
        // Expand
        sidebarItems.classList.remove('collapsed');
        header.classList.remove('collapsed');
    } else {
        // Collapse
        sidebarItems.classList.add('collapsed');
        header.classList.add('collapsed');
    }
}

// Initialize sidebar sections as expanded (dropdown by default)
function initializeSidebar() {
    const sidebarHeaders = document.querySelectorAll('.sidebar-header');
    const sidebarItems = document.querySelectorAll('.sidebar-items');
    
    // Remove collapsed class from all headers and items by default (expanded state)
    sidebarHeaders.forEach(header => {
        header.classList.remove('collapsed');
    });
    
    sidebarItems.forEach(items => {
        items.classList.remove('collapsed');
    });
}

// Toast notifications
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    toast.className = `toast toast-${type}`;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

// Mobile menu
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
    }
}

function closeMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
    }
}

// Navigation handling
function handleNavigation(page) {
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to clicked nav item
    event.target.closest('.nav-item').classList.add('active');
    
    // Handle different page navigation
    switch(page) {
        case 'dashboard':
            console.log('Navigate to Dashboard');
            break;
        case 'home':
            console.log('Navigate to Home');
            break;
        case 'search':
            console.log('Navigate to Search');
            break;
        case 'network':
            console.log('Navigate to Network');
            break;
        case 'explore':
            console.log('Navigate to Explore');
            break;
        default:
            console.log('Navigate to', page);
            break;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar to expanded state (dropdown by default)
    initializeSidebar();
    
    console.log('Application initialized with expanded sidebar');
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMobileMenu();
    }
});