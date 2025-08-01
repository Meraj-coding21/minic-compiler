import os
import subprocess
from flask import Flask, render_template, request, jsonify
from compiler.lexer import lexer
from compiler.parser import parser
from compiler.codegen import CodeGen

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates/'),
            static_folder=os.path.join(BASE_DIR, 'frontend/static/'))

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    c_code = request.json.get('code', '')
    if not c_code:
        return jsonify({'error': 'No code provided'}), 400

    # --- 1. Lexer Phase ---
    lexer.input(c_code)
    tokens = [str(tok) for tok in lexer]

    # --- 2. Parser Phase ---
    try:
        lexer.input(c_code)
        ast = parser.parse(c_code, lexer=lexer)
        if ast is None:
            return jsonify({'error': 'Syntax Error: Could not build AST.'})
    except Exception as e:
        return jsonify({'error': f'Parsing failed: {e}'})

    # --- 3. Code Generation Phase ---
    try:
        codegen = CodeGen()
        llvm_ir = codegen.generate_code(ast)
        with open('output/output.ll', 'w') as f:
            f.write(llvm_ir)
    except Exception as e:
        return jsonify({'error': f'Code generation failed: {e}'})

    # --- 4. Execution Phase (AOT Compilation) ---
    try:
        llc_path = 'C:/Program Files/LLVM/bin/llc.exe'
        clang_path = 'C:/Program Files/LLVM/bin/clang.exe'

        obj_file = 'output/output.o'
        exe_file = 'output/a.out'
        runtime_file = 'runtime/minic_runtime.c'

        subprocess.run([llc_path, '-filetype=obj', 'output/output.ll', '-o', obj_file], check=True, capture_output=True)
        subprocess.run([clang_path, obj_file, runtime_file, '-o', exe_file], check=True, capture_output=True)
        
        # ** FIX **: Use the absolute path to the executable.
        result = subprocess.run([os.path.abspath(exe_file)], capture_output=True, text=True, check=True)
        output = result.stdout
        
    except subprocess.CalledProcessError as e:
        error_message = "Execution failed.\n"
        error_message += f"Stderr: {e.stderr.decode() if e.stderr else 'N/A'}\n"
        error_message += f"Stdout: {e.stdout.decode() if e.stdout else 'N/A'}"
        return jsonify({'error': error_message})
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred during execution: {e}'})

    return jsonify({
        'tokens': '\n'.join(tokens),
        'ast': str(ast),
        'llvm_ir': llvm_ir,
        'output': output
    })