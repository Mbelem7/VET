document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('proveedor_search');
    const sugerenciasDiv = document.getElementById('proveedor_sugerencias');
    const proveedorIdInput = document.getElementById('proveedor_id');
    const tablaProveedor = document.getElementById('tabla-proveedor-seleccionado');
    const tdNombre = document.getElementById('td-nombre');
    const tdApellido = document.getElementById('td-apellido');
    const tdEmpresa = document.getElementById('td-empresa');

    // Agregar referencia al botón eliminar
    const btnEliminarProveedor = document.getElementById('eliminar-proveedor');

    let timeout = null;

    input.addEventListener('input', function () {
        const query = input.value.trim();
        if (timeout) clearTimeout(timeout);
        if (query.length < 2) {
            sugerenciasDiv.innerHTML = '';
            sugerenciasDiv.style.display = 'none';
            return;
        }
        timeout = setTimeout(() => {
            fetch(`/buscar_proveedor?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    sugerenciasDiv.innerHTML = '';
                    if (data.length === 0) {
                        sugerenciasDiv.style.display = 'none';
                        return;
                    }
                    data.forEach(prov => {
                        const div = document.createElement('div');
                        div.className = 'sugerencia-item';
                        div.textContent = `${prov.nombre} ${prov.apellido} (${prov.empresa})`;
                        div.addEventListener('click', function () {
                            input.value = `${prov.nombre} ${prov.apellido}`;
                            proveedorIdInput.value = prov.id;
                            sugerenciasDiv.innerHTML = '';
                            sugerenciasDiv.style.display = 'none';
                            // Mostrar en tabla
                            tdNombre.textContent = prov.nombre;
                            tdApellido.textContent = prov.apellido;
                            tdEmpresa.textContent = prov.empresa;
                            tablaProveedor.style.display = '';
                        });
                        sugerenciasDiv.appendChild(div);
                    });
                    sugerenciasDiv.style.display = 'block';
                });
        }, 200);
    });

    // Si el usuario borra el input, ocultar tabla y limpiar id
    input.addEventListener('blur', function () {
        setTimeout(() => {
            if (!input.value.trim()) {
                proveedorIdInput.value = '';
                tablaProveedor.style.display = 'none';
                tdNombre.textContent = '';
                tdApellido.textContent = '';
                tdEmpresa.textContent = '';
            }
        }, 200);
    });

    // Evento para el botón eliminar proveedor
    if (btnEliminarProveedor) {
        btnEliminarProveedor.addEventListener('click', function () {
            proveedorIdInput.value = '';
            tablaProveedor.style.display = 'none';
            tdNombre.textContent = '';
            tdApellido.textContent = '';
            tdEmpresa.textContent = '';
            input.value = '';
            input.focus();
        });
    }
});
