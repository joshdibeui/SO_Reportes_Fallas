/* ==============================
   AQUI IRA EL SCRIPT JS 
   ============================== */


/* Script para registro*/

document.getElementById("registroForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const datos = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    }; 

    try {
        const respuesta = await fetch("/registrodata", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();
        alert(resultado.mensaje);

    } catch (error) {
        alert("Error al registrar usuario");
        console.error(error);
    }
});
