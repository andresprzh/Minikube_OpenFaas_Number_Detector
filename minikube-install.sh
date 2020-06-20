minikube config set driver virtualbox
minikube start
kubectl -n kube-system create sa tiller && kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
export PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
# export PASSWORD=42099d59d6d060d5934854561a433ee1b4cc25b8
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password="$PASSWORD"
helm upgrade openfaas --install openfaas/openfaas --namespace openfaas --set functionNamespace=openfaas-fn --set basic_auth=true
export OPENFAAS_URL="http://$(minikube ip):31112"
opfaas="export OPENFAAS_URL=${OPENFAAS_URL}"
sudo bash -c "echo $opfaas >> /home/${USER}/.bashrc"
docker pull jhonnyc2320/inletsjhonny
docker run -d -it -e UPSTREAM=http://$(minikube ip):31112 f6995a19aa99
echo "PASSWORD"
echo $PASSWORD