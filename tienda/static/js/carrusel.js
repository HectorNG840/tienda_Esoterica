document.addEventListener("DOMContentLoaded", () => {
    let actual = 0;
    const atras = document.getElementById("atras");
    const adelante = document.getElementById("adelante");
    const img = document.getElementById("img");

    function renderCarrusel() {
        img.innerHTML = `<img class="img" src="${imagenes[actual]}" alt="Imagen ${actual + 1}" loading="lazy">`;
    }

    atras.addEventListener("click", () => {
        actual = (actual === 0) ? imagenes.length - 1 : actual - 1;
        renderCarrusel();
    });

    adelante.addEventListener("click", () => {
        actual = (actual + 1) % imagenes.length;
        renderCarrusel();
    });

    renderCarrusel();
});
