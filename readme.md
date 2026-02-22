# Retro uhkapelialusta (Raspberry Pi 3)

Retro-tyylinen uhkapelialusta, joka on tarkoitettu ajettavaksi Raspberry Pi 3 -tietokoneella. Pelaaminen alkaa credittejä lisäämällä; crediteillä voi pelata Pokeria tai hedelmäpeliä (slot).

## Toiminta

1. **Credittejä** – Valikosta "Lisää credittejä" lisää pelirahaa (oletus 10 kpl).
2. **Poker** – Video Poker (Jacks or Better): jaetaan 5 korttia, pidä haluamasi kortit, vaihda loput ja voita käden mukaan.
3. **Hedelmäpeli (Slot)** – Kolme rullaa, paina PELAA. Kolme samaa symbolia = voitto.

## Asennus

```bash
# Python 3.7+ (esim. Raspberry Pi OS)
pip install -r requirements.txt

# Tai virtuaaliympäristössä:
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Käynnistys

```bash
python main.py
# tai: .venv/bin/python main.py
```

- **ESC** = takaisin valikkoon / lopeta.
- Hiiri: valinnat ja napot.

## Raspberry Pi 3 -kioski

- `config.py`: voit asettaa `FULLSCREEN = True` koko näytölle.
- Kehitystä varten kannattaa asettaa `FULLSCREEN = False` ja ajaa tavallisessa ikkunassa.
- Pi:llä voi käyttää suoraan framebufferia (ei X): aseta ympäristömuuttujat ennen käynnistystä, ks. `ui.init_display()`.

## Projektirakenne

```
multi-slot-machine/
├── main.py       # Pääohjelma, credit-näyttö ja valikko
├── config.py     # Näyttö, värit, panokset
├── ui.py         # Näyttö, fontit, napot
├── games/
│   ├── slot.py   # Hedelmäpeli
│   └── poker.py  # Video Poker
├── requirements.txt
└── readme.md
```

## Teknologia

- **Pygame** – grafiikka ja syöte
- Python 3
