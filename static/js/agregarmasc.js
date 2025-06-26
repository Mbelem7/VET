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

    //agregar mascota con propietario 

    // Mostrar/ocultar buscador según el checkbox
    document.getElementById('check-propietario-registrado').addEventListener('change', function () {
        const buscadorRow = document.getElementById('buscador-propietario-row');
        const tablaRow = document.getElementById('row-tabla-propietario');
        if (this.checked) {
            buscadorRow.style.display = '';
            tablaRow.style.display = '';
        } else {
            buscadorRow.style.display = 'none';
            tablaRow.style.display = 'none';
        }
    });

    // Autocompletado de propietarios
    const input = document.getElementById('buscador_propietario');
    const sugerencias = document.getElementById('sugerencias_propietario');
    const hiddenId = document.getElementById('propietario_id');

    input.addEventListener('input', function () {
        const texto = input.value.trim();
        if (!texto) {
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
            return;
        }
        fetch(`/buscar_propietario?correo=${encodeURIComponent(texto)}`)
            .then(res => res.json())
            .then(data => {
                sugerencias.innerHTML = '';
                sugerencias.style.display = data.length ? 'block' : 'none';
                data.forEach(item => {
                    // Solo mostrar correo y nombre completo, nunca el id
                    const div = document.createElement('div');
                    div.textContent = item.correo + ' (' + item.nombre + ' ' + item.apellido + ')';
                    div.classList.add('sugerencia-item');
                    div.addEventListener('mousedown', () => {
                        input.value = item.nombre + ' ' + item.apellido;
                        hiddenId.value = item.id; // El id solo se guarda oculto
                        sugerencias.innerHTML = '';
                        sugerencias.style.display = 'none';
                        // Mostrar datos completos en la tabla
                        fetch(`/obtener_propietario?correo=${encodeURIComponent(item.correo)}`)
                            .then(res => res.json())
                            .then(datos => mostrarPropietarioSeleccionado(datos));
                    });
                    sugerencias.appendChild(div);
                });
            });
    });

    function mostrarPropietarioSeleccionado(datos) {
        const tabla = document.getElementById('tabla_propietario').querySelector('tbody');
        tabla.innerHTML = `
            <tr>
              <td>${datos.nombre}</td>
              <td>${datos.apellido}</td>
              <td>${datos.cedula}</td>
              <td>${datos.telefono}</td>
              <td>${datos.correo}</td>
              <td>${datos.direccion}</td>
              <td>
                <button type="button" class="eliminar-propietario btnproducto">Eliminar</button>
              </td>
            </tr>
        `;
        document.getElementById('row-tabla-propietario').style.display = '';
        // El id nunca se muestra en la tabla
        tabla.querySelector('.eliminar-propietario').addEventListener('click', function() {
            tabla.innerHTML = '';
            document.getElementById('row-tabla-propietario').style.display = 'none';
            document.getElementById('buscador_propietario').value = '';
            document.getElementById('propietario_id').value = '';
        });
    }
});
