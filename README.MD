# Trabajo Final sistemas distribuidos
Ejemplo de uso de kubernets con openfaas de función que detecta el numero en imagenes 8x8 usando keras y TensorFlow
Código python en [**number-detector**](number-detector)

Se uso inlets para desplegar la función en la dirección http://165.22.127.169/ui/
Logearse con la siguiente instrucción:

```
echo -n 9b4fa20ae72fc1fd98e4decad055d8ef7d15c3a8 | faas-cli login -g 'http://165.22.127.169:80' -u admin --password-stdin
```

En la carpeta [**example-images**](example-images) de encuentran algunos ejemplo de imágenes para probar la función.
se ejecuta con el código, de tal forma que se envía la imagen decodificada en base 64

```
echo "`base64 example-images/4.png`" | faas-cli invoke number-detector
```

[**Ejemplo de ejecucion**](https://asciinema.org/a/XFdHdspKVjjAiMFMdFWCeoLBx)

---
## Prerrequisitos

* Instalar Minikube

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && \
chmod +x minikube && \
sudo cp minikube /usr/local/bin && rm minikube
```

* Instalar faas-cli

```
curl -sL cli.openfaas.com | sudo sh
```

* Instalar helm

```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

---
## Crear Cluster de kubernets usando minikube

* [**ENLACE A VÍDEO EN ASCIINEMA**](https://asciinema.org/a/as4wKH16BBx4yduPeV6uasI7K)

### Iniciar cluster con kubernets

```
minikube start
```

### Crear service account para triller 
```
kubectl -n kube-system create sa tiller && kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
```

### Crear namespaces para openfaas
```
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
```

### Añadir openfaas al repositorio de helm

```
helm repo add openfaas https://openfaas.github.io/faas-netes/
```

### Actualiza charts de helm
```
helm repo update
```

### Genera contraseña valida para cliente openfaas,

```
export PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
```
**Recordar consultar y guardar la contraseña**

### Crea usuario para publicar funciones en el Kluster usando la contraseña creada
```
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password="$PASSWORD"
```

### Instalar openfaas usando chart

```
helm upgrade openfaas --install openfaas/openfaas --namespace openfaas --set functionNamespace=openfaas-fn --set basic_auth=true
```

### Asigna url a openfaas

```
export OPENFAAS_URL="http://$(minikube ip):31112"
```

### Opcionalmente se puede guardar la url en las variables de ambiente

```
opfaas="export OPENFAAS_URL=${OPENFAAS_URL}" && \
echo $opfaas >> /home/${USER}/.bashrc
```

### Logearse usando el usuario admin creado y la contraseña

```
echo -n $PASSWORD | faas-cli login -u admin --password-stdin
```

### Valida la instalación

```
kubectl get pods -n openfaas
faas-cli list
```

---
## Crea funcion 

### Usar debian 3
Permite usar librerías compiladas como numpy y TensorFlow
```
faas-cli template pull https://github.com/openfaas-incubator/python3-debian
faas-cli new numpy-function --lang python3-debian
```

### Construye, publica y despliega funcion
```
for i in build push deploy ; do
faas-cli ${i} -f ./number-detector.yml
done
```
---
## Ejecutar funcion

```
echo "`base64 example-images/4.png`" | faas-cli invoke number-detector
```
