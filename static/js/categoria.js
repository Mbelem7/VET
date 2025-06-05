document.addEventListener("DOMContentLoaded", function () {
    const selectCategoria = document.querySelector("#categoria");

    selectCategoria.addEventListener("change", function () {
        const idCategoria = selectCategoria.value;
        // Aquí puedes agregar lógica si necesitas cargar algo según la categoría seleccionada
        console.log("Categoría seleccionada:", idCategoria);
        // Por ejemplo, podrías hacer un fetch para cargar productos o subcategorías
        // fetch(`/subcategorias/${idCategoria}`).then(...);
    });
});