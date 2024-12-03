document.addEventListener("DOMContentLoaded", () => {
    let actual = 0;
    const atras = document.getElementById("atras");
    const adelante = document.getElementById("adelante");
    const img = document.getElementById("img");

    function renderCarrusel() {
        img.innerHTML = `<img class="img" src="${imagenes[actual]}" alt="Imagen ${actual + 1}" loading="lazy" onclick="location.href='${rutas[actual]}'">`;
    }    

    atras.addEventListener("click", () => {
        actual = (actual === 0) ? imagenes.length - 1 : actual - 1;
        renderCarrusel();
        resetAutoSlide();
    });

    adelante.addEventListener("click", () => {
        actual = (actual + 1) % imagenes.length;
        renderCarrusel();
        resetAutoSlide();
    });

    const autoSlideInterval = 5000;
    let autoSlide = setInterval(() => {
        actual = (actual + 1) % imagenes.length;
        renderCarrusel();
    }, autoSlideInterval);

    function resetAutoSlide() {
        clearInterval(autoSlide);
        autoSlide = setInterval(() => {
            actual = (actual + 1) % imagenes.length;
            renderCarrusel();
        }, autoSlideInterval);
    }

    renderCarrusel();
});
