# openssl

 openssl version -a
OpenSSL 1.1.1n  15 Mar 2022
built on: Tue Aug 15 19:14:44 2023 UTC
platform: debian-amd64
options: 
OPENSSLDIR: "/usr/lib/ssl"
ENGINESDIR: "/usr/lib/x86_64-linux-gnu/engines-1.1"
Seeding source: os-specific

## versionを表示する　オプション-a

 openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 > test9key.pem

        　genpkeyコマンドを使用する


 openssl pkey -text -noout -in test9key.pem

        pkey コマンドで　内容を表示する

 openssl genpkey -out sertest.key -aes128 -algorithm RSA -pkeyopt rsa_keygen_bits:4096
 パスフレーズを使って　sertest.key を生成


## .key .pem .pub 拡張子の違い　内容に合わせて使用する
privatekey は　PUBLIC KEY を作る時に利用　PUBLIC KEYにはprivatekeyも内包


#### 公開キー　秘密キー　証明書　署名　各役割を理解してからコマンドを利用
　openssl のコマンドは　csr　crt　証明書生成　表示　　すべて可能


 #### パスワードだけを使って　ファイルを暗号化　復号化
 openssl enc -e -aes-256-cbc -pbkdf2 -in test.jpg -out enctest.jpg

 ファイルを調べてみる
  file enctest.jpg
enctest.jpg: openssl enc'd data with salted password

openssl enc -d -aes-256-cbc -pbkdf2 -in test.jpg -out dectest.jpg

　wsl　debianで実行　　-pbkdf2 推奨オプション

