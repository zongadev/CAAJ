function editarComentario(id) {
  // Cancelar cualquier edición activa antes de abrir una nueva
  const edicionesActivas = document.querySelectorAll('[id^="comment-edit-"]');
  edicionesActivas.forEach((edit) => {
    if (edit.style.display === "block") {
      const editId = edit.id.replace("comment-edit-", "");
      if (editId !== id.toString()) {
        cancelarEdicion(editId);
      }
    }
  });

  const commentText = document.getElementById(`comment-text-${id}`);
  const commentEdit = document.getElementById(`comment-edit-${id}`);

  if (commentText && commentEdit) {
    commentText.style.display = "none";
    commentEdit.style.display = "block";
  }
}

function cancelarEdicion(id) {
  const commentText = document.getElementById(`comment-text-${id}`);
  const commentEdit = document.getElementById(`comment-edit-${id}`);
  const textarea = document.getElementById(`comment-textarea-${id}`);

  if (commentText && commentEdit && textarea) {
    // Restaurar texto original
    textarea.value = commentText.textContent.trim();
    commentText.style.display = "block";
    commentEdit.style.display = "none";
  }
}

function guardarComentario(id) {
  const textarea = document.getElementById(`comment-textarea-${id}`);
  const nuevoContenido = textarea.value.trim();

  if (!nuevoContenido) {
    alert("El comentario no puede estar vacío");
    return;
  }

  // Enviar al servidor
  fetch("/actualizar_comentario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id_comentario: id,
      contenido: nuevoContenido,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Actualizar el texto del comentario
        const commentText = document.getElementById(`comment-text-${id}`);
        commentText.textContent = nuevoContenido;

        // Ocultar editor
        cancelarEdicion(id);
      } else {
        alert(data.msg || "Error al actualizar el comentario");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al actualizar el comentario");
    });
}
