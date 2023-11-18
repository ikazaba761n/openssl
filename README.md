# openssl

 openssl version -a
OpenSSL 1.1.1n  15 Mar 2022
built on: Tue Aug 15 19:14:44 2023 UTC
platform: debian-amd64
options: 
OPENSSLDIR: "/usr/lib/ssl"
ENGINESDIR: "/usr/lib/x86_64-linux-gnu/engines-1.1"
Seeding source: os-specific

# versionを表示する　オプション-a

 openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 > test9key.pem

        　genpkeyコマンドを使用する


 openssl pkey -text -noout -in test9key.pem

        pkey コマンドで　内容を表示する

 openssl genpkey -out sertest.key -aes128 -algorithm RSA -pkeyopt rsa_keygen_bits:4096
 パスフレーズを使って　sertest.key を生成

 
