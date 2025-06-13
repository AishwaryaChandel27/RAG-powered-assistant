// RAG Assistant JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

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
                // Scroll to the query form
                queryInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // Form submission handling with loading state
    const queryForm = document.querySelector('form[action*="ask_question"]');
    if (queryForm) {
        queryForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i data-feather="loader" class="me-2"></i>Processing...';
            submitBtn.disabled = true;
            
            // Re-render feather icons
            feather.replace();
            
            // Add loading class to form
            this.classList.add('loading');
        });
    }

    // Auto-resize textarea
    const textarea = document.getElementById('query');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.querySelector('form[action*="ask_question"]');
            if (form) {
                form.submit();
            }
        }
        
        // Focus search with '/' key
        if (e.key === '/' && !e.target.matches('input, textarea')) {
            e.preventDefault();
            const queryInput = document.getElementById('query');
            if (queryInput) {
                queryInput.focus();
            }
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy functionality for code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(codeBlock => {
        const pre = codeBlock.parentNode;
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2';
        copyBtn.innerHTML = '<i data-feather="copy" width="14" height="14"></i>';
        copyBtn.setAttribute('title', 'Copy code');
        
        pre.style.position = 'relative';
        pre.appendChild(copyBtn);
        
        copyBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(() => {
                this.innerHTML = '<i data-feather="check" width="14" height="14"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i data-feather="copy" width="14" height="14"></i>';
                    feather.replace();
                }, 2000);
            });
        });
    });

    // Update feather icons after dynamic content
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
