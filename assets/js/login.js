
COLOR_FONDO_ERROR = '#ff6565';
COLOR_FONDO_NORMAL= '#FFFFFF'

function errorCambiarColorField(campo){
    campo.style.background = COLOR_FONDO_ERROR;
}

function normalCambiarColorField(campo){
    campo.style.background = COLOR_FONDO_NORMAL;
}

function check(ID){
    campo = document.getElementById(ID)
    if(campo.validity.valueMissing){
        console.log("hola");
        errorCambiarColorField(campo)
    }
    if(campo.validity.patternMismatch){
        errorCambiarColorField(campo)
    }else{
        normalCambiarColorField(campo)
    }
}
//e es el evento al submitear
document.querySelector("#form").addEventListener('submit',function (e) { // Al enviar el formulario
    let campos = ['mail', 'con']; // lista de IDs de los campos a validar
    let valido = true;
    for (var i = 0; i < campos.length; i++) { // Recorre los campos
      var id = campos[i];
      var campo = document.getElementById(id); // Obtiene el campo por ID
      if (!campo.checkValidity()) { // Si el campo no es false, se bolquea el envio
        valido = false;
      }
    }
    if (!valido) {
        e.preventDefault();  //evita el submit 
    }
  });