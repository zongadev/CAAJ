function publicarComentario() {
  // Envia el form por AJAX usando la función auxiliar del ejemplo
  queryAjaxForm("/publicar_comentario", "comments-list", "formComentario");
  // Limpia el textarea después de enviar
  document.getElementById("comentario").value = "";
}

function votarApunte(tipo) {
  const idApunte = window.location.search.match(/apunte=(\d+)/)?.[1];
  if (!idApunte) return;
  queryAjaxJson(
    "/votar_apunte",
    { id_apunte: idApunte, tipo: tipo },
    function (data) {
      if (data.success) {
        document.getElementById("like-count").textContent = data.likes;
        document.getElementById("dislike-count").textContent = data.dislikes;

        // Agregar feedback visual
        const upvoteBtn = document.querySelector(".upvote");
        const downvoteBtn = document.querySelector(".downvote");

        // Remover clases activas
        upvoteBtn.classList.remove("active");
        downvoteBtn.classList.remove("active");

        // Agregar clase activa solo si hay un voto (data.voto_actual no es null)
        if (data.voto_actual === "like") {
          upvoteBtn.classList.add("active");
        } else if (data.voto_actual === "dislike") {
          downvoteBtn.classList.add("active");
        }
        // Si data.voto_actual es null, no se agrega ninguna clase (voto removido)
      } else {
        if (data.requiresLogin) {
          alert('Debes iniciar sesión para votar');
          window.location.href = '/login';
        } else {
          alert(data.msg || "Error al votar");
        }
      }
    }
  );
}
