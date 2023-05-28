import re
from pathlib import Path

for p in range(1, 4):
    with open(f'Teste{p}.txt', 'a') as teste:
        teste.write("Estou aqui\n")

k = Path('.').glob('*.txt')
for p in list(k):
    o = re.sub("(?<=\').*?(?=\')", '', str(p))
    print(o)
    Path(p).unlink()
