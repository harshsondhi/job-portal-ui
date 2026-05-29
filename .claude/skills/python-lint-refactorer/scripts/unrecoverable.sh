cat << 'EOF' > /tmp/test_unrecoverable.py
def break_loop():
    # Indentation error mixed with syntax error
     if True
    print("Missing colon and broken indent")

# Undefined variables inside a broken loop
for i in range(10):
    x = undefined_variable_1 + undefined_variable_2

# Duplicate argument names (SyntaxError / F831)
def duplicate_args(arg1, arg1):
    pass
EOF
