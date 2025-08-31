const express = require("express");
const path = require("path");
const app = express();
const PORT = 3000;

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname,"public")));

// Routing
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname,"public", "Login.html"));
});

app.get("/Login.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public","Login.html"));
});

app.get("/Signup.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public","Signup.html"));
});

app.get("/Dashboard.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public","Dashboard.html"));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
