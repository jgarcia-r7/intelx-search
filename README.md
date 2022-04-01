# intelx-search
IntelX Search Tool for Emails

## Description:  
**intelx-search.py** interfaces with https://public.intelx.io and its API. It retrieves the latest public API key for its queries. It queries the Public IntelX database for email addressess based on the domain name you supply and the results limit. The tool can also proxy requests through a SOCKS5 proxy with `-s`. Email addressess are written to `emails.txt` by default, unless output file name is specified with `-o`.

## Usage:  
```bash
git clone https://github.com/jgarcia-r7/intelx-search
pip3 install -r requirements
./intelx-search.py -h
```
**intelx-search.py** takes the following arguments:
```bash
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Target domain REQUIRED
  -l LIMIT, --limit LIMIT
                        Results limit OPTIONAL (Defualt: 10000)
  -o OUTPUT, --output OUTPUT
                        Output file name OPTIONAL (Defualt: emails.txt)
  -s SOCKS, --socks SOCKS
                        Proxy requests through SOCKS5 proxy OPTIONAL (Ex: -s 127.0.0.1)
  -sp SOCKS_PORT, --socks_port SOCKS_PORT
                        SOCKS5 proxy port OPTIONAL (Ex: -sp 1080 | Default: 1080)
```

**Example:**  
![image](https://user-images.githubusercontent.com/81575551/161337743-709045d1-5308-48c3-8754-6c25f7434132.png)
