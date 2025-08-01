document.addEventListener('DOMContentLoaded', (event) => {
    // Initialize CodeMirror
    const editor = CodeMirror.fromTextArea(document.getElementById('codeInput'), {
        lineNumbers: true,
        mode: 'text/x-csrc',
        theme: 'default'
    });

    const compileBtn = document.getElementById('compileBtn');
    const outputElem = document.getElementById('output');
    const tokensElem = document.getElementById('tokens');
    const llvmIrElem = document.getElementById('llvm_ir');

    compileBtn.addEventListener('click', async () => {
        const code = editor.getValue();
        outputElem.textContent = "Compiling...";
        tokensElem.textContent = "";
        llvmIrElem.textContent = "";

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: code })
            });

            const result = await response.json();

            if (result.error) {
                outputElem.textContent = `Error: ${result.error}`;
            } else {
                outputElem.textContent = result.output;
                tokensElem.textContent = result.tokens;
                llvmIrElem.textContent = result.llvm_ir;
            }
        } catch (error) {
            outputElem.textContent = `An unexpected error occurred: ${error}`;
        }
    });
});