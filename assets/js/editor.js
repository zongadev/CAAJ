function customValidez(campo, mensaje) { // Cambia el mensaje de error
  campo.setCustomValidity(mensaje);
}

function check(ID) { // Chequea el campo
  campo.setCustomValidity("");

  if (campo.validity.valueMissing) {
    customValidez(campo, "Este campo debe de estar completo");
  } else if (campo.validity.patternMismatch) {
    customValidez(campo, "El formato es incorrecto");
  } else {
    campo.setCustomValidity(""); //limpia el mensaje
  }
  campo.reportValidity(); // Muestra el mensaje de error si es necesario
}

//se ejecuta al abrir la pagina
document.querySelector('.editor-form').addEventListener('submit', 
  function (e) { //al apretar submit
    let campos = ['titulo', 'contenido','tags','archivo']; //campos a validar
    let valido = true;
    for (var i = 0; i < campos.length; i++) {
      var id = campos[i];
      var campo = document.getElementById(id); 
      check(id); //manda el id para ser comprobado
      if (!campo.checkValidity()) { // Si el campo no es false, se bolquea el envio
        valido = false;
      }
    }
    if (!valido) { // Si el campo no es valido, se bloquea el envio
      e.preventDefault(); // Bloquea el envio del formulario
    }
  });