"""Constants for Marketplace Refresh."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "marketplace_refresh"
# Same as manifest.json and the card: the card URL carries it, so that browsers load a new release.
VERSION: Final = "2.5.0"
MARKETPLACE_DOMAIN: Final = "marketplace"

CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_BACKUP_BEFORE_INSTALL: Final = "backup_before_install"
# Hours between two automatic checks; 0 turns the automatic check off.
DEFAULT_SCAN_INTERVAL: Final = 24
MAX_SCAN_INTERVAL: Final = 168

# Repositories refreshed at the same time: the Marketplace itself fetches them one by one,
# a few in parallel keeps a large install quick without hammering the GitHub API.
PARALLEL_REFRESHES: Final = 4

SERVICE_CHECK_UPDATES: Final = "check_updates"
SERVICE_CHECK_REPOSITORY: Final = "check_repository"
SERVICE_INSTALL_UPDATES: Final = "install_updates"

# Fired when a full check finds updates that the previous one didn't.
EVENT_UPDATES_FOUND: Final = f"{DOMAIN}_updates_found"

STATE_IDLE: Final = "idle"
STATE_RUNNING: Final = "running"
STATE_ERROR: Final = "error"

# The card bundled with the integration, served by Home Assistant and added to the dashboard resources.
CARD_URL: Final = f"/{DOMAIN}/marketplace-refresh-card.js"

# Name of the backup in the list of updates that could not be installed ("<name>: <error>"), in Home Assistant's
# language: the backup failed, so nothing was installed.
BACKUP_FAILED: Final = {
    "en": "Backup before installing",
    "fr": "Sauvegarde avant l'installation",
    "de": "Backup vor der Installation",
    "es": "Copia de seguridad antes de instalar",
    "sr": "Резервна копија пре инсталације",
    "sr-Latn": "Rezervna kopija pre instalacije",
    "it": "Backup prima dell'installazione",
    "nl": "Back-up vóór de installatie",
    "pt": "Cópia de segurança antes da instalação",
    "pt-BR": "Backup antes da instalação",
    "pl": "Kopia zapasowa przed instalacją",
    "ro": "Copie de rezervă înainte de instalare",
    "da": "Backup før installation",
    "sv": "Säkerhetskopia före installation",
    "bg": "Резервно копие преди инсталиране",
    "ru": "Резервная копия перед установкой",
    "uk": "Резервна копія перед встановленням",
    "hu": "Biztonsági mentés telepítés előtt",
    "sk": "Záloha pred inštaláciou",
    "cs": "Záloha před instalací",
    "sl": "Varnostna kopija pred namestitvijo",
    "lv": "Rezerves kopija pirms instalēšanas",
    "el": "Αντίγραφο ασφαλείας πριν από την εγκατάσταση",
}
