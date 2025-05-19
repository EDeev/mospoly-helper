// Основной JavaScript-файл для сайта EasyAccess

document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }
    
    // Изменение стиля хедера при прокрутке
    const header = document.querySelector('header');
    
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
    
    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            // Проверяем, что это не просто якорь
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    // Закрываем мобильное меню, если оно открыто
                    if (navLinks && navLinks.classList.contains('active')) {
                        navLinks.classList.remove('active');
                        if (mobileMenuToggle) {
                            mobileMenuToggle.classList.remove('active');
                        }
                    }
                    
                    // Прокручиваем до элемента
                    const headerHeight = header ? header.offsetHeight : 0;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Анимация появления элементов при прокрутке
    const animatedElements = document.querySelectorAll('.feature-card, .tech-item, .update-card, .team-card, .curator-card, .point-card, .info-block, .resource-card, .download-card');
    
    if (animatedElements.length > 0) {
        // Функция для проверки видимости элемента
        function isElementInViewport(el) {
            const rect = el.getBoundingClientRect();
            return (
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85
            );
        }
        
        // Функция для добавления класса анимации
        function handleScroll() {
            animatedElements.forEach(element => {
                if (isElementInViewport(element)) {
                    element.classList.add('animate-in');
                }
            });
        }
        
        // Обработчик прокрутки
        window.addEventListener('scroll', handleScroll);
        
        // Вызываем обработчик сразу для элементов, которые видны при загрузке страницы
        handleScroll();
    }
    
    // Дополнительные стили для анимаций
    const style = document.createElement('style');
    style.textContent = `
        .feature-card, .tech-item, .update-card, .team-card, .curator-card, .point-card, .info-block, .resource-card, .download-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-in {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
});
