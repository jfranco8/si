function validar(){
  var valido=true;
  var nombre = document.formulario.nombre.value;
  var tarjeta = document.formulario.tarjeta.value;
  var mail = document.formulario.mail.value;
  var fecha = document.formulario.fecha.value;
  var username = document.formulario.username.value;
  var password = document.formulario.password.value;
  var password2 = document.formulario.password2.value;


  if (!nombre || !tarjeta || !mail || !fecha || !username || !password || !password2){
    valido=false;
    alert("Hay campos sin rellenar");
  }/*else{
    if (username.length<3){
      valido=false;
      alert("Usuario con menos de 3 caracteres");
    }

    if (!(/\S+@\S+\.\S/.test(mail))){
      valido=false;
      alert("Email incorrecto");
    }
  }*/
  if (valido==true){
    alert("Informacion correcta");
  }
  return valido;
}
