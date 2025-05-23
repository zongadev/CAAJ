const COLOR_FONDO_ERROR = "#ff6565";
const COLOR_FONDO_NORMAL = "#FFFFFF";

function setErrorMsg(id, msg) {
  document.getElementById("error-" + id).textContent = msg;
}
function clearErrorMsg(id) {
  document.getElementById("error-" + id).textContent = "";
}

function errorCambiarColorField(campo) {
  campo.style.background = COLOR_FONDO_ERROR;
}

function normalCambiarColorField(campo) {
  campo.style.background = COLOR_FONDO_NORMAL;
}

function validarComentario() {
  const campo = document.getElementById("comment");
  const valor = campo.value.trim();
  let errorMsg = "";

  // Solo letras, números, símbolos permitidos, mínimo 60 caracteres
  if (!valor) {
    errorMsg = "El comentario no puede estar vacío.";
  } else if (valor.length < 60) {
    errorMsg = "El comentario debe tener al menos 60 caracteres.";
  } else if (!/^[\w\d\s.,;:¡!¿?'"()\-_*+=@#$%&/\\[\]{}<>|^~`áéíóúÁÉÍÓÚüÜñÑ]+$/u.test(valor)) {
    errorMsg = "El comentario solo puede contener letras, números y símbolos permitidos.";
  }

  if (errorMsg) {
    setErrorMsg("comment", errorMsg);
    errorCambiarColorField(campo);
    return false;
  } else {
    clearErrorMsg("comment");
    normalCambiarColorField(campo);
    return true;
  }
}

// Validación en tiempo real
const commentField = document.getElementById("comment");
if (commentField) {
  commentField.addEventListener("input", validarComentario);
  commentField.addEventListener("blur", validarComentario);
}

// Validación al enviar
const btn = document.getElementById("publicar-comentario-btn");
if (btn) {
  btn.addEventListener("click", function (e) {
    if (!validarComentario()) {
      e.preventDefault();
    }
  });
}
