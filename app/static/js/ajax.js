function queryAjax(url, idDest,method="POST",dataSend=null) {
    // hace un request al servidor
    // url: donde vamos a pedir los datos
    // idDest: id del elemento donde metemos la respuesta
    // method: POST o GET
    // dataSend: datos a enviar (opcional)

    const xhr = new XMLHttpRequest(); // crea objeto AJAX     
    if(xhr) {
        xhr.timeout = 2000; // 2 segundos antes de explotar
        xhr.open(method, url, true); // abre la conexión (true = asincro)
        document.body.style.cursor = 'wait'; // muestra cursor de espera
                                             // para que el usuario sepa que algo está pasando

        xhr.onload = () => {
            // cuando termina el request
            document.body.style.cursor = 'default'; // cursor normal de nuevo
            textHTML = xhr.responseText; // agarra la respuesta
            setDataIntoNode(idDest,textHTML); // mete la respuesta en el HTML
            //console.log("Terminado con exito");
        };

        xhr.ontimeout = () => {
            // si se demora demasiado
            // document.body.style.cursor = 'default'; 
            console.log("Terminado por expiración de tiempo");
        };

        xhr.onloadend = () => {
            // cuando termina todo (bien o mal)
            document.body.style.cursor = 'default'; // vuelve a normal
        };  
        xhr.send(dataSend); // envía el request
    }
    else{
        console.log('No se pudo instanciar el objeto AJAX!'); // algo pasó mal
    }
}

function queryAjaxForm(url, idDest, idForm) {
    // agarra un form y lo envía por AJAX
    const form = document.getElementById(idForm);
    if (!form) return; // si no existe el form, sale
    const formData = new FormData(form); // convierte el form en datos

    const xhr = new XMLHttpRequest(); // crea objeto AJAX
    xhr.open('POST', url, true); // abre conexión POST
    document.body.style.cursor = 'wait'; // cursor de espera

    xhr.onload = function() {
        document.body.style.cursor = 'default'; // vuelve cursor normal
        if (xhr.status === 200) {
            // si todo salió bien
            // agrega el nuevo comentario a la lista
            const commentsList = document.getElementById(idDest);
            if (commentsList) {
                commentsList.innerHTML += xhr.responseText; // mete la respuesta en el html
            }
        } else {
            // si salió mal
            // muestra el error
            const errorMsg = document.getElementById('error-comment');
            if (errorMsg) errorMsg.textContent = 'Error al publicar el comentario.';
        }
    };

    xhr.onerror = function() {
        document.body.style.cursor = 'default'; // vuelve cursor normal
        // fallo la conexión
        const errorMsg = document.getElementById('error-comment');
        if (errorMsg) errorMsg.textContent = 'Error de red.';
    };

    xhr.send(formData); // envía el formulario
}

function queryAjaxJson(url, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    document.body.style.cursor = 'wait';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.body.style.cursor = 'default';
            if (xhr.status === 200 || xhr.status === 400 || xhr.status === 401) {
                try {
                    callback(JSON.parse(xhr.responseText));
                } catch (e) {
                    callback({success: false, msg: 'Error al procesar respuesta del servidor'});
                }
            } else {
                callback({success: false, msg: 'Error de red o servidor'});
            }
        }
    };
    xhr.send(JSON.stringify(data));
}