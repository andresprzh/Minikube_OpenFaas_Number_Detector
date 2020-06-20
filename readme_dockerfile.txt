A continuacion se describe el proceso de creacion del inlet.

En primera medida se utilizo Digital ocean y se creo el token necesario para entrar
este se encuentra en el dockerfile.


Con la siguiente instruccion se descarga e installa el inlet.

+++++++++++++++++++++++++++++++++++++++++++++++++

curl -sLSf https://inletsctl.inlets.dev | sudo sh

inletsctl download

+++++++++++++++++++++++++++++++++++++++++++++++++

Con las siguientes instrucciones se crea el servidor de salida
donde se especifica el digital ocean, region y el token que se
anteriormente.

+++++++++++++++++++++++++++++++++++++++++++++++++

>> inletsctl create \
  --provider digitalocean \
  --region lon1 \
  --access-token-file $HOME/inlets-cloud-api

+++++++++++++++++++++++++++++++++++++++++++++++++

Una vez creado el servidor de salida tendriamos que ver la siguiente salida
para confirmar que todo quedo listo y se vera la ip del servidor y el token


>> IP: 192.168.0.11:80
Auth-token: gZM13NsvmcahE7agc3j4jJQpQCPO9hlQM8HapkNnJagjUby1UDpKFd8sObVC0fhl

Para crear el inlet hacemos lo siguiente

>> export UPSTREAM=http://127.0.0.1:8080
   inlets client --remote "ws://167.71.142.34:8080" \
 --token "gZM13NsvmcahE7agc3j4jJQpQCPO9hlQM8HapkNnJagjUby1UDpKFd8sObVC0fhl" \
 --upstream $UPSTREAM

UPSTREAM es una variable donde se guarda la ip del servidor loca o anfitrion.

Nota: Para correr el contenedor se utiliza el siguiente comando:

docker run -d -id UPSTREAM=ip_local imagen_id






