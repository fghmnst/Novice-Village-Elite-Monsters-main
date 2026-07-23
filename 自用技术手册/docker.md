# docker

以Ubuntu24.04且部署在大陆以外的服务器为例，介绍最新最潮的下载安装
[Install Docker Engine on Ubuntu | Docker Docs](https://docs.docker.com/engine/install/ubuntu/)

> 国内服务器折腾起来十分麻烦，但依旧有解，这里挖一个坑
> **下载：**

```shell
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)

# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

如果网络环境正常的话，理论上这一路下来可以十分爽快地复制粘贴，接下来设置sudo组，免得搞个docker回回得输入sudo

```shell
# 1. 创建 docker 用户组（如果已存在会提示，无影响）
sudo groupadd docker

# 2. 将当前用户加入 docker 用户组
sudo usermod -aG docker $USER

# 3. 刷新用户组权限（或直接退出终端重新登录）
newgrp docker
```

ojbk。接下来是docker常见指令：
**镜像操作：**

1. 检索：`docker search`
2. 下载：`docker pull`
3. 列表：`docker images`
4. 删除镜像：`docker rmi`
   **容器操作：**
5. 删除容器：`docker rm`
6. 运行：`docker run`
7. 查看：`docker ps`
8. 停止：`docker start`
9. 重启：`docker restart`
10. 状态：`docker stats
11. 日志：`docker logs`
12. 进入：`docker exec`
    加上`--help`可查看帮助
