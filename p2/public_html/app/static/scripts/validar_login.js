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
