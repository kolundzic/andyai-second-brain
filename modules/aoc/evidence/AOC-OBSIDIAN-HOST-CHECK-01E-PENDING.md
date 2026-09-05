# AOC–OBSIDIAN–HOST–CHECK–01E — PENDING

## Status

**READY FOR HOST RUN**

Test skripta i testovi su spremni u repou.

01E još nije označen kao PASS zato što prava provera mora da se pokrene na računaru na kome stvarno radi Obsidian.

## Komande

Prvo prikaži verziju Obsidiana i poznate vaultove:

```bash
python3 scripts/host_check.py --list
```

Zatim pokreni proveru nad izabranim vaultom:

```bash
python3 scripts/host_check.py --vault "VAULT NAME"
```

## PASS uslov

- Obsidian CLI radi
- vault je pronađen
- četiri AOC beleške su pročitane kroz read-only adapter
- KORMILO rezultat je tačan
- `authority_state = HUMAN_REQUIRED`
- `execution_allowed = false`

Kada se ovo izvrši na Andyjevom MacBooku ili HP/Omarchy računaru, rezultat se upisuje u novi evidence fajl i 01E se tada zaključava kao PASS ili FAIL.
