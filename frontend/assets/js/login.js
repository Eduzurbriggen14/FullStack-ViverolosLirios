const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const data = {
    usuario: username,
    password: password,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const responseData = await response.json();
      const { acces_token, es_administrador } = responseData;

      // Guardar el estado del usuario (es_administrador) en el LocalStorage
      localStorage.setItem("es_administrador", es_administrador);

      // Redirigir al index.html
      window.location.href = "./index.html";
    } else {
      const errorData = await response.json();
      alert(errorData.mensaje);
    }
  } catch (error) {
    console.error("Error al enviar solicitud:", error);
    alert("Se produjo un error al enviar el formulario. Pruebe de nuevo.");
  }
});