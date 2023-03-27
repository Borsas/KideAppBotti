# Ropotti :D

Käytä omal vastuul :D

## Käyttö

1. Asenna uusin python
2. `python3 -m pip install -r requirements.txt`
3. Hae JWT kide.app sivuilta (ks. JWT haku)
4. Aja bottia `python3 main.py --id <tapahtuma_id>`
5. `python3 main.py --help` antaa jotain neuvoi
6. ???
7. Kovaa ajoa

## JWT Haku

1. Kirjaudu sisään
2. Avaa network tab selaimessa
3. Etsi joku request
4. Siellä on `Request Headers` kohdas `authorization` rivi, kopioi siitä kaikki paitsi `Bearer `
5. Esim. `Bearer eyJhbGciOiJo...` kopioit vaan `eyJhbGciOiJo...`
6. Nimeä .env.example -> .env ja pasteta token sinne
