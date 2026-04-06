document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // File input and Drag & Drop UX
    const fileInput = document.getElementById('file-input');
    const fileMessage = document.querySelector('.file-message');
    const fileDropArea = document.querySelector('.file-drop-area');
    const loadingOverlay = document.getElementById('loading-overlay');

    const updateFileMessage = (file) => {
        if (file) {
            fileMessage.textContent = `Selected: ${file.name}`;
            fileMessage.style.color = "var(--success-color)";
        } else {
            fileMessage.textContent = "Drag & drop your .txt, .docx, or .pdf file here or click to browse";
            fileMessage.style.color = "";
        }
    };

    fileInput.addEventListener('change', (e) => {
        updateFileMessage(e.target.files[0]);
    });

    // Drag and Drop listeners
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, () => {
            fileDropArea.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, () => {
            fileDropArea.classList.remove('drag-over');
        }, false);
    });

    fileDropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileMessage(files[0]);
        }
    }, false);

    // Process Button
    const processBtn = document.getElementById('process-btn');
    const outputSection = document.getElementById('output-section');
    const pipelineStatus = document.getElementById('pipeline-status');
    const reportBody = document.getElementById('report-body');
    const finalTextOutput = document.getElementById('final-text-output');
    let currentFinalText = "";

    const showLoading = (show) => {
        if (show) {
            loadingOverlay.classList.remove('hidden');
            processBtn.disabled = true;
        } else {
            loadingOverlay.classList.add('hidden');
            processBtn.disabled = false;
        }
    };

    processBtn.addEventListener('click', async () => {
        const activeTab = document.querySelector('.tab-content.active').id;
        const formData = new FormData();

        if (activeTab === 'paste-tab') {
            const text = document.getElementById('text-input').value;
            if (!text.trim()) {
                alert("Please paste some text.");
                return;
            }
            formData.append('text', text);
        } else {
            const file = fileInput.files[0];
            if (!file) {
                alert("Please select a file.");
                return;
            }
            
            // Basic client-side validation
            const allowedExtensions = /(\.txt|\.docx|\.pdf)$/i;
            if (!allowedExtensions.exec(file.name)) {
                alert("Unsupported file type. Please upload a .txt, .docx, or .pdf file.");
                return;
            }
            
            formData.append('file', file);
        }

        showLoading(true);
        outputSection.classList.add('hidden');

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                outputSection.classList.remove('hidden');
                
                pipelineStatus.innerHTML = `<p style="color: var(--success-color);">Analyzed and Corrected! Found ${result.report.total_corrections} inconsistencies.</p>`;
                
                // Populate the Table
                reportBody.innerHTML = '';
                if(result.report.details.length === 0) {
                    reportBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">No proper noun inconsistencies detected.</td></tr>';
                } else {
                    result.report.details.forEach(item => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><strong>${item.canonical_form}</strong></td>
                            <td>${item.replacements_count}</td>
                            <td><span style="color:#94a3b8">${item.variants_found.join(', ')}</span></td>
                        `;
                        reportBody.appendChild(tr);
                    });
                }
                
                // Display text
                currentFinalText = result.final_text;
                finalTextOutput.textContent = currentFinalText;

                // Smooth scroll to results
                outputSection.scrollIntoView({ behavior: 'smooth' });

            } else {
                alert(`Error: ${result.detail || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert("An error occurred connecting to the server.");
        } finally {
            showLoading(false);
        }
    });

    // Handle Downloads
    document.getElementById('download-txt-btn').addEventListener('click', () => {
        if (!currentFinalText) return;
        const blob = new Blob([currentFinalText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'corrected_proper_nouns.txt';
        a.click();
        URL.revokeObjectURL(url);
    });

    document.getElementById('download-docx-btn').addEventListener('click', async () => {
        if (!currentFinalText) return;
        
        try {
            const dForm = new FormData();
            dForm.append("text", currentFinalText);
            
            const btn = document.getElementById('download-docx-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Generating...';
            
            const response = await fetch('/api/download-docx', {
                method: 'POST',
                body: dForm
            });
            
            if (!response.ok) throw new Error("Failed to generate DOCX");
            
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'corrected_proper_nouns.docx';
            a.click();
            URL.revokeObjectURL(url);
            
            btn.textContent = originalText;
        } catch (error) {
            alert("Error downloading DOCX: " + error.message);
        }
    });
});
