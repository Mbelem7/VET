document.addEventListener('DOMContentLoaded', function () {
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

    document.getElementById('telp').addEventListener('input', function () {
        // Solo 8 dígitos
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }
    });

        // Dirección: elimina guiones al inicio
    const dirInput = document.getElementById('dirp');
    if (dirInput) {
        dirInput.addEventListener('input', function () {
            this.value = this.value.replace(/^[-]+/, '');
        });
    }

});