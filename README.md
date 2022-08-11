# tesi

comandi utili:

- dalla cartella principale del progetto, eseguire il seguente comando per spostarsi nella cartella per i logs

    `$ cd logs`

- avvia zeek su un file pcap e salva i log nella cartella attuale

    `$ /usr/local/zeek/bin/zeek -r ../pcap_files/2020-10-12-Lokibot-infection-traffic.pcap`

- dopo che lo script è stato eseguito, spostarsi nella cartella degli script per eseguire lo script python per la normalizzazione dei dati, tramite il seguente comando:

    `$ cd ../scripts`

- a questo punto eseguire la normalizzazione dei file tramite il comando:

    `$ python3 PacketsHandler/__main__.py`
