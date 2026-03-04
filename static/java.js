document.addEventListener('DOMContentLoaded', function () {

    const root = document.documentElement;

    /* =======================
       تهيئة الثيم
    ======================== */
    const saved = localStorage.getItem('theme');
    if (saved) root.setAttribute('data-theme', saved);

    function toggleDark() {
        const isDark = root.getAttribute('data-theme') === 'dark';
        const next = isDark ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    }

    window.toggleDark = toggleDark;

    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleDark);
    }

    /* =======================
       تأثير الأزرار
    ======================== */
    document.querySelectorAll('.btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            btn.animate([
                { transform: 'scale(1)' },
                { transform: 'scale(0.98)' },
                { transform: 'scale(1)' }
            ], {
                duration: 180,
                easing: 'ease-out'
            });
        });
    });

    /* =======================
       زر العودة للأعلى
    ======================== */
    const scrollBtn = document.createElement('button');
    scrollBtn.id = 'scrollTopBtn';
    scrollBtn.title = 'العودة إلى الأعلى';
    scrollBtn.textContent = '↑';
    document.body.appendChild(scrollBtn);

    scrollBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', function () {
        if (window.scrollY > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    });

    /* =======================
       كشف البطاقات عند التمرير
    ======================== */
    const observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card').forEach(function (el) {
        observer.observe(el);
    });

    const msgEl = document.createElement('div');
    msgEl.className = 'quran-text';
    msgEl.textContent = messages[Math.floor(Math.random() * messages.length)];
    document.body.prepend(msgEl);

    /* =======================
       تشغيل قائمة الهاتف ☰
    ======================== */
    const toggle = document.getElementById('nav-toggle');
    const menu = document.querySelector('.main-nav');

    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            menu.classList.toggle('active');
        });
    }

});