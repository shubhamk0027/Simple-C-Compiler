echo "........................................"
echo "...........Lexical Analyzer............."
echo "........................................"
python3 LexicalAnalyzer.py 
cat OLexicalAnalyzer.txt

echo "........................................"
echo ".............Syntax Analyzer............"
echo "........................................"
python3 SyntaxAnalyzer.py 
cat OSyntaxAnalyzer.txt

echo "........................................"
echo ".............Code Generator............."
echo "........................................"
python3 CodeGenerator.py
cat OCodeGenerator.txt

echo "........................................"
echo "......Virtual Machine Interpreter......."
echo "........................................"
python3 VMInterpreter.py 
cat output.txt