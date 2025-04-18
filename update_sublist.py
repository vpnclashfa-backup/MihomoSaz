secret: ''
sniffer:
  enable: true
  force-domain:
  - +.v2ex.com
  - www.google.com
  - google.com
  port-whitelist:
  - '80'
  - '443'
  skip-domain:
  - Mijia Cloud
  - dlg.io.mi.com
  sniff:
    http:
      override-destination: true
      ports:
      - 1-442
      - 444-8442
      - 8444-65535
    tls:
      override-destination: true
      ports:
      - 1-79
      - 81-8079
      - 8081-65535
  sniffing:
  - tls
  - http
socks-port: 7891
tcp-concurrent: true
tun:
  auto-detect-interface: true
  auto-redir: true
  auto-route: true
  dns-hijack:
  - any:53
  - any:53
  - tcp://any:53
  enable: true
  stack: mixed
unified-delay: true

proxy-providers:
  proxy:
    name: "MyProxy"
    type: "http"
    url: "http://default-url.com"  # اینجا URL تغییر می‌کند
    timeout: 30
    interval: 300
    geoip:
      enabled: true
      file: "geoip.dat"
    udp: false
    tls:
      enabled: false
    remarks: "This is the default proxy provider."
