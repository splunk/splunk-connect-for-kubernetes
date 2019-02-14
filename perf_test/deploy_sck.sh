#!/bin/bash
set -e
TAG="PERF-TEST"
DATA_GEN_IMAGE="luckyj5/k8s-datagen"

function print_msg ()
{
    datetime=`date "+%Y-%m-%d %H:%M:%S"`
    echo "$datetime: $1"
}

function replace_generic_version ()
{
    file="$1"
    _line=`awk '/version:/{print NR;exit}' $file`
    replacement="version: $TAG"
    # Escape backslash, forward slash and ampersand for use as a sed replacement.
    replacement_escaped=$( echo "$replacement" | sed -e 's/[\/&]/\\&/g' )
    sed -i '' "${_line}s/.*/$replacement_escaped/" "$file"
}

function prepare_sck_charts ()
{
    print_msg "Preparing SCK charts for deployment"
    repos_array=( "../helm-chart/splunk-connect-for-kubernetes" "../helm-chart/splunk-kubernetes-logging"
                  "../helm-chart/splunk-kubernetes-metrics" "../helm-chart/splunk-kubernetes-objects" )
    sub_repos_array=( "../helm-chart/splunk-kubernetes-logging"
                  "../helm-chart/splunk-kubernetes-metrics" "../helm-chart/splunk-kubernetes-objects" )

    for repo in "${repos_array[@]}"
    do
      filename="${repo}/Chart.yaml"
      replace_generic_version $filename
    done

    mkdir ../helm-artifacts
    mkdir ../helm-chart/splunk-connect-for-kubernetes/charts

    for sub_repo in "${sub_repos_array[@]}"
    do
      cp -rp $sub_repo ../helm-chart/splunk-connect-for-kubernetes/charts
    done

    for repo in "${repos_array[@]}"
    do
      helm package -d ../helm-artifacts $repo
    done
}

function clean_artifacts ()
{
    print_msg "Cleaning all temporary build artifacts"
    rm -r ../helm-artifacts
    rm -r ../helm-chart/splunk-connect-for-kubernetes/charts
}

function deploy_sck ()
{
    print_msg "Deploying SCK"
    prepare_sck_charts
    print_msg "Installing the SCK build artifacts on the kubernetes cluster"
    helm install --name=perf-test -f perf_test_sck_values.yml ../helm-artifacts/splunk-connect-for-kubernetes*.tgz
    clean_artifacts
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
    print_msg "Deploying K8s data gen"
    datagen_params=("$@")
    echo "run Number of arguments: ${#datagen_params[@]}"
    for val in "${datagen_params[@]}"; do
        echo " - $val"
    done
    deployment_name=${datagen_params[0]}
    namespace=${datagen_params[1]}
    number_of_replicas=${datagen_params[2]}
    msg_count=${datagen_params[3]}
    msg_size=${datagen_params[4]}
    eps=${datagen_params[5]}
    kubectl run ${deployment_name} -n ${namespace} --image=${DATA_GEN_IMAGE} --replicas=${number_of_replicas} --env="MSG_COUNT=${msg_count}" --env="MSG_SIZE=${msg_size}" --env="EPS=${eps}"
}

function clean_datagen ()
{
    print_msg "Cleaning up K8s data gen"
    datagen_params=("$@")
    deployment_name=${datagen_params[0]}
    namespace=${datagen_params[1]}
    kubectl delete deployment ${deployment_name} -n ${namespace}
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
    --clean_data_gen "DEPLOYMENT_NAME NAMESPACE" #Cleanup K8s datagen
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