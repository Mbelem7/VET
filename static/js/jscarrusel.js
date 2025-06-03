
  const contentImages = document.querySelector('.content-images');
  const slides = document.querySelectorAll('.content-images-item');
  const leftButton = document.getElementById('button-left');
  const rightButton = document.getElementById('button-right');

  let currentIndex = 0;

  function updateSlider() {
    const slideWidth = contentImages.clientWidth;
    contentImages.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
  }

  rightButton.addEventListener('click', () => {
    if (currentIndex < slides.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0; // volver al inicio
    }
    updateSlider();
  });

  leftButton.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
    } else {
      currentIndex = slides.length - 1; // ir al final
    }
    updateSlider();
  });

  // Hacer que el carrusel se adapte al tamaño de su contenedor
  window.addEventListener('resize', updateSlider);

