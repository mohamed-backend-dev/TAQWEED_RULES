/* 🔧 وظائف تفاعلية وميّزات طفيفة */
document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;

    // تهيئة الثيم المخزن
    const saved = localStorage.getItem('theme');
    if (saved) root.setAttribute('data-theme', saved);

    const toggleDark = () => {
        const isDark = root.getAttribute('data-theme') === 'dark';
        const next = isDark ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    };
    window.toggleDark = toggleDark;

    // زر تبديل الثيم (اختياري)
    document.getElementById('themeToggle')?.addEventListener('click', toggleDark);

    // تأثير ضغطة الأزرار
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.animate([
                {transform: 'scale(1)'},
                {transform: 'scale(0.98)'},
                {transform: 'scale(1)'}
            ], {duration: 180, easing: 'ease-out'});
        });
    });

    // زر العودة إلى الأعلى
    const scrollBtn = document.createElement('button');
    scrollBtn.id = 'scrollTopBtn';
    scrollBtn.title = 'العودة إلى الأعلى';
    scrollBtn.textContent = '↑';
    document.body.appendChild(scrollBtn);
    scrollBtn.addEventListener('click', () => window.scrollTo({top: 0, behavior: 'smooth'}));
    window.addEventListener('scroll', () => {
        scrollBtn.classList.toggle('show', window.scrollY > 300);
    });

    // كشف البطاقات عند التمرير
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
                observer.unobserve(entry.target);
            }
        });
    }, {threshold: 0.1});

    document.querySelectorAll('.card, .reveal').forEach(el => observer.observe(el));

    // رسالة دينية متغيرة
    const messages = [
        'من قال سبحان الله وبحمده في يوم مائة مرة حطت خطاياه... (رواه البخاري)',
        'ابتسم في وجه أخيك صدقة. (حديث)',
        'خيركم من تعلم القرآن وعلمه. (حديث)'
    ];
    const msgEl = document.createElement('div');
    msgEl.className = 'quran-text';
    msgEl.textContent = messages[Math.floor(Math.random() * messages.length)];
    document.body.prepend(msgEl);

    // افتح القائمة المنسدلة على الهواتف
    document.querySelectorAll('nav .dropdown').forEach(drop => {
        const btn = drop.querySelector('.dropbtn');
        btn.addEventListener('click', e => {
            e.preventDefault();
            drop.classList.toggle('open');
        });
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('nav-toggle');
    const menu = document.querySelector('.main-nav');

    toggle?.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

    // Dropdown toggle على الهواتف
    document.querySelectorAll('.dropbtn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            btn.nextElementSibling.classList.toggle('active');
        });
    });
});
document.addEventListener('DOMContentLoaded', () => {

    const toggle = document.getElementById('nav-toggle');
    const menu = document.querySelector('.main-nav');

    toggle.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

});