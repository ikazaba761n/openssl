s# openssl

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

### openssl コマンドで　ランダムを生成
32byte パスワードの生成
        openssl rand -base64 -out passward 32
        
        最後の数字は　バイト数
cat passward

X0ZhryO1DN12UBWp9YHUnf033mIslrU+yt/x0M6Z9Ig=

 wc passward
 1  1 45 passward


#### rsautl コマンド
rsautl  間違いやすいポイント　decrypt　復号　-d省略はできない

                -infile　- ハイフンをつける
                
         openssl rsautl -encrypt -in 2he.txt  -out 2henc.dat -inkey secret.key
         

        暗号化は上記の　構文　-inkey の場所はどこでも可（状況により）
        
        secret.key は　rsagenコマンドで作ったプライベートkey


         openssl rsautl -decrypt -in 2henc.dat  -out 2hetest.txt -inkey secret.key

        復号は　-decrypt -out 出力するファイルは拡張子を変える事

 
#### openssl pkey を使う　ヘルプを表示するには　ハイフンは使わない
openssl  help pkey
Usage: pkey [options]
Valid options are:
 -help             Display this summary
 -inform format    Input format (DER or PEM)
 -outform PEM|DER  Output format (DER or PEM)
 -passin val       Input file pass phrase source
 -passout val      Output file pass phrase source
 -in val           Input key
 -out outfile      Output file
 -pubin            Read public key from input (default is private key)
 -pubout           Output public key, not private
 -text_pub         Only output public key components
 -text             Output in plaintext as well
 -noout            Don't output the key
 -*                Any supported cipher
 -traditional      Use traditional format for private keys
 -engine val       Use engine, possibly a hardware device
 -check            Check key consistency
 -pubcheck         Check public key consistency

 #### プライベートkeyを作成
 openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -aes-128-cbc > prikey.pem

 #### ファイルの中身を調べる　テキスト文字である
  file prikey.pem
prikey.pem: ASCII text

#### pkey サブコマンドで調べる　
openssl pkey -in prikey.pem -text -noout

#### モジュール　などを表示
RSA Private-Key: (2048 bit, 2 primes)
modulus:
    00:bf:d6:2d:bf:8b:20:55:05:12:4c:22:b7:33:ff:
    
publicExponent: 65537 (0x10001)
privateExponent:
    37:b3:
prime1:
    00:de:
prime2:
    00:dc:
exponent1:
    00:b8
exponent2:
    33:5
coefficient:
    5c:98
#### プライベートkeyから　パブリックキーを作成
openssl pkey -pubout < prikey.pem > pubikey.pem
### パブリックキーの内容を表示
  openssl pkey -in pubikey.pem -text -noout
  上記では表示されない
#### 以下のコマンドだと表示される
openssl pkey -text -noout -pubin < pubikey.pem
RSA Public-Key: (2048 bit)
Modulus:
    00:bf:d6:2d
Exponent: 65537 (0x10001)

#### openssl pkey -pubin -in pubikey.pem -text -noout 
-pubin パブリッキーを指定　マニュアルだと指定しないとプライベートkeyとなる


#### csrファイルを作成
openssl req -new -key prikey.pem > request.csr
Enter pass phrase for prikey.pem:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.


#### A challenge password  csrファイルを作る時に入力　入れなくても可
  プライベートkeyを作る時のパスワードではない
  A challenge password は証明書を破棄するためのパスワード
  csrファイルを　テキストで出力するときにパスワードが表示されるので驚く
  プライベートkeyを作る時のパスワードと同じにしないこと
 
 Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:test（この文字列が表示される）



####　openssl req -text -noout < request.csr
csrファイルをテキストとして表示　サブコマンドは　req
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C = ja, ST = ja, L = ja, O = ja, OU = ja, CN = ja, emailAddress = p@test
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
                Modulus:
                    00:bf:
                Exponent: 65537 (0x10001)
        Attributes:
            challengePassword        :test
    Signature Algorithm: sha256WithRSAEncryption
         5f:c2:68:9c:b5:dc:c4:84:1d:d3:dd:12:cf:cc

#### アルゴリズムを指定
openssl genpkey -out server.key -algorithm EC -pkeyopt ec_paramgen_curve:prime256v1

openssl pkey -text -noout < server.key | more
Private-Key: (256 bit)
priv:
    ef:49:a0:f2:bd:c1:e5:4a:02:fd:5c:bc:32:1c:f1:
    db:65:a
pub:
    04:80:8b:e5:66:ad:70:d8:8c:a9:ee:62:0f:25:87:
    e7:f1:d0:8a:7a:76:93:c4:dd:40:92:25:ba:66:
    9a:ef:52:50:41:99:12:16:f3:c6:84:60:d9:a3:fb:
    0a:cc:41:fe:98
ASN1 OID: prime256v1
NIST CURVE: P-256

### less server.key
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg70mg8r3B5UoC/Vy8
Mhzx22WhzsmlUh6/77Rbv7B/fEKhRANCAASAi+VmrXDYjKnuYg8lh+fx0WfThc+j
/ar0nqhhqPBiiWCKenaTxN1AkiW6ZprvUlBBmRIW88aEYNmj+wrMQf6Y
-----END PRIVATE KEY-----


#### openssl ディレクトリの内容
dir /etc/ssl
certs  openssl.cnf  private

certs ディレクトリ
_Root_CA.pem
_Root_CA_-_G2.pem
_Primary_Root_CA_-_G3.pem

private ディレクトリ
sudo dir /etc/ssl/private
cat ssl-cert-snakeoil.key
BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w
-----END PRIVATE KEY-----

#### スネークオイルの意味　あてにならない　効果なし
SSLのサンプルとしてインストールされている証明書の認証サイトの名前



#### 認証局の秘密キーを作成 cnfファイルを指定
openssl req -new -config /usr/lib/ssl/openssl.cnf -x509 -keyout cakey.pem -out cacert.pem -days 3650 -sha256


####  openssl x509 -text -noout -in cacert.pem


#### cnfファイルを指定しない
openssl req -new -keyout testkey.pem -out testeq.pem

ls
testeq.pem  testkey.pem



#### /dev/urandom /dev/random
u  unlocked ランダム　内部を再利用　　urandom 
random 真の乱数　
cat /dev/random > random.txt
ls -lh random.txt
-rwxrwxrwx 1  2.6G 12月  1 12:17 random.txt

cat /dev/urandom > urandom.txt
ls -lh urandom.txt
-rwxrwxrwx 1  1.2G 12月  1 12:17 random.txt
#### 保有している乱数の表示
cat /proc/sys/kernel/random/entropy_avail
4096
#### 上限設定
cat /proc/sys/kernel/random/poolsize
4096
#### 乱数　エントロピープールは違う。
#### > cat /dev/random > testrandom.txt

処理時間がかかる、２ギガを１分くらいかけてテキストに入力
hdd デバイスに乱数を書き込んで消去には向かない　dd　引数if

#### openssl genpkey pkey
2023年 12月  2日 土曜日 13:17:26 JST



        openssl pkey キーの作成　確認

 openssl genpkey -algorithm ed25519 -out server_key.pem
        アルゴリズムを　ed25519

        確認するには　pkeyコマンドが必要　rsaではできない
        rsaでキーを作成していないので当然か
openssl pkey -text -noout -in server_key.pem
ED25519 Private-Key:
priv:
    e9:7d:7d:c0:93:8c:62:8c:1c:e1:25:4a:0d:15:f5:
    7a:98:28:91:b5:63:d4:28:a0:e3:5b:81:51:fe:d3:
    b4:34
pub:
    26:af:7d:5c:92:36:d8:73:57:72:95:89:ae:e7:bf:
    c7:ad:a9:26:71:e7:7d:d4:33:10:75:aa:8d:0a:cc:
    b6:62
 #### openssl genrsa genpkey
 3.o　では　genrsa 非推奨となっている
 This command has been deprecated. The openssl-genpkey(1) command should be used instead.


 #### キー作成　rsaを指定
 openssl genpkey -out testdec3.key -algorithm RSA -pkeyopt rsa_keygen_bits:4096

 #### キー確認
  openssl pkey -text -noout -in testdec3.key

#### ssl/tls 対応確認　openssl サブコマンド　s_client
openssl s_client -connect www.google.com:443
#### グーグルwebサイト　https　ポート　443　確認
#####
CONNECTED(00000003)
depth=2 C = US, O = Google Trust Services LLC, CN = GTS Root R1
verify return:1
depth=1 C = US, O = Google Trust Services LLC, CN = GTS CA 1C3
verify return:1
depth=0 CN = www.google.com
verify return:1
---
Certificate chain
 0 s:CN = www.google.com
   i:C = US, O = Google Trust Services LLC, CN = GTS CA 1C3
 1 s:C = US, O = Google Trust Services LLC, CN = GTS CA 1C3
   i:C = US, O = Google Trust Services LLC, CN = GTS Root R1
 2 s:C = US, O = Google Trust Services LLC, CN = GTS Root R1
   i:C = BE, O = GlobalSign nv-sa, OU = Root CA, CN = GlobalSign Root CA
---
Server certificate
-----BEGIN CERTIFICATE-----
TUdJzBqBggrBgEFBQcBAQReMFwwJwYIKwYBBQUHMAGGG2h0dHA6Ly9vY3Nw
LnBraS5nb29nL2d0czFjMzAxBggrBgEFBQcwAoYlaHR0cDovL3BraS5nb29nL3Jl
cG8vY2VydHMvZ3RzMWMzLmRlcjAZBgNVHREEEjAQgg53d3cuZ29vZ2xlLmNvbTAh
BgNVHSAEGjAYMAgGBmeBDiPeRwiiPZFXXAYMbWWnLD0Hw60dTX790fReAB2
AHb/iD8KtvuVUcJhzPWHujS0pM27KdxoQgqf5mdMWjp0AAABi1x+1+kAAAQDAEcw
RQIhAIWdZThm1Q==
-----END CERTIFICATE-----
subject=CN = www.google.com

issuer=C = US, O = Google Trust Services LLC, CN = GTS CA 1C3

---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: ECDSA
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 4293 bytes and written 386 bytes
Verification: OK
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 256 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 0 (ok)
---
read:errno=0
#### CN(コモンネーム≒ドメイン) 
     depth=2 ルート証明書。
     depth=1 中間CA証明書。
     depth=0 TLSサーバー証明書


 ##### crl file 確認　
 $ openssl crl -inform der -in SCRoot2CRL.crl -text | more
Certificate Revocation List (CRL):
        Version 2 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = JP, O = "SECOM Trust Systems CO.,LTD.", OU = Security Communicati
on RootCA2
        Last Update: Nov 29 05:46:59 2023 GMT
        Next Update: Nov 27 05:46:59 2024 GMT
        CRL extensions:
            X509v3 Authority Key Identifier:
                keyid:0A:85:A9:77:65:05:98:7C:40:81:F8:0F:97:2C:38:F1:0A:EC:3C:CF

            X509v3 CRL Number:
                162
Revoked Certificates:
    Serial Number: 22B9B0BD
        Revocation Date: May 27 06:18:09 2021 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Cessation Of Operation
    Serial Number: 22B9B0C6
        Revocation Date: May 27 06:21:34 2021 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Cessation Of Operation
    Serial Number: 22B9B0C7
        Revocation Date: Aug 31 06:31:33 2021 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Cessation Of Operation
    Serial Number: 22B9B0CA
        Revocation Date: May 27 05:18:58 2021 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Cessation Of Operation
    Serial Number: 22B9B0CC
        Revocation Date: Aug 31 06:04:44 2021 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code:
                Cessation Of Operation
 #### openssl  pkey -text -noout プライベートキーを表示させない

 RSA Private-Key: (2048 bit, 2 primes)
modulus:
    00:d8:60:1d:5a:32:47:8f:c1:0a:c1:95:ea:9d:d2:

-----BEGIN PRIVATE KEY-----
MIIjLZertP/x+bHJ/vkETwC+ahZx4=
-----END PRIVATE KEY-----
RSA Private-Key: (4096 bit, 2 primes)
modulus:
    00:d8:60:1d:5a:32:47:8f:c1:0a:c1:95:ea:9d:d2:

 暗号化の係数も表示される
coefficient:
    6b:84:8b:46:b8:00:71:7e:16:f6:58:96:f0:27:b1:
    
    
    
    








  


