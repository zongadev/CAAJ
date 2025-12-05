function publicarComentario() {
  // Envia el form por AJAX usando la función auxiliar del ejemplo
  queryAjaxForm('/publicar_comentario', 'comments-list', 'formComentario');
  // Limpia el textarea después de enviar
  document.getElementById('comentario').value = '';
}

function votarApunte(tipo) {
    const idApunte = window.location.search.match(/apunte=(\d+)/)?.[1];
    if (!idApunte) return;
    queryAjaxJson('/votar_apunte', {id_apunte: idApunte, tipo: tipo}, function(data) {
        if (data.success) {
            document.getElementById('like-count').textContent = data.likes;
            document.getElementById('dislike-count').textContent = data.dislikes;
        } else {
            alert(data.msg || 'Error al votar');
        }
    });
}
