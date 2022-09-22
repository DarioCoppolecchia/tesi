# tesi

## Manuale utente

1. Inizialmente si devono creare i file .log, tramite i seguenti comandi:
    1. Spostarsi nella cartella `tesi`
    1. Creare le cartelle logs e tuesday con il comando `$ mkdir -p logs/tuesday`
    1. spostarsi nella cartella logs tramite il comando `$ cd logs` e poi nella giornata che si vuole analizzare (**per adesso si può analizzare solo tuesday**) con il comando `$ cd tuesday` che ti sposterà in tuesday
    1. avvia zeek su un file pcap e salva i log nella cartella attuale `$ /usr/local/zeek/bin/zeek -r ../pcap_files/*pcapfile*.pcap`, per esempio con il file log di tuesday: `$ /usr/local/zeek/bin/zeek -r ../../pcap_files/Tuesday-WorkingHours.pcap`
    1. dopo che lo script è stato eseguito, spostarsi nella cartella degli script per eseguire lo script python per la normalizzazione dei dati, tramite il seguente comando: `$ cd ../../scripts`
    1. a questo punto eseguire la normalizzazione dei file tramite il comando: `$ python3 ConnectionsClassifier/__main__.py`

1. A questo punto si è all'interno del programma, e si possono eseguire diversi comandi 
    1. inizialmente, se il file `conn_labeled.log` non è stato già creato, bisogna eseguire la prima voce inserendo `1`. Dopo averlo eseguito verrà generato il file conn_labeled.log e successivamente non sarà necessario rieseguirlo
    1. successivamente bisogna eseguire il comando `2` che legge le linee da conn.log e le normalizza.
    1. inseguito devono essere convertite con il comando `4` e memorizzate nella ram per essere utilizzate successivamente
    1. infine si può visualizzare il risultato dell'ultima operazione in un file json tramite il comando `5` e aprendo il file json presente nella stessa cartella del file log
    
1. In questo menù si possono anche effettuare altre operazioni:
    - Tramite il comando `3` si possono stampare su un file tsv le varie righe preprocessate (quindi senza le linee in più create da zeek)
    - Tramite il comando `6` si possono leggere le linee dal file tsv creato col comando `3`
    - Se viene modificato il file config.ini, lo si può ricaricare tramite il comando `7`
    - Tramite i comandi dal `9` al `11` si possono inserire manualmente le configurazioni anzichè leggerle dal file config.ini
    - tramite il comando `8` si può mostrare la configurazione attuale (che può essere caricata dal file config.ini o inserita manualmente)
    - infine con il comando `12` si può uscire dal programma
