# AOC–KORMILO–LIVE–VAULT–01D — PROOF

## Test

Pokrenuto lokalno:

```bash
python3 -m unittest -v tests/test_build_kormilo.py
```

## Rezultat

**6/6 tests PASS**

Provereno je:

1. Prepoznat je pravi projekat i repo.
2. Ljudska odluka ostaje obavezna.
3. Dobijamo tačno tri sledeća koraka.
4. Svaki korišćeni fajl ima izvor i SHA-256 otisak.
5. Stara/opasna beleška nije korišćena.
6. Ako obavezna beleška nedostaje, proces se prekida umesto da nagađa.

## Zaključak

AOC može da sastavi KORMILO pregled iz malog Obsidian-kompatibilnog vaulta bez menjanja beleški i bez dobijanja prava na izvršavanje komandi.

Host provera na stvarnom Mac/HP Obsidian vaultu ostaje sledeći korak.
