
COLOR_FONDO_ERROR = '#ff6565';
COLOR_FONDO_NORMAL= '#FFFFFF'


function errorCambiarColorField(id){
    document.getElementById(id).style.background = COLOR_FONDO_ERROR;
}

function normalCambiarColorField(id){
    document.getElementById(id).style.background = COLOR_FONDO_NORMAL;
}

function customValidez(campo,txt){
    campo.addEventListener("invalid", function(){
            if(campo.validity.valueMissing){
                campo.setCustomValidity(txt);
            }
            if(campo.validity.patternMismatch){
                campo.setCustomValidity(txt);
            }
        });
}
function check(ID){
    campo = document.getElementById(ID)
    campo.setCustomValidity("")
    if(campo.validity.valueMissing){
        customValidez(campo,"Este campo debe de estar completo")
        ///cada vez que chequea, actualiza el Validity
    }
    if(campo.validity.patternMismatch){
        customValidez(campo,"El formato es incorrecto")
        errorCambiarColorField(ID)
    }
    if(!campo.validity.patternMismatch){
        normalCambiarColorField(ID)
    }
    
}