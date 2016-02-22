# Blog

## Version 0.1

Kleines Blogsystem mit folgenden Funktionen:
 * Login
 * Registration
 * Blog posting
 * Voting System
 * User Profiles

## Setup

### Voraussetzungen
Um das Blogsystem benutzen zu können benötigst du folgende Sachen:
 * Python 3
 * Flask für Python 3
 * MySQL Datenbank
 * MySQLdb für Python 3

### Vorbereitung
Ohne diese Schritte wird das Blogsystem nicht funktionieren:

#### MySQL
 1. Datenbank erstellen (Standart Name ist Blog, Name frei wählbar)
 2. Tables erstellen:
  1. `CREATE TABLE posts (title TEXT, published VARCHAR(80), author VARCHAR(50), content TEXT, link TEXT, likes INT, dislikes INT);`
  2. `CREATE TABLE users (name TEXT, email TEXT, rank TEXT, passwd VARCHAR(150), link TEXT, website TEXT, twLink TEXT, fbLink TEXT, githubLink TEXT, ytLink TEXT, skype TEXT);`
 3. Administrator erstellen:
  1. Mit Python das Passwort verschlüsseln:
   `>>> from werkzeug.security import generate_password_hash`
   `>>> generate_password_hash("*Wunschpasswort*")`
  2. `INSERT INTO users (name, email, rank, passwd) VALUES ("*Wunschname*, *E-Mail*, 'admin', *Generiertes Passwort*");`

#### Python
 1. Die Datei dbconnect (zu finden in dem Ordner scripts) und anpassen

## Zusatzinformationen
 * Benutzer Administrationsrechte geben:
  * `UPDATE users SET rank = "admin" WHERE name = "*Wunschname*";`
