document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscador_mascota');
    const sugerencias = document.getElementById('sugerencias_mascota');
    const mascotaIdInput = document.getElementById('mascota_id');
    let mascotaSeleccionada = null;

    buscador.addEventListener('input', function () {
        const query = buscador.value.trim();
        if (!query) {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
            document.getElementById('row-tabla-mascota').style.display = 'none';
            return;
        }
        fetch(`/buscar_mascotas_consulta?q=${encodeURIComponent(query)}`)
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
            if (!buscador.value || !mascotaIdInput.value) {
                document.getElementById('row-tabla-mascota').style.display = 'none';
            }
        }, 150);
    });

    document.querySelector('form').addEventListener('submit', function (e) {
        if (!mascotaIdInput.value) {
            e.preventDefault();
            alert('Selecciona una mascota de la lista.');
        }
    });

    function mostrarTablaMascota(mascota) {
        const rowDiv = document.getElementById('row-tabla-mascota');
        const tbody = document.querySelector('#tabla_mascota tbody');
        if (!mascota || !mascota.nombre) {
            tbody.innerHTML = '';
            rowDiv.style.display = 'none';
            return;
        }
        tbody.innerHTML = `
            <tr>
                <td>${mascota.nombre || ''}</td>
                <td>${mascota.edad || ''}</td>
                <td>${mascota.peso || ''}</td>
                <td>${mascota.especie || ''}</td>
                <td>${mascota.raza || ''}</td>
                <td>${mascota.propietario || ''}</td>
                <td><button type="button" id="eliminar_mascota_info" class="eliminar_mascota_info">Eliminar</button></td>
            </tr>
        `;
        rowDiv.style.display = 'block';
        const btnEliminar = document.getElementById('eliminar_mascota_info');
        if (btnEliminar) {
            btnEliminar.addEventListener('click', function () {
                tbody.innerHTML = '';
                rowDiv.style.display = 'none';
                buscador.value = '';
                mascotaIdInput.value = '';
            });
        }
    }
});
