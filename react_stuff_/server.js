const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());

app.get('/select-path', (req, res) => {
    // PowerShell command with a Filter added for PDF files
    const command = `powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.OpenFileDialog; $f.Filter = 'PDF Files (*.pdf)|*.pdf'; $f.ShowDialog() | Out-Null; $f.FileName"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: stderr });
        }
        const selectedPath = stdout.trim();
        res.json({ path: selectedPath });
    });
});


// Add express.json middleware at the top of server.js to read JSON bodies
app.use(express.json());

// New endpoint to actually process the PDF
app.post('/process-pdf', (req, res) => {
    const { filePath } = req.body;

    if (!filePath) {
        return res.status(400).json({ error: "No file path provided" });
    }

    console.log(`Backend received path: ${filePath}`);

    const pythonScriptPath = path.join(__dirname, '..', 'python_logic', 'the_main_file.py');
    const pythonProcess = spawn('python', [pythonScriptPath, filePath]);
    let resultData = "";
    pythonProcess.stdout.on('data', (data) => {
        resultData += data.toString();
    });
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: "Python script failed" });
        }
        try {
            const parsedResult = JSON.parse(resultData);
            res.json({
                message: "Bridge Successful! ✅",
                data: parsedResult
            });
        } catch (e) {
            res.status(500).json({ error: "Failed to parse Python output" });
        }
    });
    
    // For now, let's just simulate success:
    setTimeout(() => {
        res.json({ 
            message: "Success!", 
            details: `Processed file at ${filePath}` 
        });
    }, 1000); 
});

app.listen(5000, () => console.log('Backend running on http://localhost:5000'));