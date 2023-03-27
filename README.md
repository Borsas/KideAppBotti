# Ropotti :D

Käytä omal vastuul :D

## Käyttö

1. Asenna uusin python
2. `python3 -m pip install -r requirements.txt`
3. Hae JWT kide.app sivuilta
   a. Kirjaudu sisään
   b. Avaa network tab selaimessa
   c. Etsi joku request
   d. Siellä on `Request Headers` kohdas `authorization` rivi, kopioi siitä kaikki paitsi `Bearer `
   e. Esim. `Bearer eyJhbGciOiJo...` kopioit vaan `eyJhbGciOiJo...`
   f. Nimeä .env.example -> .env ja pasteta token sinne
4. Aja bottia `python3 main.py --id <tapahtuma_id>`
5. `python3 main.py --help` antaa jotain neuvoi
6. ???
7. Kovaa ajoa
