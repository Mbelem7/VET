document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscador_mascota');
    const sugerencias = document.getElementById('sugerencias_mascota');
    const mascotaIdInput = document.getElementById('mascota_id');
    const selectServicio = document.getElementById('servicio');
    const tablaServicios = document.getElementById('tabla-negocios').querySelector('tbody');
    const btnAgregar = document.getElementById('agregar_servicio');
    const totalInput = document.getElementById('tots');

    const catalogoDataElement = document.getElementById('data-servicios');
    const serviciosCatalogo = JSON.parse(catalogoDataElement.dataset.catalogo);

    let mascotaSeleccionada = null;

    buscador.addEventListener('input', function () {
        const query = buscador.value.trim();
        if (!query) {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
            document.getElementById('row-tabla-mascota').style.display = 'none';
            return;
        }
        fetch(`/buscar_mascota?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                sugerencias.innerHTML = '';
                sugerencias.style.display = data.length ? 'block' : 'none';
                data.forEach(mascota => {
                    const div = document.createElement('div');
                    div.textContent = mascota.nombre + (mascota.propietario ? ` (Propietario: ${mascota.propietario})` : '');
                    div.classList.add('sugerencia-item');
                    div.addEventListener('mousedown', function () {
                        buscador.value = mascota.nombre;
                        mascotaIdInput.value = mascota.id;
                        mascotaSeleccionada = mascota;
                        sugerencias.innerHTML = '';
                        sugerencias.style.display = 'none';
                        mostrarTablaMascota(mascota);
                    });
                    sugerencias.appendChild(div);
                });
            });
    });

    buscador.addEventListener('blur', () => {
        setTimeout(() => {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
        }, 150);
    });

    document.querySelector('form').addEventListener('submit', function (e) {
        if (!mascotaIdInput.value) {
            e.preventDefault();
            alert('Selecciona una mascota de la lista.');
        }
    });

    btnAgregar.addEventListener('click', () => {
        const servicioId = selectServicio.value;
        const servicioNombre = selectServicio.options[selectServicio.selectedIndex].text;
        const precio = serviciosCatalogo[servicioId];

        const yaExiste = Array.from(tablaServicios.querySelectorAll('input[name="servicio_id[]"]'))
            .some(input => input.value == servicioId);
        if (yaExiste) {
            alert("Este servicio ya fue agregado.");
            return;
        }

        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>
                ${servicioNombre}
                <input type="hidden" name="servicio_id[]" value="${servicioId}">
            </td>
            <td>
                ${precio.toFixed(2)}
                <input type="hidden" name="precio[]" value="${precio.toFixed(2)}">
            </td>
            <td>
                <button type="button" class="eliminar_servicio">Eliminar</button>
            </td>
        `;
        tablaServicios.appendChild(fila);
        actualizarTotal();
    });

    tablaServicios.addEventListener('click', function (e) {
        if (e.target.classList.contains('eliminar_servicio')) {
            e.target.closest('tr').remove();
            actualizarTotal();
        }
    });

    function actualizarTotal() {
        let total = 0;
        tablaServicios.querySelectorAll('input[name="precio[]"]').forEach(input => {
            total += parseFloat(input.value) || 0;
        });
        totalInput.value = total.toFixed(2);
    }

    document.querySelector('form').addEventListener('submit', function (e) {
        if (!mascotaIdInput.value) {
            e.preventDefault();
            alert('Selecciona una mascota de la lista.');
            return;
        }

        if (tablaServicios.querySelectorAll('input[name="servicio_id[]"]').length === 0) {
            e.preventDefault();
            alert('Agrega al menos un servicio.');
        }
    });

    function mostrarTablaMascota(mascota) {
        // Obtener especie y raza por AJAX si no vienen en el objeto
        Promise.all([
            fetch(`/api/mascota_especie/${mascota.id}`).then(r => r.json()),
            fetch(`/api/mascota_raza/${mascota.id}`).then(r => r.json())
        ]).then(([especie, raza]) => {
            const rowDiv = document.getElementById('row-tabla-mascota');
            const tbody = document.querySelector('#tabla_mascota tbody');
            tbody.innerHTML = `
                <tr>
                    <td>${mascota.nombre}</td>
                    <td>${especie.nombre || ''}</td>
                    <td>${raza.nombre || ''}</td>
                    <td>${mascota.propietario || ''}</td>
                    <td><button type="button" id="eliminar_mascota_info" class="eliminar_mascota_info">Eliminar</button></td>
                </tr>
            `;
            rowDiv.style.display = '';
            // Agregar event listener para eliminar la selección de mascota
            const btnEliminar = document.getElementById('eliminar_mascota_info');
            if (btnEliminar) {
                btnEliminar.addEventListener('click', function () {
                    tbody.innerHTML = '';
                    rowDiv.style.display = 'none';
                    document.getElementById('buscador_mascota').value = '';
                    document.getElementById('mascota_id').value = '';
                });
            }
        });
    }

    // Ocultar la tabla si el usuario borra la selección
    buscador.addEventListener('blur', () => {
        setTimeout(() => {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
            if (!buscador.value || !mascotaIdInput.value) {
                document.getElementById('row-tabla-mascota').style.display = 'none';
            }
        }, 150);
    });
});