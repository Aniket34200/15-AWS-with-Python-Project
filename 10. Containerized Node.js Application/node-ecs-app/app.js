const express = require("express");

const app = express();

const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("Node.js App Running Successfully on ECS!");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});