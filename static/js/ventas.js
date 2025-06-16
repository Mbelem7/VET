document.addEventListener('DOMContentLoaded', function () {
  // Elementos del formulario
  const buscador = document.getElementById('buscador_producto');
  const sugerencias = document.getElementById('sugerencias');
  const productoIdInput = document.getElementById('producto_id');
  const tipoVentaSelect = document.getElementById('tipo_venta');
  const cantidadInput = document.getElementById('cantidad');
  const cantidadKgInput = document.getElementById('cantidad_kg');
  const precioUnitarioInput = document.getElementById('precio_unitario');
  const subtotalInput = document.getElementById('subtotal');
  const totalInput = document.getElementById('totv');
  const tablaProductos = document.getElementById('tabla-negocios').querySelector('tbody');
  const btnAgregar = document.getElementById('agregar_producto');

  let tipoVentaActual = 'unidad';
  let productoSeleccionado = null;

  // Mostrar/ocultar campos según tipo de venta y actualizar precio
  function actualizarTipoVenta() {
    tipoVentaActual = tipoVentaSelect.value;
    cantidadInput.value = '';
    cantidadKgInput.value = '';
    subtotalInput.value = '';

    if (tipoVentaActual === 'unidad') {
      document.getElementById('cantidad_unidad_div').style.display = '';
      document.getElementById('cantidad_peso_div').style.display = 'none';
    } else {
      document.getElementById('cantidad_unidad_div').style.display = 'none';
      document.getElementById('cantidad_peso_div').style.display = '';
    }

    if (productoSeleccionado) {
      if (tipoVentaActual === 'unidad') {
        precioUnitarioInput.value = productoSeleccionado.precio || 0;
      } else {
        precioUnitarioInput.value = productoSeleccionado.precio_unitario || 0;
      }
    } else {
      precioUnitarioInput.value = '';
    }
  }

  tipoVentaSelect.addEventListener('change', actualizarTipoVenta);

  // Autocompletado de productos
  buscador.addEventListener('input', function () {
    const query = buscador.value.trim();
    if (!query) {
      sugerencias.innerHTML = '';
      sugerencias.style.display = 'none';
      return;
    }
    fetch(`/buscar_producto?q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => {
        sugerencias.innerHTML = '';
        sugerencias.style.display = data.length ? 'block' : 'none';
        data.forEach(producto => {
          const div = document.createElement('div');
          div.textContent = producto.nombre;
          div.classList.add('sugerencia-item');
          div.addEventListener('mousedown', function () {
            buscador.value = producto.nombre;
            productoIdInput.value = producto.id;
            productoSeleccionado = producto;
            tipoVentaSelect.value = producto.tipo_venta;
            actualizarTipoVenta();
            sugerencias.innerHTML = '';
            sugerencias.style.display = 'none';
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

  // Calcular subtotal en tiempo real
  function calcularSubtotal() {
    const precioUnitario = parseFloat(precioUnitarioInput.value) || 0;
    let subtotal = 0;

    if (tipoVentaActual === 'unidad') {
      const cantidad = parseFloat(cantidadInput.value) || 0;
      subtotal = cantidad * precioUnitario;
    } else {
      const cantidadLibras = parseFloat(cantidadKgInput.value) || 0;
      const cantidadKg = cantidadLibras * 0.453592;
      subtotal = cantidadKg * precioUnitario;
    }

    subtotalInput.value = subtotal.toFixed(2);
  }

  cantidadInput.addEventListener('input', calcularSubtotal);
  cantidadKgInput.addEventListener('input', calcularSubtotal);
  precioUnitarioInput.addEventListener('input', calcularSubtotal);

  // Agregar producto a la tabla
  btnAgregar.addEventListener('click', () => {
    const nombre = buscador.value.trim();
    const productoId = productoIdInput.value;
    const tipoVenta = tipoVentaSelect.value;
    const cantidad = parseFloat(cantidadInput.value) || 0;
    const cantidadKg = parseFloat(cantidadKgInput.value) || 0;
    const precioUnitario = parseFloat(precioUnitarioInput.value) || 0;
    const subtotal = parseFloat(subtotalInput.value) || 0;

    if (!productoId || precioUnitario <= 0) {
      alert("Por favor, selecciona un producto válido.");
      return;
    }

    if (tipoVenta === 'unidad' && cantidad <= 0) {
      alert("Debe ingresar una cantidad de unidades mayor a cero.");
      return;
    }

    if (tipoVenta === 'peso' && cantidadKg <= 0) {
      alert("Debe ingresar una cantidad en libras mayor a cero.");
      return;
    }

    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${nombre}<input type="hidden" name="producto_id" value="${productoId}"></td>
      <td>${tipoVenta}<input type="hidden" name="tipo_venta" value="${tipoVenta}"></td>
      <td>
        ${tipoVenta === 'unidad' ? cantidad : '-'}
        <input type="hidden" name="cantidad" value="${cantidad}">
      </td>
      <td>
        ${tipoVenta === 'peso' ? cantidadKg : '-'}
        <input type="hidden" name="cantidad_kg" value="${cantidadKg}">
      </td>
      <td>${precioUnitario.toFixed(2)}<input type="hidden" name="precio_unitario" value="${precioUnitario.toFixed(2)}"></td>
      <td class="subtotal">${subtotal.toFixed(2)}<input type="hidden" name="subtotal" value="${subtotal.toFixed(2)}"></td>
      <td><button type="button" class="eliminar_producto">Eliminar</button></td>
    `;
    tablaProductos.appendChild(fila);

    buscador.value = '';
    productoIdInput.value = '';
    cantidadInput.value = '';
    cantidadKgInput.value = '';
    precioUnitarioInput.value = '';
    subtotalInput.value = '';
    productoSeleccionado = null;

    actualizarTotal();
  });

  tablaProductos.addEventListener('click', function (e) {
    if (e.target.classList.contains('eliminar_producto')) {
      e.target.closest('tr').remove();
      actualizarTotal();
    }
  });

  function actualizarTotal() {
    let total = 0;
    tablaProductos.querySelectorAll('.subtotal').forEach(td => {
      total += parseFloat(td.textContent) || 0;
    });
    totalInput.value = total.toFixed(2);
  }

  // Impedir la entrada de números negativos y caracteres no deseados en los inputs numéricos
  function impedirNegativosYE(inputElement) {
    inputElement.addEventListener('input', () => {
      // Si el valor es negativo, lo cambia a 0
      if (parseFloat(inputElement.value) < 0) {
        inputElement.value = 0;
      }
    });

    inputElement.addEventListener('keydown', (e) => {
      // Bloquear '-' y 'e' (mayúscula y minúscula)
      if (e.key === '-' ||
        e.key === 'Minus' ||
        e.key.toLowerCase() === 'e' ||
        e.key === '+' ||
        e.key === 'Add') {
        e.preventDefault();
      }
    });
  }

  // Aplicar a los inputs numéricos relevantes
  impedirNegativosYE(document.getElementById('cantidad'));
  impedirNegativosYE(document.getElementById('cantidad_kg'));



  actualizarTipoVenta();
});
