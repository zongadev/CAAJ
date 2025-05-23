COLOR_FONDO_ERROR = "#ff6565";
COLOR_FONDO_NORMAL = "#FFFFFF";

// Helper: set error message under input
function setErrorMsg(id, msg) {
  document.getElementById("error-" + id).textContent = msg;
}

// Helper: clear error message
function clearErrorMsg(id) {
  document.getElementById("error-" + id).textContent = "";
}

function errorCambiarColorField(campo) {
  campo.style.background = COLOR_FONDO_ERROR;
}

function normalCambiarColorField(campo) {
  campo.style.background = COLOR_FONDO_NORMAL;
}

// Password validation logic
function validarPassword(valor) {
  // Al menos 8 caracteres, una mayúscula, una minúscula y un número
  return /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/.test(valor);
}

// Add pattern validation for nombre, apellido, and mail in JS
function validarNombre(valor) {
  // Solo letras y espacios
  return /^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$/.test(valor);
}
function validarApellido(valor) {
  // Letras, espacios, apóstrofes y guiones
  return /^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$/.test(valor);
}
function validarMail(valor) {
  // Mismo patrón que antes
  return /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/.test(valor);
}

function check(ID) {
  let campo = document.getElementById(ID);
  let errorMsg = "";
  campo.setCustomValidity("");

  if (campo.validity.valueMissing) {
    errorCambiarColorField(campo);
    errorMsg = "Este campo es obligatorio.";
  } else if (ID === "nom01" && !validarNombre(campo.value)) {
    errorCambiarColorField(campo);
    errorMsg = "Solo letras y espacios.";
  } else if (ID === "ape01" && !validarApellido(campo.value)) {
    errorCambiarColorField(campo);
    errorMsg = "Apellido inválido.";
  } else if (ID === "mail01" && !validarMail(campo.value)) {
    errorCambiarColorField(campo);
    errorMsg = "Correo inválido.";
  } else if (ID === "con01") {
    if (!validarPassword(campo.value)) {
      errorCambiarColorField(campo);
      errorMsg =
        "Mínimo 8 caracteres, una mayúscula, una minúscula y un número.";
    } else {
      normalCambiarColorField(campo);
    }
  } else {
    normalCambiarColorField(campo);
  }

  if (errorMsg) {
    setErrorMsg(ID, errorMsg);
    campo.setCustomValidity(errorMsg);
    campo.reportValidity();
  } else {
    clearErrorMsg(ID);
    campo.setCustomValidity("");
  }
}

//e es el evento al submitear
document.querySelector("#regis-form").addEventListener("submit", function (e) {
  // Al enviar el formulario
  let campos = ["nom01", "ape01", "mail01", "con01"]; // lista de IDs de los campos a validar
  let valido = true;
  for (var i = 0; i < campos.length; i++) {
    // Recorre los campos
    var id = campos[i];
    var campo = document.getElementById(id); // Obtiene el campo por ID
    check(id); // fuerza la validación y muestra mensajes
    if (campo.validity.valueMissing) {
      d;
      valido = false;
    }
    if (id === "con01" && !validarPassword(campo.value)) {
      valido = false;
    }
  }
  if (!valido) {
    e.preventDefault(); //evita el submit
  }
});

// Limpiar mensajes al resetear
document.querySelector("#regis-form").addEventListener("reset", function () {
  let campos = ["nom01", "ape01", "mail01", "con01"];
  campos.forEach((id) => {
    clearErrorMsg(id);
    normalCambiarColorField(document.getElementById(id));
  });
});

["nom01", "ape01", "mail01", "con01"].forEach(function (id) {
  var campo = document.getElementById(id);
  if (campo) {
    campo.addEventListener("input", function () {
      check(id);
    });
  }
});
