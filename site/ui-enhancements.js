// UI Enhancement Functions for Calcora
// Add this to both demo.html and engine web UI

// Matrix validation and preview
function validateAndPreviewMatrix(textareaId, previewId, dimensionsId) {
    const textarea = document.getElementById(textareaId);
    const preview = document.getElementById(previewId);
    const dimensions = document.getElementById(dimensionsId);
    
    if (!textarea || !preview || !dimensions) return;
    
    try {
        const value = textarea.value.trim();
        if (!value) {
            preview.style.display = 'none';
            return;
        }
        
        const matrix = JSON.parse(value);
        if (Array.isArray(matrix) && matrix.length > 0 && Array.isArray(matrix[0])) {
            const rows = matrix.length;
            const cols = matrix[0].length;
            dimensions.innerHTML = `<i class="fas fa-check-circle" style="color: var(--success);"></i> ${rows}×${cols} matrix`;
            preview.style.display = 'block';
            preview.style.borderLeft = '3px solid var(--success)';
            preview.style.background = 'rgba(16, 185, 129, 0.1)';
            textarea.style.borderColor = 'var(--success)';
        } else {
            throw new Error('Invalid matrix format');
        }
    } catch (e) {
        dimensions.innerHTML = `<i class="fas fa-exclamation-triangle" style="color: var(--error);"></i> Invalid format - check brackets and commas`;
        preview.style.display = 'block';
        preview.style.borderLeft = '3px solid var(--error)';
        preview.style.background = 'rgba(239, 68, 68, 0.1)';
        textarea.style.borderColor = 'var(--error)';
    }
}

// Loading with progress messages
let loadingMessages = [
    '⚙️ Parsing expression...',
    '🔬 Applying math rules...',
    '✨ Simplifying result...',
    '📝 Generating steps...'
];
let loadingInterval = null;

function showLoadingWithProgress() {
    const loadingEl = document.getElementById('loading');
    if (!loadingEl) return;
    
    loadingEl.classList.add('visible');
    
    // Rotate messages
    let messageIndex = 0;
    const loadingText = loadingEl.querySelector('.loading-text');
    if (loadingText) {
        loadingText.textContent = loadingMessages[0];
        
        loadingInterval = setInterval(() => {
            messageIndex = (messageIndex + 1) % loadingMessages.length;
            loadingText.textContent = loadingMessages[messageIndex];
        }, 800);
    }
}

function hideLoadingWithProgress() {
    const loadingEl = document.getElementById('loading');
    if (loadingEl) {
        loadingEl.classList.remove('visible');
    }
    if (loadingInterval) {
        clearInterval(loadingInterval);
        loadingInterval = null;
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    const style = document.createElement('style');
    if (!document.getElementById('toast-styles')) {
        style.id = 'toast-styles';
        style.textContent = `
            .toast {
                position: fixed;
                top: 2rem;
                right: 2rem;
                padding: 1rem 1.5rem;
                border-radius: 0.75rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                gap: 0.75rem;
                font-weight: 600;
                z-index: 10000;
                animation: slideInRight 0.3s ease-out;
            }
            .toast-success {
                background: var(--success);
                color: white;
            }
            .toast-error {
                background: var(--error);
                color: white;
            }
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Validate expression syntax
function validateExpression(expr) {
    if (!expr || typeof expr !== 'string') return [];
    
    const errors = [];
    
    if (expr.includes('^')) {
        errors.push('Use ** for exponents, not ^. Example: x**2 instead of x^2');
    }
    
    if (expr.includes('×')) {
        errors.push('Use * for multiplication, not ×');
    }
    
    // Check balanced parentheses
    let openCount = (expr.match(/\(/g) || []).length;
    let closeCount = (expr.match(/\)/g) || []).length;
    if (openCount !== closeCount) {
        errors.push('Unbalanced parentheses - check your brackets');
    }
    
    // Check for common function misspellings
    const commonMisspellings = {
        'sine': 'sin',
        'cosine': 'cos',
        'tangent': 'tan',
        'ln': 'log',
        'square root': 'sqrt'
    };
    
    for (const [wrong, right] of Object.entries(commonMisspellings)) {
        if (expr.toLowerCase().includes(wrong)) {
            errors.push(`Use "${right}" instead of "${wrong}"`);
        }
    }
    
    return errors;
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        setTimeout(() => {
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        }, 100);
    }
}

// Enhanced copy with feedback
function copyToClipboardWithFeedback(text, buttonElement) {
    if (!text) {
        showToast('Nothing to copy', 'error');
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        if (buttonElement) {
            const originalHTML = buttonElement.innerHTML;
            buttonElement.innerHTML = '<i class="fas fa-check"></i> Copied!';
            buttonElement.style.background = 'var(--success)';
            buttonElement.style.color = 'white';
            setTimeout(() => {
                buttonElement.innerHTML = originalHTML;
                buttonElement.style.background = '';
                buttonElement.style.color = '';
            }, 1500);
        }
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'error');
    });
}

// Initialize all UI enhancements
function initializeUIEnhancements() {
    // Add matrix validation listeners
    const matrixA = document.getElementById('matrix-a');
    const matrixB = document.getElementById('matrix-b');
    
    if (matrixA) {
        matrixA.addEventListener('input', () => {
            validateAndPreviewMatrix('matrix-a', 'matrix-a-preview', 'matrix-a-dimensions');
        });
        // Initial validation
        validateAndPreviewMatrix('matrix-a', 'matrix-a-preview', 'matrix-a-dimensions');
    }
    
    if (matrixB) {
        matrixB.addEventListener('input', () => {
            validateAndPreviewMatrix('matrix-b', 'matrix-b-preview', 'matrix-b-dimensions');
        });
    }
    
    // Add input validation for expression
    const exprInput = document.getElementById('diff-expr') || document.getElementById('expr');
    if (exprInput) {
        exprInput.addEventListener('blur', () => {
            const expr = exprInput.value ? exprInput.value.trim() : '';
            if (expr) {
                const errors = validateExpression(expr);
                if (errors.length > 0) {
                    // Show first error as tooltip
                    exprInput.title = errors[0];
                    exprInput.style.borderColor = 'var(--warning)';
                } else {
                    exprInput.title = '';
                    exprInput.style.borderColor = '';
                }
            }
        });
    }
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUIEnhancements);
} else {
    initializeUIEnhancements();
}
