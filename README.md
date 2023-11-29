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




  


