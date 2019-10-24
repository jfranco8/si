function validar(){
  var valido = true;
  var nombre = document.formulario.nombre.value;
  var tarjeta = document.formulario.tarjeta.value;
  var cvc = document.formulario.cvc.value;
  var mail = document.formulario.mail.value;
  var username = document.formulario.username.value;
  var password = document.formulario.password.value;
  var password2 = document.formulario.password2.value;
  var i = 0;

  if (!nombre || !tarjeta || !mail || !cvc || !username || !password || !password2){
    valido = false;
    alert("Hay campos sin rellenar");
  }else{
    //Usuario
    for (i=0; i<username.length; i++){
      if (username.charAt(i) == " "){
        if(valido == true) alert("Usuario no puede contener espacios");
        valido = false;
        break;
      }
    }
    if (username.length<2){
      if(valido == true) alert("Usuario con menos de 2 caracteres");
      valido = false;
    }
    //Contraseñas
    if (password != password2){
      if(valido == true) alert("Las contraseñas no coinciden");
      valido = false;
    }else if (password.length<8){
      if(valido == true) alert("Contraseña con menos de 8 caracteres");
      valido = false;
    }
    //Mail
    if (!(/\S+@\S+\.\S/.test(mail))){ //No se si es una guarrada gg
      if(valido == true) alert("Email incorrecto\nTiene que ser 'x@x.x'");
      valido = false;
    }
    //Nombre
    nombre = nombre.split(" ");
    if (!nombre[0] || !nombre[1] || !nombre[2]){
      if(valido == true) alert("Nombre incorrecto\nIncluir nombre y dos apellidos");
      valido = false;
    }
    //Tarjeta
    if (isNaN(tarjeta)){
      if(valido == true) alert("Tarjeta incorrecta\nSolo debe incluir numeros");
      valido = false;
    }
    else{
      if (tarjeta.length != 16){
        if(valido == true) alert("Tarjeta incorrecta\nDebe incluir 16 numeros");
        valido = false;
      }
    }
    //CVC
    if (isNaN(cvc)){
      if(valido == true) alert("CVC incorrecto\nSolo debe incluir numeros");
      valido = false;
    }
    else{
      if (cvc.length != 3){
        if(valido == true) alert("CVC incorrecto\nDebe incluir 3 numeros");
        valido = false;
      }
    }
  }
  return valido;
}
