# Symmetric Encryption Flask App

## Installatie

```bash
# install flask cryptography
pip install flask cryptography

# start the applicatie
python app.py
```

Ga vervolgens naar http://127.0.0.1:5000 in je browser.



## Over het project
Dit project is gemaakt voor de encryptie-opdracht van week 5.  
De bedoeling was om een applicatie te bouwen waarmee tekst encrypted en decrypted kan worden via een webapp.  
De webapp is gemaakt met Python (Flask) en gebruikt de symmetrische encryptie method AES-256-GCM.  

De focus lag op:
- symmetrische encryptie,  
- het veilig omgaan met sleutels,  
- en het toepassen van cryptografische principes zoals dat van Kerckhoffs.



## Hoe werkt de applicatie
Wanneer je tekst versleutelt, gebeurt er onder de motorkap het volgende:

1. Het ingevoerde wachtwoord wordt omgezet in een 256-bit sleutel via PBKDF2-HMAC-SHA256 (met een random salt en 600.000 iteraties).
2. Die sleutel wordt vervolgens gebruikt om de tekst te versleutelen met AES-256-GCM, een moderne en veilige encryptiemethode.
3. Het resultaat wordt opgeslagen in een JSON-pakket met o.a.:
- het gebruikte algoritme,
- de KDF (key derivation function) + parameters,
- de random salt,
- de nonce,
- en de ciphertext zelf.

Bij het ontsleutelen gebeurt exact het omgekeerde.
Als het wachtwoord onjuist is of het pakket is aangepast, mislukt de decryptie automatisch door de integriteitscontrole van GCM.


## Voorbeeld JSON-pakket
```
{
  "alg": "AES-256-GCM",
  "kdf": "PBKDF2-HMAC-SHA256",
  "params": {
    "iterations": 600000,
    "salt": "M4C1KthQoEjVY+RmNg=="
  },
  "nonce": "2EwZa6z3Lr8s8kTw",
  "ciphertext": "Hh93f6wPKAqjPvE4..."
}
```

## Gebruikte encryptiemethode

### Algoritme
De applicatie gebruikt **AES-256 in GCM-mode (Galois/Counter Mode)** via de Python-library [`cryptography`](https://cryptography.io).  
Intern wordt gebruikgemaakt van:

- **AES-256-GCM** voor symmetrische encryptie  
- **PBKDF2-HMAC-SHA256** voor sleutelafleiding  
- **Nonce en salt** om elke encryptie uniek te maken  

### Waarom deze keuze?
- **Bewezen veilig:** AES-GCM is een moderne standaard die ook integriteitscontrole biedt.  
- **Simpel te gebruiken:** de `cryptography`-library regelt veilige nonce-generatie en authenticatie automatisch.  
- **Goede praktijk:** het sluit aan bij hedendaagse richtlijnen voor symmetrische encryptie en wachtwoord-gebaseerde sleutelafleiding.



## Sleutelbeheer uitgelegd

De app slaat geen sleutels op.
Elke keer dat de gebruiker een wachtwoord invoert, wordt daar tijdelijk een sleutel van afgeleid met PBKDF2.
- De salt maakt elke sleutel uniek, zelfs bij hetzelfde wachtwoord.
- De nonce zorgt dat elke encryptie nieuw en onvoorspelbaar is.
- De ciphertext bevat de versleutelde tekst + authenticatietag.
- Het wachtwoord blijft geheim en wordt nergens opgeslagen of verzonden.

Zo blijft het systeem veilig, zolang de gebruiker een sterk wachtwoord kiest.



## Kerckhoffs’s principe

Het ontwerp volgt Kerckhoffs’s principe:
het systeem blijft veilig, zelfs als alle details van de implementatie publiek bekend zijn.
Alle parameters (zoals algoritme, salt, nonce en iteraties) zitten openlijk in het JSON-pakket.
De enige geheimhouding die telt, is die van het wachtwoord zelf.
Zonder dat wachtwoord kan niemand de data terughalen, ook niet met volledige toegang tot het pakket.




