import React, { useState, useEffect } from 'react';

function App() {
  const [filePath, setFilePath] = useState('');
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({ message: '', type: '' });

  // Auto-hide notification after 3 seconds
  useEffect(() => {
    if (notification.message) {
      const timer = setTimeout(() => setNotification({ message: '', type: '' }), 3000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  const showNotify = (msg, type) => setNotification({ message: msg, type: type });

  const handleBrowse = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/select-path');
      const data = await response.json();
      if (data.path) {
        setFilePath(data.path);
        showNotify("File path captured! 📂", "success");
      } else {
        showNotify("Selection cancelled ❌", "info");
      }
    } catch (err) {
      showNotify("Connection to server failed 🔌", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleProcessFile = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/process-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filePath }),
      });
      const result = await response.json();
      showNotify(`Success: ${result.message} 🚀`, "success");
    } catch (err) {
      showNotify("Processing failed ⚠️", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Toast Notification */}
      {notification.message && (
        <div style={{ ...styles.notification, ...styles[notification.type] }}>
          {notification.message}
        </div>
      )}

      <div style={styles.card}>
        <h1 style={styles.header}>PDF Wizard 🪄</h1>
        <p style={styles.subText}>Find and process your local PDF files instantly.</p>

        <button 
          style={loading ? {...styles.btn, ...styles.btnLoading} : styles.btnSelect} 
          onClick={handleBrowse}
          disabled={loading}
        >
          {loading ? 'Searching... 🔍' : 'Browse for Research Papers 📂'}
        </button>

        {filePath && (
          <div style={styles.pathArea}>
            <p style={styles.pathLabel}>📍 Target Location:</p>
            <code style={styles.pathCode}>{filePath}</code>
            
            <button 
              style={styles.btnProcess} 
              onClick={handleProcessFile}
              disabled={loading}
            >
              Launch Backend Task 🚀
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Beautified Styles
const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
  },
  card: {
    background: 'white',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
    textAlign: 'center',
    width: '450px',
    transition: 'all 0.3s ease',
  },
  header: { color: '#2d3436', marginBottom: '10px' },
  subText: { color: '#636e72', marginBottom: '30px' },
  btn: {
    width: '100%',
    padding: '15px',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  btnSelect: {
    backgroundColor: '#0984e3',
    color: 'white',
    padding: '15px',
    borderRadius: '10px',
    border: 'none',
    width: '100%',
    fontWeight: 'bold',
    cursor: 'pointer',
    boxShadow: '0 4px 15px rgba(9, 132, 227, 0.3)',
  },
  btnProcess: {
    backgroundColor: '#00b894',
    color: 'white',
    padding: '12px',
    marginTop: '20px',
    borderRadius: '10px',
    border: 'none',
    width: '100%',
    fontWeight: 'bold',
    cursor: 'pointer',
    boxShadow: '0 4px 15px rgba(0, 184, 148, 0.3)',
  },
  btnLoading: { backgroundColor: '#b2bec3', cursor: 'not-allowed' },
  pathArea: {
    marginTop: '30px',
    padding: '20px',
    backgroundColor: '#f1f2f6',
    borderRadius: '12px',
    textAlign: 'left',
    animation: 'fadeIn 0.5s ease-in',
  },
  pathLabel: { fontSize: '12px', fontWeight: 'bold', color: '#636e72', margin: '0 0 5px 0' },
  pathCode: { wordBreak: 'break-all', fontSize: '13px', color: '#d63031' },
  notification: {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '15px 25px',
    borderRadius: '8px',
    color: 'white',
    fontWeight: 'bold',
    boxShadow: '0 5px 15px rgba(0,0,0,0.2)',
    zIndex: 1000,
    animation: 'slideIn 0.3s ease-out',
  },
  success: { backgroundColor: '#00b894' },
  error: { backgroundColor: '#d63031' },
  info: { backgroundColor: '#0984e3' },
};

export default App;