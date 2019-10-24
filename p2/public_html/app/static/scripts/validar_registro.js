function validar(){
  var valido=true;
  var nombre = document.formulario.nombre.value;
  var tarjeta = document.formulario.tarjeta.value;
  var cvc = document.formulario.cvc.value;
  var mail = document.formulario.mail.value;
  var username = document.formulario.username.value;
  var password = document.formulario.password.value;
  var password2 = document.formulario.password2.value;
  if (!nombre || !tarjeta || !mail || !cvc || !username || !password || !password2){
    valido=false;
    alert("Hay campos sin rellenar");
  }else{
    //Usuario
    if (username.charAt(0) == " "){
      valido=false;
      alert("Usuario no puede comenzar con espacio");
    }
    else if (username.charAt(username.length - 1) == " "){
      valido=false;
      alert("Usuario no puede terminar con espacio");
    }
    else if (username.length<2){
      valido=false;
      alert("Usuario con menos de 2 caracteres");
    }
    //Contraseñas
    if (password != password2){
      valido=false;
      alert("Las contraseñas no coinciden");
    }
    //Mail
    if (!(/\S+@\S+\.\S/.test(mail))){ //No se si es una guarrada gg
      valido=false;
      alert("Email incorrecto\nTiene que ser 'x@x.x'");
    }
    //Nombre
    nombre = nombre.split(" ");
    if (!nombre[0] || !nombre[1] || !nombre[2]){
      valido=false;
      alert("Nombre incorrecto\nIncluir nombre y dos apellidos");
    }
    //Tarjeta
    if (isNaN(tarjeta)){
      valido=false;
      alert("Tarjeta incorrecta\nSolo debe incluir numeros");
    }
    else{
      if (tarjeta.length != 16){
        valido=false;
        alert("Tarjeta incorrecta\nDebe incluir 16 numeros");
      }
    }
    //CVC
    if (isNaN(cvc)){
      valido=false;
      alert("CVC incorrecto\nSolo debe incluir numeros");
    }
    else{
      if (cvc.length != 3){
        valido=false;
        alert("CVC incorrecto\nDebe incluir 3 numeros");
      }
    }
  }
  if (valido==true){
    alert("Informacion correcta");
  }
  return valido;
}
