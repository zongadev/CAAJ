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

// Email validation logic
function validarEmail(valor) {
  // Mismo patrón que antes
  return /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/.test(valor);
}

// Password validation logic
function validarPassword(valor) {
  // Al menos 8 caracteres, una mayúscula, una minúscula y un número
  return /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/.test(valor);
}

function check(ID) {
  let campo = document.getElementById(ID);
  let errorMsg = "";
  if (campo.validity.valueMissing) {
    errorCambiarColorField(campo);
    errorMsg = "Este campo es obligatorio.";
  } else if (ID === "mail" && !validarEmail(campo.value)) {
    errorCambiarColorField(campo);
    errorMsg = "Correo inválido.";
  } else if (ID === "con") {
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

// Validación al enviar el formulario
document.querySelector("#form").addEventListener("submit", function (e) {
  let campos = ["mail", "con"];
  let valido = true;
  for (var i = 0; i < campos.length; i++) {
    var id = campos[i];
    var campo = document.getElementById(id);
    check(id);
    if (campo.validity.valueMissing) {
      valido = false;
    }
    if (id === "mail" && !validarEmail(campo.value)) {
      valido = false;
    }
    if (id === "con" && !validarPassword(campo.value)) {
      valido = false;
    }
  }
  if (!valido) {
    e.preventDefault();
  }
});

// Limpiar mensajes al resetear
document.querySelector("#form").addEventListener("reset", function () {
  let campos = ["mail", "con"];
  campos.forEach((id) => {
    clearErrorMsg(id);
    normalCambiarColorField(document.getElementById(id));
  });
});

// Validar en tiempo real mientras el usuario escribe
["mail", "con"].forEach(function (id) {
  var campo = document.getElementById(id);
  campo.addEventListener("input", function () {
    check(id);
  });
});
