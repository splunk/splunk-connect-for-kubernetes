#!/usr/bin/env bash
set -e
wget https://github.com/tcnksm/ghr/releases/download/v0.12.0/ghr_v0.12.0_linux_amd64.tar.gz
tar -xzvf ghr_v0.12.0_linux_amd64.tar.gz
sudo chmod +x ghr_v0.12.0_linux_amd64
sudo mv ghr_v0.12.0_linux_amd64/ghr /usr/local/bin/ghr

VERSION=`cat VERSION`
echo "Pushing SCK release to github releases...${VERSION}"
ghr -t ${GITHUB_TOKEN} -u ${CIRCLE_PROJECT_USERNAME} -r ${CIRCLE_PROJECT_REPONAME} -c ${CIRCLE_SHA1} -n "${RELEASE_TITLE}" -b "${RELEASE_BODY}" -draft ${VERSION} ./helm-artifacts-release/
