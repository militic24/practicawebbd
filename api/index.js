const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Usuario hardcodeado (ejemplo)
const usuario = {
  username: 'mildred',
  password: '1234'
};

// Endpoint de login
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  if (username === usuario.username && password === usuario.password) {
    res.json({ success: true });
  } else {
    res.status(401).json({ success: false, message: 'Credenciales incorrectas' });
  }
});

app.listen(3001, () => {
  console.log('API corriendo en http://localhost:3001');
});
