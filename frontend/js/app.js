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

    // File input UX
    const fileInput = document.getElementById('file-input');
    const fileMessage = document.querySelector('.file-message');

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileMessage.textContent = `Selected: ${e.target.files[0].name}`;
            fileMessage.style.color = "var(--success-color)";
        } else {
            fileMessage.textContent = "Drag & drop your .txt file here or click to browse";
            fileMessage.style.color = "";
        }
    });

    // Process Button
    const processBtn = document.getElementById('process-btn');
    const outputSection = document.getElementById('output-section');
    const pipelineStatus = document.getElementById('pipeline-status');
    const reportBody = document.getElementById('report-body');
    const finalTextOutput = document.getElementById('final-text-output');
    let currentFinalText = "";

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
            formData.append('file', file);
        }

        processBtn.textContent = 'Processing...';
        processBtn.disabled = true;
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

            } else {
                alert(`Error: ${result.detail || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert("An error occurred connecting to the server.");
        } finally {
            processBtn.textContent = 'Analyze Consistency';
            processBtn.disabled = false;
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
            
            btn.textContent = 'Download .DOCX';
        } catch (error) {
            alert("Error downloading DOCX: " + error.message);
        }
    });
});
