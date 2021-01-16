import subprocess

engine = subprocess.Popen(
    'stockfish',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    bufsize=1,
)

line = engine.stdout.readline().strip()
print(line)
