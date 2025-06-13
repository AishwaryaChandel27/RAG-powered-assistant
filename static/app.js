// Publications Assistant JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Theme management
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;
    
    // Check for saved theme preference or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme
    if (currentTheme === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
        themeIcon.setAttribute('data-feather', 'moon');
    } else {
        htmlElement.removeAttribute('data-theme');
        themeIcon.setAttribute('data-feather', 'sun');
    }
    
    // Theme toggle functionality
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-theme');
            
            if (currentTheme === 'dark') {
                // Switch to light theme
                htmlElement.removeAttribute('data-theme');
                themeIcon.setAttribute('data-feather', 'sun');
                localStorage.setItem('theme', 'light');
            } else {
                // Switch to dark theme
                htmlElement.setAttribute('data-theme', 'dark');
                themeIcon.setAttribute('data-feather', 'moon');
                localStorage.setItem('theme', 'dark');
            }
            
            // Update feather icons
            feather.replace();
        });
    }

    // Handle example query clicks
    const exampleQueries = document.querySelectorAll('.example-query');
    const queryInput = document.getElementById('query');

    exampleQueries.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const queryText = this.textContent.trim();
            if (queryInput) {
                queryInput.value = queryText;
                queryInput.focus();
                queryInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // Form submission handling with loading state
    const queryForm = document.querySelector('form[action*="ask_question"]');
    if (queryForm) {
        queryForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                // Show loading state
                submitBtn.innerHTML = '<i data-feather="loader"></i>';
                submitBtn.disabled = true;
                feather.replace();
            }
        });
    }

    // Auto-resize textarea
    if (queryInput) {
        queryInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && queryInput === document.activeElement) {
            e.preventDefault();
            if (queryForm) {
                queryForm.submit();
            }
        }
        
        // Focus search with '/' key
        if (e.key === '/' && !e.target.matches('input, textarea')) {
            e.preventDefault();
            if (queryInput) {
                queryInput.focus();
            }
        }
    });

    // Initialize feather icons
    feather.replace();
});

// Utility functions
function showToast(message, type = 'info') {
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// API call function for future enhancements
async function askQuestion(query) {
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error asking question:', error);
        throw error;
    }
}
