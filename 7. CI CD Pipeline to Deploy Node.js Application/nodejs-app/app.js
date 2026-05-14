const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Simple API route
app.get('/api/message', (req, res) => {
    res.json({ message: "Hello from Node.js backend 🚀" });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});