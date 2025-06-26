document.addEventListener('DOMContentLoaded', function () {
    // Impedir la entrada de números negativos y caracteres no deseados en los inputs numéricos

    function impedirNegativosYE(inputElement) {
        inputElement.addEventListener('input', () => {
            // Si el valor es negativo, lo cambia a 1
            if (parseFloat(inputElement.value) < 1) {
                inputElement.value = 1;
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

    // Selecciona todos los inputs numéricos y aplica la función
    document.querySelectorAll('input[type="number"]').forEach(input => {
        impedirNegativosYE(input);
    });

    // Para inputs de solo letras (opcional)
    document.querySelectorAll('input[data-letras]').forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]/g, '');
        });
    });

    // Solo agregar event listener si el input existe
    const telpInput = document.getElementById('telp');
    if (telpInput) {
        telpInput.addEventListener('input', function () {
            // Solo 8 dígitos
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
        });
    }

    // Dirección: elimina guiones al inicio
    const dirInput = document.getElementById('dirp');
    if (dirInput) {
        dirInput.addEventListener('input', function () {
            this.value = this.value.replace(/^[-]+/, '');
        });
    }

    // Validar que los inputs de tipo text no permitan guiones al inicio ni '+' en ninguna parte
    document.querySelectorAll('input[type="text"]').forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/^[-]+/, '').replace(/\+/g, '');
        });
    });

    // Función para impedir guiones al inicio y '+' en cualquier parte en inputs de tipo text
    function impedirGuionYMasInicio(inputElement) {
        inputElement.addEventListener('input', function () {
            this.value = this.value.replace(/^[-]+/, '').replace(/\+/g, '');
        });
    }

    // Ejemplo de uso: aplicar a todos los inputs de tipo text
    document.querySelectorAll('input[type="text"]').forEach(input => {
        impedirGuionYMasInicio(input);
    });

    // Selecciona los inputs numéricos por ID y aplica la validación solo si existen
    const precInput = document.getElementById('prec');
    if (precInput) impedirNegativosYE(precInput);
    const totalcInput = document.getElementById('totalc');
    if (totalcInput) impedirNegativosYE(totalcInput);
    const dosisInput = document.getElementById('dosis');
    if (dosisInput) impedirNegativosYE(dosisInput);
    const duracionInput = document.getElementById('duracion');
    if (duracionInput) impedirNegativosYE(duracionInput);

    // Aplica la función solo si el input existe
    const cedpInput = document.getElementById('cedp');
    if (cedpInput) impedirGuionYMasInicio(cedpInput);
});