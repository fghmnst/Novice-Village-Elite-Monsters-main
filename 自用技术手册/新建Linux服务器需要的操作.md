# 新建Linux服务器需要的操作

[详解如何 SSH 远程登录自己的 Linux 服务器 - 雨月空间站](https://mintimate.cn/2021/12/03/connectToLinux/#%E5%86%99-SSH-Config)


**本文有大量删减，详情见原文**

0. 更新系统软件包（sudo apt upgrade，Ubuntu)
1. 配置ssh
2. 创建普通用户
3. 关闭密码登录
4. 下载btop gdu 以及随便一个fetch（我的个人偏好）
5. \*文件传输
   **注：本文中的mint需要改为自己的用户名，毕竟这是我直接复制粘贴过来的。**

# 1. 配置ssh

---

首先确保电脑内已经安装了ssh（一般默认装）

```shell
ssh -V
```

## 密码登陆（第一次）

密码登录最直观，格式是：

```shell
 ssh 用户名@服务器IP
```

比如服务器 IP 是 `192.168.3.241`，登录用户是 `root`：

```shell
ssh root@192.168.3.241
```

如果服务器 SSH 端口不是默认的 `22`，比如改成了 `2222`：

```shell
ssh -p 2222 root@192.168.3.241
```

注意：`-p` 是小写，表示 port。

## 密钥登陆

### 生成密钥

原文作者推荐Ed25519密钥：

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

如果不支持Ed25519可退回RSA密钥：

```shell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

生成过程中会询问的问题：

```text
Enter file in which to save the key  //密钥保存位置。默认是 `~/.ssh/id_ed25519`，直接回车即可
Enter passphrase //私钥保护密码。个人电脑建议设置，自动化脚本可以留空
Enter same passphrase again//再输入一次私钥保护密码
```

生成后一般会有两个文件：

```text
~/.ssh/id_ed25519  
~/.ssh/id_ed25519.pub
```

其中：

- `id_ed25519` 是私钥，不能泄露。
- `id_ed25519.pub` 是公钥，可以放到服务器。

查看公钥内容：

```shell
cat ~/.ssh/id_ed25519.pub
```

公钥通常长这样：

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

你要复制的是整行，从 `ssh-ed25519` 开始，到最后的备注结束。

**接下来是正式登陆（有删减，详情见原文）**

### 方法一：使用 ssh-copy-id

如果服务器当前还能用密码登录，最简单的方法是 `ssh-copy-id`：

```shell
ssh-copy-id 用户名@服务器IP
```

比如：

```shell
ssh-copy-id root@192.168.3.241
```

如果 SSH 端口不是 22：

```shell
ssh-copy-id -p 2222 root@192.168.3.241
```

如果你要指定某个公钥文件：

```shell
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@192.168.3.241
```

它会自动把你的公钥追加到服务器对应用户的：

```shell
~/.ssh/authorized_keys
```

然后测试登录：

```shell
ssh root@192.168.3.241
```

如果不再要求输入服务器用户密码，就说明密钥登录成功了。

**Windows 自带 OpenSSH 有时没有 `ssh-copy-id`，可以用下面的手动方法。**

### 方法二： 手动写入 authorized_keys

先用密码登录服务器：

```shell
ssh root@192.168.3.241
```

在服务器上创建 `.ssh` 目录，并设置权限：

```shell
mkdir -p ~/.ssh  
chmod 700 ~/.ssh
```

编辑 `authorized_keys`：

```shell
nano ~/.ssh/authorized_keys
```

把你本地 `id_ed25519.pub` 的整行公钥粘贴进去，一行一个公钥。

保存后设置权限：

```shell
chmod 600 ~/.ssh/authorized_keys
```

如果你是用 root 帮普通用户配置，还要确认文件属于目标用户：

```shell
sudo chown -R 用户名:用户名 /home/用户名/.ssh
```

比如用户叫 `demo`：

```shell
sudo chown -R demo:demo /home/demo/.ssh
```

然后在本地测试：

```shell
ssh demo@服务器IP
```

## 指定私钥登陆

如果你使用的不是默认私钥名，就需要用 `-i` 指定私钥：

```shell
ssh -i ~/.ssh/my_server_key root@192.168.3.241
```

如果端口也不是默认 22：

```shell
ssh -i ~/.ssh/my_server_key -p 2222 root@192.168.3.241
```

私钥权限太宽时，OpenSSH 可能拒绝使用它。macOS 和 Linux 可以这样修复：

```shell
chmod 600 ~/.ssh/my_server_key
```

## 写 SSH Config

当服务器多了以后，每次都输入：

```shell
ssh -i ~/.ssh/my_server_key -p 2222 root@192.168.3.241
```

确实很烦。可以把配置写到本机的：

```shell
~/.ssh/config
```

**注：我记得这里在实操的过程中遇到了自己的电脑的ssh目录下没有config这个文件，这种情况就需要自己手动创建一个**

ssh config 示例：

```shell
Host myserver  
	HostName 192.168.3.241  
	User root  
	Port 2222  
	IdentityFile ~/.ssh/my_server_key  
	#指定**私钥文件**的路径。这里为 `~/.ssh/my_server_key`，SSH 会使用该私钥进行公钥认证（而非默认的 `~/.ssh/id_rsa` 等）。
	IdentitiesOnly yes
	#强制**只使用** `IdentityFile` 指定的密钥（以及 `ssh-agent` 中可能添加的其他密钥？实际上 `IdentitiesOnly yes` 会让 SSH **只尝试**配置文件中明确指定的密钥文件，而忽略 `ssh-agent` 中缓存的其它密钥）。这可以避免因 `ssh-agent` 中存有多个密钥而导致认证失败或尝试顺序混乱的问题。
```

    **整体逻辑**：
    当执行`ssh myserver` 时，实际效果等价于：

    ssh -i ~/.ssh/my_server_key -o IdentitiesOnly=yes root@154.9.25.235 -p 22

    但配置块让每次连接更简洁，同时方便统一管理多台主机的连接参数。

以后登录只需要：

```shell
ssh myserver
```

还可以直接复制文件：

```shell
scp ./test.txt myserver:/root/
```

或者使用 VS Code Remote SSH 连接 `myserver`。

常用字段含义：

| 字段                   | 含义                                         |
| :--------------------- | :------------------------------------------- |
| `Host`               | 本地别名，可以随便起                         |
| `HostName`           | 真实服务器 IP 或域名                         |
| `User`               | 登录用户名                                   |
| `Port`               | SSH 端口                                     |
| `IdentityFile`       | 私钥路径                                     |
| `IdentitiesOnly yes` | 只使用这里指定的私钥，避免客户端乱试其他钥匙 |
|                        |                                              |

## \*配置心跳包

真正使用过程中由于经常需要停下来查看攻略，总会出现一段时间不操作服务器自己断联的情况，此时就得在config中配置心跳包了

```text
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 10
```

在config文件中最开头加上这一段即可全局生效，若想单独给其中某些服务器配置则需要在特定的地方修改。

其中第一行意味着每隔60秒发送一次心跳包，第二行意味着连续10次无响应才断开

# 2.创建普通用户

---

如果你一直用 `root` 登录，操作确实方便，但也更危险。更推荐创建一个普通用户，通过 `sudo` 管理服务器。

以 Debian / Ubuntu 为例：

```shell
sudo adduser mint  
sudo usermod -aG sudo mint
```

然后给这个用户配置 SSH 公钥：

```shell
sudo mkdir -p /home/mint/.ssh  
sudo nano /home/mint/.ssh/authorized_keys  
sudo chmod 700 /home/mint/.ssh  
sudo chmod 600 /home/mint/.ssh/authorized_keys  
sudo chown -R mint:mint /home/fghmnst/.ssh
```

本地测试：

```shell
ssh mint@服务器IP
```

登录后验证 sudo：

```shell
sudo whoami
```

如果输出：

```shell
root
```

说明这个普通用户可以通过 `sudo` 执行管理员命令。

# 3.关闭密码登录

---

确认密钥登录和 sudo 都没问题以后，可以考虑关闭密码登录。

编辑：

```shell
sudo nano /etc/ssh/sshd_config
```

推荐配置：

```text
PubkeyAuthentication yes  
PasswordAuthentication no  
PermitRootLogin prohibit-password
```

含义：

- `PubkeyAuthentication yes`：允许密钥登录。
- `PasswordAuthentication no`：禁止密码登录。
- `PermitRootLogin prohibit-password`：root 不能用密码登录，但可以在配置了公钥时用密钥登录。

如果你想更严格，可以完全禁止 root 远程登录：

```text
PermitRootLogin no
```

改完后检查配置：

```shell
sudo sshd -t
```

重启服务：

```shell
sudo systemctl restart ssh  
# 或  
sudo systemctl restart sshd
```

然后开一个新终端测试：

```shell
ssh fghmnst@服务器IP
```

确认新连接能登录，再关闭旧窗口。

# \*文件传输

---

SSH 不只可以登录，还可以传文件。

## scp

把本地文件上传到服务器：

```shell
scp ./index.html root@服务器IP:/var/www/html/
```

从服务器下载文件到本地：

```shell
scp root@服务器IP:/var/log/nginx/access.log ./
```

指定端口：

```shell
scp -P 2222 ./index.html root@服务器IP:/var/www/html/
```

注意：`ssh` 用小写 `-p` 指定端口，`scp` 用大写 `-P`。

## sftp

进入交互式文件传输：

```shell
sftp root@服务器IP
```

常用命令：

```text
put 本地文件  
get 远程文件  
ls  
pwd  
cd  
exit
```

如果你已经写了 SSH Config：

```shell
sftp myserver
```

常见报错见原文。
