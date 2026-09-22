// Configuracion ESLint (equivalente a pylint para este proyecto JS nativo).
// Los scripts se cargan como <script> sueltos (sin modulos ni build), por lo
// que cada pantalla comparte funciones/variables globales definidas en
// js/datos.js y js/app.js. Este archivo declara esos globales para que
// ESLint no los marque como "no definidos".

const globalesDelProyecto = {
  // Definidos en js/app.js
  pantallas: 'readonly',
  registrarPantalla: 'writable',
  cargarPantalla: 'writable',
  estado: 'writable',
  establecerRol: 'writable',
  volverAlSelectorDeRol: 'writable',
  actualizarNavegacion: 'writable',

  // Definidos en js/datos.js
  datos: 'writable',
  generarId: 'writable',
  obtenerClientePorId: 'writable',
  clientesFiltrados: 'writable',
  clientesActivos: 'writable',
  existeCorreoDuplicado: 'writable',
  nombreCoach: 'writable',
  rutinasDeCliente: 'writable',
  rutinaActivaDeCliente: 'writable',
  obtenerRutinaPorId: 'writable',
  eliminarRutina: 'writable',
  medicionesDeCliente: 'writable',
  existeMedicionEnFecha: 'writable'
};

module.exports = [
  {
    ignores: ['node_modules/**']
  },
  {
    files: ['js/**/*.js', 'pantallas/**/*.js'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'script',
      globals: {
        window: 'readonly',
        document: 'readonly',
        ...globalesDelProyecto
      }
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      eqeqeq: 'warn',
      'no-var': 'warn'
    }
  },
  {
    files: ['test/**/*.js'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'commonjs',
      globals: {
        require: 'readonly',
        module: 'readonly',
        __dirname: 'readonly',
        console: 'readonly'
      }
    }
  }
];
