document.addEventListener("DOMContentLoaded", function () {
    const selectEspecie = document.querySelector("#especiem");
    const selectRaza = document.querySelector("#razam");

    selectEspecie.addEventListener("change", function () {
        const idEspecie = selectEspecie.value;
        selectRaza.innerHTML = '<option value="">Seleccione una raza</option>';
        if (idEspecie === "") return;

        fetch(`/razas/${idEspecie}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    data.forEach(raza => {
                        const option = document.createElement("option");
                        option.value = raza.id;
                        option.textContent = raza.nombre;
                        selectRaza.appendChild(option);
                    });
                    selectRaza.disabled = false;
                } else {
                    const option = document.createElement("option");
                    option.value = "";
                    option.textContent = "No hay razas disponibles";
                    selectRaza.appendChild(option);
                    selectRaza.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al cargar las razas:', error);
                const option = document.createElement("option");
                option.value = "";
                option.textContent = "Error al cargar razas";
                selectRaza.appendChild(option);
                selectRaza.disabled = true;
            });
    });
});