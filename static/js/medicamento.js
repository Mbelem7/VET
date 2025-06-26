document.addEventListener('DOMContentLoaded', function () {
    // Buscador de medicamentos
    const sugerencias = document.getElementById('sugerencias_medicamento');
    const inputMed = document.getElementById('buscador_medicamento');
    const hiddenIdMed = document.getElementById('medicamento_id');
    const dosisInput = document.getElementById('dosis');
    const duracionInput = document.getElementById('duracion');
    const btnAgregarMed = document.getElementById('agregar_medicamento');
    const tablaMed = document.getElementById('tabla_medicamentos').querySelector('tbody');
    const precioConsultaInput = document.getElementById('prec');
    const totalInput = document.getElementById('totalc');
    let medicamentoSeleccionado = null;

    inputMed.addEventListener('input', function () {
        const texto = inputMed.value.trim();
        if (!texto) {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
            return;
        }
        fetch(`/buscar_medicamento?q=${encodeURIComponent(texto)}`)
            .then(res => res.json())
            .then(data => {
                sugerencias.innerHTML = '';
                sugerencias.style.display = data.length ? 'block' : 'none';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.textContent = item.nombre;
                    div.classList.add('sugerencia-item');
                    div.addEventListener('mousedown', () => {
                        inputMed.value = item.nombre;
                        hiddenIdMed.value = item.id;
                        medicamentoSeleccionado = item;
                        sugerencias.innerHTML = '';
                        sugerencias.style.display = 'none';
                    });
                    sugerencias.appendChild(div);
                });
            });
    });

    inputMed.addEventListener('blur', () => {
        setTimeout(() => {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
        }, 150);
    });

    btnAgregarMed.addEventListener('click', function () {
        if (!medicamentoSeleccionado) {
            alert('Selecciona un medicamento válido.');
            return;
        }
        const dosis = dosisInput.value.trim();
        const duracion = duracionInput.value.trim();
        if (!dosis || !duracion) {
            alert('Completa dosis y duración.');
            return;
        }
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>
                ${medicamentoSeleccionado.nombre}
                <input type="hidden" name="medicamento_id[]" value="${medicamentoSeleccionado.id}">
            </td>
            <td>
                ${dosis}
                <input type="hidden" name="dosis[]" value="${dosis}">
            </td>
            <td>
                ${duracion}
                <input type="hidden" name="duracion[]" value="${duracion}">
            </td>
            <td class="precio_med">
                ${medicamentoSeleccionado.precio.toFixed(2)}
                <input type="hidden" name="precio_med[]" value="${medicamentoSeleccionado.precio.toFixed(2)}">
            </td>
            <td>
                <button type="button" class="eliminar_medicamento">Eliminar</button>
            </td>
        `;
        tablaMed.appendChild(fila);

        // Limpiar campos
        inputMed.value = '';
        hiddenIdMed.value = '';
        dosisInput.value = '';
        duracionInput.value = '';
        medicamentoSeleccionado = null;

        actualizarTotal();
    });

    tablaMed.addEventListener('click', function (e) {
        if (e.target.classList.contains('eliminar_medicamento')) {
            e.target.closest('tr').remove();
            actualizarTotal();
        }
    });

    function actualizarTotal() {
        let total = parseFloat(precioConsultaInput.value) || 0;
        tablaMed.querySelectorAll('.precio_med').forEach(td => {
            total += parseFloat(td.textContent) || 0;
        });
        totalInput.value = total.toFixed(2);
    }

    precioConsultaInput.addEventListener('input', actualizarTotal);

    // Buscador de mascotas (no se toca, se mantiene igual)
    const buscador = document.getElementById('buscador_mascota');
    const sugerenciasMascota = document.getElementById('sugerencias_mascota');
    const mascotaIdInput = document.getElementById('mascota_id');
    let mascotaSeleccionada = null;

    buscador.addEventListener('input', function () {
        const query = buscador.value.trim();
        if (!query) {
            sugerenciasMascota.innerHTML = '';
            sugerenciasMascota.style.display = 'none';
            return;
        }
        fetch(`/buscar_mascota?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                sugerenciasMascota.innerHTML = '';
                sugerenciasMascota.style.display = data.length ? 'block' : 'none';
                data.forEach(mascota => {
                    const div = document.createElement('div');
                    div.textContent = mascota.nombre;
                    div.classList.add('sugerencia-item');
                    div.addEventListener('mousedown', function () {
                        buscador.value = mascota.nombre;
                        mascotaIdInput.value = mascota.id;
                        mascotaSeleccionada = mascota;
                        sugerenciasMascota.innerHTML = '';
                        sugerenciasMascota.style.display = 'none';
                    });
                    sugerenciasMascota.appendChild(div);
                });
            });
    });

    buscador.addEventListener('blur', () => {
        setTimeout(() => {
            sugerenciasMascota.innerHTML = '';
            sugerenciasMascota.style.display = 'none';
        }, 150);
    });
});