const { exec } = require('child_process');
const express = require('express');
const app = express();
const port = 3000;

// 1. Chạy Python khi start Node
exec('python get_ip.py', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Python stderr: ${stderr}`);
        return;
    }
    console.log(`Python output: ${stdout}`);
});

// 2. Serve file HTML + ip.txt
app.use(express.static('src'));

app.listen(port, () => {
    console.log(`Server chạy tại http://localhost:${port}`);
});