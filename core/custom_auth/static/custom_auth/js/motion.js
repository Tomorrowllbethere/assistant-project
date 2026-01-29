const glass = document.querySelector('.glass-hero');
const brand = document.querySelector('.brand-motion');

document.addEventListener('mousemove', (e) => {
    // Обчислюємо зміщення від центру
    const x = (window.innerWidth / 2 - e.pageX) / 40;
    const y = (window.innerHeight / 2 - e.pageY) / 40;

    // 1. Ефект Tilt для скляної панелі
    if (glass) {
        glass.style.transform = `rotateY(${-x}deg) rotateX(${y}deg)`;
    }

    // 2. Паралакс для тексту (рухається швидше за скло)
    if (brand) {
        brand.style.transform = `translate(${x * 1.8}px, ${-y * 1.8}px)`;
        // Додаємо динамічну тінь для об'єму
        brand.style.textShadow = `${x}px ${-y}px 25px rgba(0,0,0,0.3)`;
    }
});

// Плавне повернення, коли мишка йде
document.addEventListener('mouseleave', () => {
    if (glass) glass.style.transition = "all 0.5s ease";
    if (glass) glass.style.transform = `rotateY(0deg) rotateX(0deg)`;
    
    if (brand) brand.style.transition = "all 0.5s ease";
    if (brand) brand.style.transform = `translate(0, 0)`;
});
