# AOC–OBSIDIAN–HOST–CHECK–01E

## Cilj

Proveriti da AOC radi sa Obsidianom koji stvarno radi na Andyjevom računaru.

Do sada smo proveravali nad Obsidian-kompatibilnim folderom. U 01E koristimo pravi Obsidian CLI i kroz njega čitamo iste beleške.

## Šta test radi

1. Proveri da li je `obsidian` komanda dostupna.
2. Prikaže poznate vaultove.
3. Andy izabere vault.
4. AOC kroz read-only adapter pročita samo:
   - `Projects/AOC/PROJECT.md`
   - `Projects/AOC/STATUS.md`
   - `Projects/AOC/OPEN.md`
   - `Projects/AOC/DECISIONS.md`
5. Od toga sastavi KORMILO pregled.

## Šta test NE radi

- ne menja beleške
- ne briše fajlove
- ne pokreće shell komande iz beleški
- ne daje AI-ju pravo da izvršava akcije

## PASS uslov

01E je PASS tek kada na pravom Mac/HP računaru dobijemo:

- Obsidian verziju
- uspešno pročitan izabrani vault
- tačan projekat i repo
- tačno 3 sledeća koraka
- `authority_state = HUMAN_REQUIRED`
- `execution_allowed = false`
- izvor za svaku korišćenu belešku

## Trenutni status

**READY FOR HOST RUN — nije još PASS.**

Sledeća praktična provera je na Andyjevom MacBooku ili HP/Omarchy računaru.
