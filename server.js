const express = require("express");
const cors = require("cors");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("public"));

/* ==============================
   BASE DE DATOS TEMPORAL
   ============================== */
let usuarios = [];

/* ==============================
   RUTA PRINCIPAL
   ============================== */
app.get("/", (req, res) => {
    res.send("Servidor funcionando correctamente 🚀");
});

/* ==============================
   REGISTRO
   ============================== */
app.post("/registro", (req, res) => {

    const { nombre, correo, password } = req.body;

    // Guardamos usuario en memoria
    usuarios.push({ nombre, correo, password });

    console.log("Usuarios registrados:");
    console.log(usuarios);

    res.json({
        mensaje: "Usuario registrado correctamente ✅"
    });
});

/* ==============================
   LOGIN
   ============================== */
app.post("/login", (req, res) => {

    const { correo, password } = req.body;

    const usuarioEncontrado = usuarios.find(
        user => user.correo === correo && user.password === password
    );

    if (usuarioEncontrado) {
        res.json({ mensaje: "Login exitoso ✅" });
    } else {
        res.status(401).json({ mensaje: "Correo o contraseña incorrectos ❌" });
    }
});

/* ==============================
   SERVIDOR
   ============================== */
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
