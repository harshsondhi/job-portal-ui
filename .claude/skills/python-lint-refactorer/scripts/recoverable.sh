cat << 'EOF' > /tmp/test_recoverable.py
import os, sys # Multiple imports on one line (E401)
import math # Unused import (F401)

def messy_function(x,y): # Missing whitespace around arguments (E231)
    print("Test")
    return x+y # Missing whitespace around operator (E226)
EOF