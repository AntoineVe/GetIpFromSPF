# GetIpFromSPF
Returns IP from SPF field in the DNS query

# Usage
`bash` example, this will add google mail servers IPs in a pf table :

```bash
for ip in `./get_ip_from_dns.py gmail.com`; do pfctl -t spamd-white -T add $ip; done
```

