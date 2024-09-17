// userrequirements/static/userrequirements/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Custom JavaScript can go here

    // Example: Smooth scroll for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({
                behavior: 'smooth'
            });
        });
    }

    // Example: Show a confirmation dialog on logout
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    }

    // Add more custom JavaScript as needed
});
