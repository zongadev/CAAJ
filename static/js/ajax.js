function queryAjax(url, idDest,method="POST",dataSend=null) {
    /**Realiza una una petición request al servidor 'url'. NO envía datos 
     * al servidor 'xhr.send(null)', sólo hace la petición a la url y 
     * almacena la respuesta dentro del nodo cuyo id sea 'idDest'
     * 
     * url:    es la dirección donde se obtiene los datos (es el servidor)
     * idDest: es el id de un elemento html de la página. Es donde se escribirán 
     *         los datos recibido de la url.
     * method: es el metodo del request. Es la forma en que se trasnmite los datos
     *         en el protocolo htttp. Puede ser POST o GET. Por default es POST.
     * 
     * dataSend: son los datos que se envian al servidor en la petición. Por lo general 
     *           le asignamos 'FormData' donde enviaremos un estructura clave-valor.
     *           Si dataSend=null entonces en la paticion no estamos enviando datos 
     *           hacia el servidor.
     *    
     */

    const xhr = new XMLHttpRequest();                          // Creo el objeto AJAX     
    if(xhr) {
        xhr.timeout = 2000;                                    // setear el tiempo de timeout.
        xhr.open(method, url, true);                           // Abre la connección AJAX. false = sincro , true = asincro
        document.body.style.cursor = 'wait';                   // Setea la espera: Poner el cursor del mouse en espera
                                                               // otra opocion sería setear una imagen de espera en el div   

        xhr.onload = () => {
            // Evento load  se activa cuando una solicitud XMLHttpRequest 
            // se completa exitosamente.
            document.body.style.cursor = 'default';        // Resetea la espera: Poner el cursor del mouse en normal
            textHTML = xhr.responseText;                   // RECUPERA la respuesta que viene del servidor en formato html
            setDataIntoNode(idDest,textHTML);  
            //console.log("Terminado con exito");
        };

        xhr.ontimeout = () => {
            // Evento timeout se activa cuando la solicitud finaliza debido a que 
            // expira el tiempo preestablecido.
            // document.body.style.cursor = 'default'; 
            console.log("Terminado por expiración de tiempo");
        };

        xhr.onloadend = () => {
            // El evento 'loadend' se activa cuando se completa una solicitud, ya sea con éxito 
            // (después de 'load') o sin éxito  (por un 'timeout', un 'abort', o un 'error')
            document.body.style.cursor = 'default';  
                     
        };  
        xhr.send(dataSend); // Envio de solicitud 'request' al sevidor
    }
    else{
        console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección
    }
}

function queryAjaxForm(url, idDest, idForm) {
    const form = document.getElementById(idForm);
    if (!form) return;
    const formData = new FormData(form);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    document.body.style.cursor = 'wait';

    xhr.onload = function() {
        document.body.style.cursor = 'default';
        if (xhr.status === 200) {
            // Agrega el nuevo comentario al final de la lista
            const commentsList = document.getElementById(idDest);
            if (commentsList) {
                commentsList.innerHTML += xhr.responseText;
            }
        } else {
            // Muestra el error en el span de error
            const errorMsg = document.getElementById('error-comment');
            if (errorMsg) errorMsg.textContent = 'Error al publicar el comentario.';
        }
    };

    xhr.onerror = function() {
        document.body.style.cursor = 'default';
        const errorMsg = document.getElementById('error-comment');
        if (errorMsg) errorMsg.textContent = 'Error de red.';
    };

    xhr.send(formData);
}

function queryAjaxJson(url, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    document.body.style.cursor = 'wait';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.body.style.cursor = 'default';
            if (xhr.status === 200) {
                callback(JSON.parse(xhr.responseText));
            } else {
                callback({success: false, msg: 'Error de red o servidor'});
            }
        }
    };
    xhr.send(JSON.stringify(data));
}