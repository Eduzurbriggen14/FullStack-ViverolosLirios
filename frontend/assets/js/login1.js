document.getElementById("login-form").addEventListener("submit", function (event) {
  event.preventDefault();

  // Obtener los valores del campo de usuario y contraseña dentro del evento de envío del formulario
  var usuario = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  console.log("usuario:", usuario);
  console.log("password:", password);

  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ usuario: usuario, password: password }),
  })
    .then((response) => {
      console.log("Respuesta del servidor:", response);
      return response.json();
    })
    .then((data) => {
      console.log("Datos recibidos:", data);
      if ("access_token" in data) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("es_administrador", data.es_administrador);
        window.location.href = "./index.html";
      } else {
        alert("Credenciales inválidas");
      }
    })
    .catch((error) => {
      console.error("Error", error);
      alert("Error de conexión");
    });
});