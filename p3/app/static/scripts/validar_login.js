function validar(){
  var valido = true;
  var nombre = document.formulario.username.value;
  var password = document.formulario.password.value;

  if (!nombre || !password){
    valido = false;
    alert("Hay campos sin rellenar");
  }

  return valido;
}

window.onload=function(){
  var misCookies = document.cookie;
  var listaCookies = misCookies.split(";");
  var flag = 0;
  var micookie = "";
  for (i in listaCookies){
    if (listaCookies[i].search("userID") > -1){
      flag = 1;
      var lacookie = listaCookies[i];
      var igual = lacookie.indexOf("=");
      micookie = lacookie.substring(igual+1);
    }
  }
  if (flag == 0){
    micookie = "";
  }
  document.formulario.username.value=micookie;
  return true;
}
