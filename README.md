# AutoAPE-mlps

AutoAPE(Advanced Perceptron Engine) - MLPS(Machine Learning Processing Server)

## Build

### 빌드 시 필요한 Git 설정

```gitconfig
[http "https://*.seculayer.com:8443"]
    sslVerify = true
    sslCAInfo = /run/secrets/cert
    extraHeader = Authorization: Bearer <TOKEN>
```

위와 같은 내용을 파일(예: `../gitconfig`, `./gitconfig`)에 작성합니다. Container 빌드 시, 보안 파일로 넘길 것이기 때문에, `~/.gitconfig`에 추가하지 않습니다.

`<TOKEN>`은 Seculayer Bitbucket에서 Token을 발급받아서, `Authorization: Bearer` 부분은 그대로 두고, `<TOKEN>` 부분만 변경하면 됩니다.

### Docker build

`${SECRET_GITCONFIG}`에 위에서 설정한 파일 경로를, `${SSL_CERT}` 부분에는 *서비스모델팀 - 업무가이드*를 참고하여, Git용 인증서를 다운로드받고, 다운로드받은 인증서 경로를 설정하면 됩니다. **[`build-mlps.sh`](./build-mlps.sh) 파일에 관련 설정이 들어가야 합니다.**

```console
DOCKER_BUILDKIT=1 docker build --secret id=gitconfig,src="${SECRET_GITCONFIG}" --secret id=cert,src=${SSL_CERT} -t mlps .
```

```console
# 예제
docker build --secret id=gitconfig,src="../gitconfig" --secret id=cert,src=$HOME/seculayer/cert/slroot.crt -t mlps .
```

### `Pycmmn`, `dataconverter`, `apeflow` 업데이트 시 주의사항

위 3가지 패키지는 pypi를 통해서 받는 것이 아니라 `git` 소스를 통해서 받기 때문에, 버전 관리에 유의해야 합니다. 위

`poetry.lock` 파일 내용을 확인하여, git commit hash가 원하는 버전과 맞는지 확인해주세요.

버전이 맞지 않다면, `poetry update {PACKAGE}` 또는 `poetry update` 명령어로 `poetry.lock` 파일을 갱신해서 업데이트합니다.
