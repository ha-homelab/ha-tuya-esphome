# SWP1-PW2-V5 / TYWE3S : conversion série vérifiée

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Un exemplaire SWP1-PW2-V5 a été converti le 2026-10-18 après l'échec de Tuya-Convert classique avec l'identité PSK `02`. Une inspection filaire a identifié un ESP8266EX, un quartz de 26 MHz et 2 MiB de flash. Une sauvegarde d'usine vérifiée a fourni le plan GPIO avant l'écriture du micrologiciel final. Le propriétaire a ensuite confirmé le fonctionnement normal comme prise de bibliothèque.

Ces preuves concernent cet exemplaire, pas tous les produits au boîtier similaire. L'ancien interrupteur brûlé servant de référence matérielle était un autre appareil : son identité Home Assistant et sa configuration LocalTuya ont été conservées.

## Matériel confirmé

- Relais : **GPIO13, actif à l'état haut**, restauration `ALWAYS_OFF`.
- Bouton physique : **GPIO3 / RXD0, actif à l'état bas**, pull-up et anti-rebond de 30 ms.
- Voyant du relais : **GPIO14, actif à l'état bas**, suit l'état commandé du relais.
- Voyant de connexion : **GPIO0, actif à l'état bas**.
- Journalisation série : désactivée ; débrancher les fils UART du programmateur avant de tester le bouton, car son entrée partage RXD0.

Le JSON matériel de l'application d'usine indiquait ces affectations ; les observations ultérieures du bouton, du relais et des voyants les ont confirmées. Aucun balayage des sorties GPIO ni micrologiciel de diagnostic neutre n'a été nécessaire. Le profil ne configure aucune mesure électrique. Un voyant ou un état API ne constitue pas un retour des contacts du relais.

## Câblage basse tension

**Débrancher complètement l'appareil du secteur avant de l'ouvrir ou de connecter quoi que ce soit. Le laisser débranché pendant toute la programmation.** Utiliser une source régulée de 3,3 V et une logique UART vérifiée à 3,3 V. Un convertisseur de niveau adapte les signaux ; il ne fournit pas d'alimentation régulée à la cible.

![Câblage série fonctionnel : alimentation externe de 3,3 V, adaptateur UART 5 V, convertisseur de niveau et TYWE3S](images/swp1-serial-wiring.svg)

Le dessin représente les connexions électriques, **pas la position physique des pastilles**. Repérer les broches avec la [fiche Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), en vérifiant l'orientation du dessin par rapport à la carte. Ne pas déduire la fonction d'une pastille de test de sa position. La tension d'alimentation nominale documentée est de 3,3 V.

Pour l'adaptateur à logique 5 V utilisé ici :

1. **5V de l'adaptateur → référence HV** du convertisseur.
2. Alimentation externe régulée **3.3V → VCC du module et LV du convertisseur**.
3. Relier GND de l'adaptateur, GND du convertisseur, négatif de l'alimentation et GND du module à une masse commune.
4. **TX de l'adaptateur → HV1**, avec **LV1 → RXD0 du module** sur le canal correspondant.
5. **TXD0 du module → LV2**, avec **HV2 → RX de l'adaptateur** sur le canal correspondant.
6. Laisser la sortie 3V3 de l'adaptateur déconnectée. Ne pas mettre deux sorties d'alimentation en parallèle.

Choisir un convertisseur adapté au débit et au sens UART. Cette chaîne précise a fonctionné à 115200 bauds après correction du câblage ; cela ne valide pas toute carte HV/LV bon marché. Un véritable adaptateur UART 3,3 V peut se passer de convertisseur après vérification de son niveau de sortie.

L'adaptateur indiquait initialement 3,3 V à vide, mais la cible connectée ne recevait que **1,9 V**. Son signal TX atteignait aussi **5,1 V**. Ce sont deux problèmes distincts : une alimentation externe a corrigé l'alimentation, et le convertisseur a adapté les niveaux UART. Mesurer VCC sur le module en charge et les niveaux des signaux par rapport à la même masse. Voir les [conseils de connexion physique ESPHome](https://esphome.io/guides/physical_device_connection/).

## Mode téléchargement, sauvegarde et micrologiciel

Hors tension, maintenir **GPIO0 relié à GND**. Rétablir la basse tension, puis **relier brièvement RST à GND et relâcher RST**. Maintenir EN haut ; ne pas maintenir RST bas. GPIO0 peut rester à la masse pendant l'écriture, mais retirer ce pont avant un démarrage normal. Le message ROM lisible `boot mode:(1,0)` a confirmé le mode téléchargement dans ce cas. Voir la [documentation des modes de démarrage Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Un seul programme peut posséder le port série. Quitter Miniterm avant esptool. Le croisement correct de TX/RX a résolu le dernier échec de communication ; un voyant allumé ne prouvait pas une liaison série fonctionnelle.

Avant l'écriture, l'opérateur a lu **les 2,097,152 octets complets** de la flash d'usine et vérifié cette sauvegarde par rapport à l'appareil avec esptool. Conserver sauvegardes, journaux série bruts, images compilées et identifiants hors du Git public : un dump d'usine peut contenir des secrets de provisionnement. La [référence esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) décrit l'identification, `read-flash`, `verify-flash` et `write-flash`. Choisir la taille de lecture d'après la flash réellement détectée, pas d'après le nom du boîtier.

Compiler le [profil autonome](../examples/swp1-pw2-v5.yaml) dans un nouveau répertoire privé. Exécuter ces commandes depuis la racine du dépôt ; copier uniquement ce profil, ni la base générique ni un paquet XS-SSA01 :

```sh
SWP_REPO="$PWD"
SWP_BUILD_DIR="$HOME/.local/share/esphome/swp1-private"
umask 077
mkdir -p "$SWP_BUILD_DIR"
cp "$SWP_REPO/examples/swp1-pw2-v5.yaml" "$SWP_BUILD_DIR/"
python3.12 -m venv "$SWP_BUILD_DIR/.venv"
"$SWP_BUILD_DIR/.venv/bin/python" -m pip install 'esphome==2026.9.1'
"$SWP_BUILD_DIR/.venv/bin/python" "$SWP_REPO/scripts/create-secrets.py" \
  "$SWP_BUILD_DIR/secrets.yaml"
"$SWP_BUILD_DIR/.venv/bin/python" -m esphome compile \
  "$SWP_BUILD_DIR/swp1-pw2-v5.yaml"
```

L'assistant demande les identifiants Wi-Fi et génère des clés distinctes ; il refuse d'écraser les secrets existants. Ces commandes compilent sans flasher. Voir les [notes de provisionnement chiffré](security-profile.md) pour la gestion des identifiants. Cet exemplaire utilisait **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. L'image installée faisait **429,600 octets**, écrits à l'adresse `0x0` à 115200 bauds ; esptool a confirmé le hash écrit. Une nouvelle compilation peut avoir une autre taille : ce nombre est une observation, pas une exigence d'installation.

## Démarrage normal et validation

Couper l'alimentation, retirer GPIO0–GND et les deux fils de signal UART, puis rétablir uniquement les 3,3 V externes. L'API native chiffrée s'est connectée ; ON/OFF fonctionnait, et un redémarrage logiciel depuis ON remettait le relais sur OFF. Le propriétaire a confirmé deux pressions avec clics du relais et suivi du voyant.

Ensuite, tout câblage temporaire et l'alimentation externe ont été retirés, et le boîtier refermé avant l'installation normale. Le propriétaire a confirmé le fonctionnement sur la prise installée. **Aucun essai contrôlé de coupure/rétablissement du secteur depuis ON, ni mesure de tension des contacts ou de transitoires de démarrage n'a été réalisé.** Les clics sur établi seuls n'auraient pas prouvé la commutation d'une charge.

Home Assistant a reçu un relais et des diagnostics de connexion, signal, version et redémarrage. La fonction installée a été renommée dans HA sans reflasher : le hostname initial du micrologiciel reste valable. Le code privé complet a été sauvegardé dans le répertoire ESPHome de HA et dans ESPHome Dashboard. Le relais a été ajouté une seule fois à la section Living Room de la deuxième page du tableau de bord. Un futur déploiement doit préserver ces identités de registre ou les migrer explicitement.

## En cas d'échec

- **Aucune réponse série :** vérifier VCC en charge, masse commune, TX adaptateur → RX module, TX module → RX adaptateur et l'absence de terminal occupant le port.
- **Octets illisibles :** capturer un nouveau reset à 74880 bauds pour le journal ROM ; employer le débit esptool choisi pour le transfert réel.
- **Toujours en mode téléchargement :** retirer le pont GPIO0–masse et redémarrer.
- **Voyant d'état allumé pendant le reset :** GPIO0 pilote aussi ce voyant ; le strap de démarrage à la masse peut l'expliquer. Ne pas l'utiliser comme test de reset.
- **Bouton inopérant avec le programmateur connecté :** débrancher UART ; GPIO3 est partagé.
- **API opérationnelle mais pas la charge :** un état de relais déclaré ne diagnostique ni contacts, ni alimentation de bobine, ni câblage secteur. Ne pas sonder une carte exposée sous tension secteur.
