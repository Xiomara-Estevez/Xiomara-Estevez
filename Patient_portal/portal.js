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

    // Detect AWS Cognito redirect (authorization code or tokens) and forward to welcome portal.
    // Look in both search and hash since implicit flows put tokens in the fragment.
    const search = window.location.search || '';
    const hash = window.location.hash ? window.location.hash.replace('#', '?') : '';
    const params = new URLSearchParams(search + hash);

    const hasAuth = params.has('code') || params.has('id_token') || params.has('access_token');
    const currentPath = window.location.pathname.split('/').pop();

    // Only redirect when we detect auth parameters and we're not already on the welcome page.
    if (hasAuth && currentPath !== 'welcome_portal.html') {
        // Small delay to allow any page UI to settle
        setTimeout(() => {
            window.location.href = 'welcome_portal.html';
        }, 200);
    }
  
        // Ensure the Cognito login link uses the current host as the redirect_uri so it works when deployed
        // If an anchor with id `authLink` exists and contains a Cognito URL, replace its `redirect_uri` param
        const authLink = document.getElementById('authLink');
        if (authLink && authLink.href) {
            try {
                const url = new URL(authLink.href);
                const params = url.searchParams;
                if (params.has('redirect_uri')) {
                    const newRedirect = window.location.origin + window.location.pathname.replace(/\/index\.html$/, '/') ;
                    params.set('redirect_uri', newRedirect);
                    url.search = params.toString();
                    authLink.href = url.toString();
                }
            } catch (e) {
                // ignore invalid URL parsing
            }
        }
});