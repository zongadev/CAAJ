function customValidez(campo, mensaje) { // Cambia el mensaje de error
  campo.setCustomValidity(mensaje);
}

function check(ID) { // Chequea el campo
  campo.setCustomValidity("");

  if (campo.validity.valueMissing) { // Si el campo está vacío
    customValidez(campo, "Este campo debe de estar completo");
  } else if (campo.validity.patternMismatch) { // Si el formato es incorrecto
    customValidez(campo, "El formato es incorrecto");
  } else {
    campo.setCustomValidity(""); // Si el campo es válido, limpia el mensaje
  }
  campo.reportValidity(); // Muestra el mensaje de error si es necesario
}

//se ejecuta al abrir la pagina, recorre todos los campos 
// que tengan la clase .editor-form y le asigna la funcion anonima
document.querySelector('.editor-form').addEventListener('submit', function (e) { // Al enviar el formulario
    let campos = ['titulo', 'contenido','tags','archivo']; // lista de IDs de los campos a validar
    let valido = true;
    for (var i = 0; i < campos.length; i++) { // Recorre los campos
      var id = campos[i];
      var campo = document.getElementById(id); // Obtiene el campo por ID
      check(id);
      if (!campo.checkValidity()) { // Si el campo no es false, se bolquea el envio
        valido = false;
      }
    }
  });