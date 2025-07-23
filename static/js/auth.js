// Показать/скрыть пароль
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeOpen = document.querySelector('.eye-open');
    const eyeClosed = document.querySelector('.eye-closed');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeOpen.style.display = 'none';
        eyeClosed.style.display = 'block';
    } else {
        passwordInput.type = 'password';
        eyeOpen.style.display = 'block';
        eyeClosed.style.display = 'none';
    }
}

// Анимации для полей ввода
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input');
    const submitButton = document.querySelector('.submit-button');
    const authForm = document.querySelector('.auth-form');
    
    // Эффекты фокуса для полей
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            if (this.value) {
                this.parentElement.classList.add('filled');
            } else {
                this.parentElement.classList.remove('filled');
            }
        });
        
        // Проверяем заполненность при загрузке
        if (input.value) {
            input.parentElement.classList.add('filled');
        }
    });
    
    // Автофокус на первое поле
    const firstInput = document.querySelector('.form-input');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Обработка отправки формы
    if (authForm) {
        authForm.addEventListener('submit', function(e) {
            const submitText = submitButton.querySelector('.submit-text');
            const submitArrow = submitButton.querySelector('.submit-arrow');
            const submitSpinner = submitButton.querySelector('.submit-spinner');
            
            submitText.style.opacity = '0';
            submitArrow.style.display = 'none';
            submitSpinner.style.display = 'block';
            submitButton.disabled = true;
            
            // В реальном приложении форма отправится автоматически
            // Этот код просто для демонстрации анимации
        });
    }
    
    // Валидация в реальном времени
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const wrapper = this.parentElement;
            
            if (this.value && !emailRegex.test(this.value)) {
                wrapper.classList.add('error');
            } else {
                wrapper.classList.remove('error');
            }
        });
    }
    
    // Анимация элементов при загрузке
    const animatedElements = document.querySelectorAll('.brand-feature, .flash-message');
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.transitionDelay = `${index * 0.1}s`;
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    });
});

// Обработка социальных кнопок
document.querySelectorAll('.social-button').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Анимация нажатия
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
        
        // В реальном приложении здесь будет редирект на соответствующий провайдер
        console.log('Social login:', this.classList[1]);
    });
});

// Обработка ссылки "Забыли пароль?"
document.querySelector('.forgot-password')?.addEventListener('click', function(e) {
    e.preventDefault();
    
    // В реальном приложении здесь будет модальное окно или редирект
    alert('Функция восстановления пароля будет доступна в ближайшее время.');
});

// Клавиатурные сокращения
document.addEventListener('keydown', function(e) {
    // Enter в любом поле - отправка формы
    if (e.key === 'Enter' && e.target.classList.contains('form-input')) {
        const form = e.target.closest('form');
        if (form) {
            form.requestSubmit();
        }
    }
    
    // Escape - очистка полей
    if (e.key === 'Escape') {
        document.querySelectorAll('.form-input').forEach(input => {
            if (input !== document.activeElement) {
                input.value = '';
                input.parentElement.classList.remove('filled');
            }
        });
    }
});

// Добавляем CSS для дополнительных состояний
const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    .input-wrapper.focused .form-input {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        border-color: var(--color-accent);
    }
    
    .input-wrapper.error .form-input {
        border-color: #ef4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
    
    .input-wrapper.filled .input-icon {
        color: var(--color-accent);
    }
    
    .submit-button:active {
        transform: scale(0.98);
    }
    
    .social-button:active {
        transform: scale(0.98) translateY(-1px);
    }
`;
document.head.appendChild(additionalStyles);
