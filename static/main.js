// F1 Manager Game - Enhanced JavaScript
// Loading animation
window.addEventListener('load', () => {
  document.body.classList.add('loaded');
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Add ripple effect to buttons
function createRipple(event) {
  const button = event.currentTarget;
  const ripple = document.createElement('span');
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = event.clientX - rect.left - size / 2;
  const y = event.clientY - rect.top - size / 2;
  
  ripple.style.width = ripple.style.height = size + 'px';
  ripple.style.left = x + 'px';
  ripple.style.top = y + 'px';
  ripple.classList.add('ripple');
  button.appendChild(ripple);
  
  setTimeout(() => ripple.remove(), 600);
}

document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', createRipple);
});

// Fade in elements on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('fade-in');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.glass-card, .card').forEach(el => {
  observer.observe(el);
});

// Form validation with animations
const forms = document.querySelectorAll('form');
forms.forEach(form => {
  const inputs = form.querySelectorAll('input, select');
  
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', () => {
      if (!input.value) {
        input.parentElement.classList.remove('focused');
      }
    });
  });
});

// Toast notification system
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => toast.classList.add('show'), 100);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Loading spinner
function showLoader() {
  const loader = document.createElement('div');
  loader.className = 'loader-overlay';
  loader.innerHTML = '<div class="loader"></div>';
  document.body.appendChild(loader);
}

function hideLoader() {
  const loader = document.querySelector('.loader-overlay');
  if (loader) loader.remove();
}

// Enhanced table row animations
const tableRows = document.querySelectorAll('tbody tr');
tableRows.forEach((row, index) => {
  row.style.animation = `fadeInUp 0.5s ease ${index * 0.05}s forwards`;
  row.style.opacity = '0';
});

// Card hover 3D effect
document.querySelectorAll('.card, .glass-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;
    
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
  });
  
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
  });
});

// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (menuToggle) {
  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuToggle.classList.toggle('active');
  });
}

console.log('%cF1 Manager Game%c \n🏎️ Powered by Shrestha Hardia', 'color: #E10600; font-size: 24px; font-weight: bold;', 'color: #FFD700; font-size: 12px;');
