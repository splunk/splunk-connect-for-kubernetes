#!/bin/bash
set -e
TAG="PERF-TEST"
DATA_GEN_IMAGE="luckyj5/k8s-datagen"

function print_msg ()
{
    datetime=`date "+%Y-%m-%d %H:%M:%S"`
    echo "$datetime: $1"
}


function setup_kubeclient ()
{

    echo "Setup kube client..."
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
    sudo apt-get -y install gnupg
    sudo mkdir ~/.kube
    echo $GPG_KEY | gpg --output config --passphrase-fd 0 --decrypt --batch .circleci/performance/kubeconfig_perf.gpg
    sudo mv config ~/.kube/config

}

function deploy_sck ()
{
    print_msg "Deploying SCK"
    setup_kubeclient
    print_msg "Installing the SCK build artifacts on the kubernetes cluster"
    helm install --name=perf-test -f .circleci/performance/perf_test_sck_values.yml helm-artifacts/splunk-connect-for-kubernetes*.tgz
}

function clean_sck ()
{
    print_msg "Cleaning SCK"
    if [ "`helm ls`" == "" ]; then
       print_msg "Nothing to clean, ready for deployment"
    else
       helm delete --purge $(helm ls --short)
    fi
}

function deploy_datagen ()
{
    datagen_params=("$@")
    deployment_name=${datagen_params[0]}
    namespace=${datagen_params[1]}
    number_of_replicas=${datagen_params[2]}
    msg_count=${datagen_params[3]}
    msg_size=${datagen_params[4]}
    eps=${datagen_params[5]}
    for ((i = 1; i <= ${number_of_replicas}; i++));
    do
        deployment_name_replica=`echo ${deployment_name}-${i}`
        print_msg "Deploying K8s data gen ${deployment_name_replica} viz. ${i} of ${number_of_replicas}"
        kubectl run ${deployment_name_replica} -n ${namespace} --image=${DATA_GEN_IMAGE} --replicas=1 --env="MSG_COUNT=${msg_count}" --env="MSG_SIZE=${msg_size}" --env="EPS=${eps}" --restart=Never
    done
}

function clean_datagen ()
{
    datagen_params=("$@")
    deployment_name=${datagen_params[0]}
    namespace=${datagen_params[1]}
    number_of_replicas=${datagen_params[2]}
    for ((i = 1; i <= ${number_of_replicas}; i++));
    do
        deployment_name_replica=`echo ${deployment_name}-${i}`
        print_msg "Cleaning K8s data gen ${deployment_name_replica} viz. ${i} of ${number_of_replicas}"
        kubectl delete pod ${deployment_name_replica} -n ${namespace}
    done
}

function usage ()
{
cat << EOF
Usage: $0 options
    OPTIONS:
    --help    # Show this message
    --deploy   # Deploy SCK
    --clean    # Clean SCK
    --deploy_data_gen "DEPLOYMENT_NAME NAMESPACE NUMBER_OF_REPLICAS MSG_COUNT MSG_SIZE EPS" #Deploy K8s datagen
    --clean_data_gen "DEPLOYMENT_NAME NAMESPACE NUMBER_OF_REPLICAS" #Cleanup K8s datagen
EOF
exit 1
}

for arg in "$@"; do
    shift
    case "$arg" in
        "--help")
            set -- "$@" "-h"
            ;;
        "--deploy")
            set -- "$@" "-d"
            ;;
        "--clean")
            set -- "$@" "-c"
            ;;
        "--deploy_data_gen")
            set -- "$@" "-e"
            ;;
        "--clean_data_gen")
            set -- "$@" "-f"
            ;;
        *)
            set -- "$@" "$arg"
    esac
done

cmd=
datagen_params=

while getopts "hdcf:e:" OPTION
do
    case $OPTION in
        h)
            usage
            ;;
        d)
            cmd="deploy"
            ;;
        c)
            cmd="clean"
            ;;
        e)
            cmd="deploy_data_gen"
            datagen_params=($OPTARG)
            ;;
        f)
            cmd="clean_data_gen"
            datagen_params=($OPTARG)
            ;;
        *)
            usage
            ;;
    esac
done

if [[ "$cmd" == "deploy" ]]; then
    deploy_sck
elif [[ "$cmd" == "clean" ]]; then
    clean_sck
elif [[ "$cmd" == "deploy_data_gen" ]]; then
    deploy_datagen "${datagen_params[@]}"
elif [[ "$cmd" == "clean_data_gen" ]]; then
    clean_datagen "${datagen_params[@]}"
else
    usage
fi