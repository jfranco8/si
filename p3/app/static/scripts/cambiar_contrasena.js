function cambiar_pss(){
  var old = document.formulario.old.value
  var new1 = document.formulario.new1.value
  var new2 = document.formulario.new2.value
  var valido = true

  if (!new1 || !new2 || !old){
    valido = false;
    alert("Hay campos sin rellenar");
  }

  if (new1 != new2){
    if(valido == true) alert("Las contraseñas no coinciden");
    valido = false;
  }else if (new1.length<8){
    if(valido == true) alert("Contraseña con menos de 8 caracteres");
    valido = false;
  }
}
