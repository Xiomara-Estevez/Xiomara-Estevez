// portal.js
document.addEventListener('DOMContentLoaded', function () {
    // Toggle service buttons on welcome page
    const mainButton = document.getElementById('mainButton');
    if (mainButton) {
        mainButton.addEventListener('click', function () {
            const hidden = document.getElementById('hiddenButtons');
            if (!hidden) return;
            hidden.style.display = hidden.style.display === 'none' ? 'block' : 'none';
        });
    }

    // Build a unified parameter set from both search and hash
    function getAllParams() {
        const p = new URLSearchParams();
        const s = new URLSearchParams(window.location.search);
        for (const [k, v] of s) p.append(k, v);
        if (window.location.hash && window.location.hash.indexOf('=') > -1) {
            const hash = window.location.hash.replace(/^#/, '');
            const h = new URLSearchParams(hash);
            for (const [k, v] of h) p.append(k, v);
        }
        return p;
    }

    const params = getAllParams();
    const hasAuth = params.has('code') || params.has('id_token') || params.has('access_token');
    const currentPath = window.location.pathname.split('/').pop();

    // Only redirect when we detect auth parameters and we're not already on the welcome page.
    if (hasAuth && currentPath !== 'welcome_portal.html') {
        setTimeout(() => { window.location.href = 'welcome_portal.html'; }, 200);
    }

    // Ensure the Register/Login link uses the current origin as the redirect_uri
    const authLink = document.getElementById('authLink');
    if (authLink && authLink.href) {
        // For local development (Live Server / file://), prevent navigating to the hosted Cognito UI
        // which will error if callback URLs are not configured. Instead simulate sign-in by
        // redirecting directly to the welcome page.
        authLink.addEventListener('click', function (ev) {
            const isLocalhost = location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.protocol === 'file:';
            if (isLocalhost) {
                ev.preventDefault();
                // Direct navigation to welcome_portal.html for local testing
                window.location.href = 'welcome_portal.html';
            }
        });

        try {
            const url = new URL(authLink.href);
            const currentRedirect = url.searchParams.get('redirect_uri');
            const desired = window.location.origin + window.location.pathname.replace(/[^/]+$/, '') + 'welcome_portal.html';
            if (!currentRedirect || !currentRedirect.startsWith(window.location.origin)) {
                url.searchParams.set('redirect_uri', desired);
                authLink.href = url.toString();
            }
        } catch (e) {
            console.warn('Failed to rewrite authLink redirect_uri', e);
        }
    }
});