COLOR_FONDO_ERROR = "#ff6565";
COLOR_FONDO_NORMAL = "#FFFFFF";

function customValidez(campo, mensaje) {
  // Cambia el mensaje de error
  campo.setCustomValidity(mensaje);
}

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

function check(ID) {
  var campo = document.getElementById(ID);
  let errorMsg = "";
  campo.setCustomValidity("");

  if (campo.validity.valueMissing) {
    errorMsg = "Este campo debe de estar completo";
    errorCambiarColorField(campo);
  } else if (campo.validity.patternMismatch) {
    errorMsg = "El formato es incorrecto";
    errorCambiarColorField(campo);
  } else if (
    ID === "materia" &&
    (campo.value === "" || campo.selectedIndex === 0)
  ) {
    errorMsg = "Selecciona una materia";
    errorCambiarColorField(campo);
  } else if (ID === "archivo" && (!campo.files || campo.files.length === 0)) {
    errorMsg = "Debes adjuntar un archivo";
    errorCambiarColorField(campo);
  } else if (ID === "tags" && campo.value.trim() !== "") {
    // Validar que cada tag sea una sola palabra (sin espacios) y separadas por coma
    let tagsArr = campo.value.split(",");
    let invalid = tagsArr.some((tag) => /\s/.test(tag) || tag === "");
    if (invalid) {
      errorMsg =
        "Cada etiqueta debe ser una sola palabra, separadas por comas y sin espacios";
      errorCambiarColorField(campo);
    }
  }

  if (errorMsg) {
    setErrorMsg(ID, errorMsg);
    campo.setCustomValidity(errorMsg);
    campo.reportValidity();
  } else {
    clearErrorMsg(ID);
    normalCambiarColorField(campo);
    campo.setCustomValidity("");
  }
}

//se ejecuta al abrir la pagina
document.querySelector("#submit-btn").addEventListener("click", function (e) {
  console.log("submit");
  //al apretar submit
  let campos = ["titulo", "contenido", "tags", "archivo", "materia", "visibilidad"]; //agregado visibilidad
  let valido = true;
  for (var i = 0; i < campos.length; i++) {
    var id = campos[i];
    var campo = document.getElementById(id);
    check(id); //manda el id para ser comprobado
    if (!campo.checkValidity()) {
      // Si el campo no es false, se bolquea el envio
      valido = false;
    }
  }
  if (!valido) {
    // Si el campo no es valido, se bloquea el envio
    e.preventDefault(); // Bloquea el envio del formulario
  } else {
    // Mostrar el HTML convertido y loguear solo en submit
    e.preventDefault();
    var markdown = document.getElementById("contenido").value;
    var html = markdownToHtml(markdown);
    console.log(html);
  }
});

// Real-time validation (input/change)
["titulo", "materia", "contenido", "tags", "archivo", "visibilidad"].forEach(function (id) {
  var campo = document.getElementById(id);
  if (campo) {
    campo.addEventListener("input", function () {
      check(id);
    });
    campo.addEventListener("blur", function () {
      check(id);
    });
    // For file and select, also listen to change
    if (campo.type === "file" || campo.tagName === "SELECT") {
      campo.addEventListener("change", function () {
        check(id);
      });
    }
  }
});

// Simple Markdown to HTML conversion
function markdownToHtml(md) {
  // Titulos: #, ##, ###
  md = md.replace(/^### (.*)$/gm, "<h3>$1</h3>");
  md = md.replace(/^## (.*)$/gm, "<h2>$1</h2>");
  md = md.replace(/^# (.*)$/gm, "<h1>$1</h1>");

  // Negritas: **text**
  md = md.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Italica: *text*
  md = md.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Links: [text](url)
  md = md.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Listas: - item
  md = md.replace(/^- (.*)$/gm, "<li>$1</li>");

  // Listas <li> in <ul>
  md = md.replace(/(<li>[\s\S]*?<\/li>)/g, function (match) {
    // If already inside <ul>, skip
    if (/^<ul>/.test(match)) return match;
    return "<ul>" + match + "</ul>";
  });

  // Saltos de linea
  md = md.replace(/\n/g, "<br>");
  return md;
}
