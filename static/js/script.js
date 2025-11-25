
const cards = document.querySelectorAll('.hide-img');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
    else {
      entry.target.classList.remove('visible');
    }
  });
}, { threshold: 0.2 });

cards.forEach(card => observer.observe(card));


const zoomInElements = document.querySelectorAll('.zoomin');
const observer1 = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('visible');
            // observer1.unobserve(entry.target);
        }
        else{
            entry.target.classList.remove('visible');
        }
    });
}, { threshold: 0.2 });

zoomInElements.forEach(element => observer1.observe(element));

const zoomInElementsfade = document.querySelectorAll('.zoom-fade');
const observerfade = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('visible');
            observerfade.unobserve(entry.target);
        }
        
    });
}, { threshold: 0 });

zoomInElementsfade.forEach(element => observerfade.observe(element));

const zoomElements = document.querySelectorAll('.scroll');

window.addEventListener('scroll', () => {
  zoomElements.forEach(el => {
    const rect = el.getBoundingClientRect();
    const windowHeight = window.innerHeight;


    const visible = 1 - Math.abs(rect.top + rect.height / 2 - windowHeight / 2) / (windowHeight / 2);

    const scale = 0.9 + Math.max(0, Math.min(visible, 1)) * 0.2;
    el.style.transform = `scale(${scale})`;
  });
});