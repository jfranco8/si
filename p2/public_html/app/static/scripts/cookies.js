function createCookie(name, value){
  var date = new Date();
  date.setTime(date.getTime() + (10 * 24 * 60 * 60 * 1000)); //Queremos que la cookie dure 10 días
  var expires = "; expires=" + date.toGMTString();
  document.cookie = name + "=" + value + expires + "; path=/login";
}

// function readCookie()
