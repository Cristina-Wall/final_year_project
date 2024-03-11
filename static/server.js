const express = require('express');
const cors = require('cors');

process.chdir(__dirname);

const app = express();
const port = 3000;

// Enable CORS for all routes
app.use(cors({
    origin: 'http://localhost:3000', // Allow requests from this origin
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true, // Allow sending cookies and authentication headers
}));

// Serve your HTML files or other static assets
// app.use(express.static('static'));
app.use(express.static('static', { 'extensions': ['html', 'htm', 'js', 'css'], 'setHeaders': (res, path, stat) => { res.set('Content-Type', 'application/javascript'); } }));

// Route handler for the root path
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/../website/index.html');
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
