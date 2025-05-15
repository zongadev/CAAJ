
COLOR_FONDO_ERROR = '#ff6565';
COLOR_FONDO_NORMAL= '#FFFFFF'

function errorCambiarColorField(id){
    document.getElementById(id).style.background = COLOR_FONDO_ERROR;
}

function normalCambiarColorField(id){
    document.getElementById(id).style.background = COLOR_FONDO_NORMAL;
}
function checkemail(emailID){
    const re = new RegExp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    var testeo = re.test(document.getElementById(emailID).value)
    if(!testeo){
        errorCambiarColorField(emailID)
    }
    if(testeo){
        normalCambiarColorField(emailID)
    }
    return testeo
}

function checkpassword(passID){
    const re = new RegExp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")
    var testeo = re.test(document.getElementById(passID).value)
    if(!testeo){
        errorCambiarColorField(passID)
    }
    if(testeo){
        normalCambiarColorField(passID)
        console.log("Hola")
    }
    return testeo
}