// Smooth Scroll for Internal Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Toggle Mobile Navigation Menu
const mobileNavButton = document.querySelector('.mobile-nav-button');
const navLinks = document.querySelector('nav ul');

mobileNavButton.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Flash Message Auto-Hide
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach((message) => {
        message.classList.add('fade-out');
    });
}, 5000);  // Auto-hide after 5 seconds

// Add Scroll-to-Top Button
const scrollToTopButton = document.createElement('button');
scrollToTopButton.classList.add('scroll-to-top');
scrollToTopButton.innerHTML = '↑';
document.body.appendChild(scrollToTopButton);

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollToTopButton.classList.add('show');
    } else {
        scrollToTopButton.classList.remove('show');
    }
});

scrollToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

document.querySelector('.mobile-nav-button').addEventListener('click', function() {
    const menu = document.querySelector('nav ul');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
});
