#!/bin/env python3
# -*- coding: UTF-8 -*-
"""
Returns IP from SPF field in the DNS query. If domain not exist, exits with 1.
If no IP but no error in DNS query, no ip listed and exits with 0.
"""

import dns.resolver
import argparse
import ipaddress


def spf2ip(spf, host):
    ips = list()
    if "spf" in spf and "redirect" not in spf:
        spf_fields = spf.split()
        for field in spf_fields:
            if "ip4" in field:
                ips.append(field.split("ip4:")[1])
            elif "mx" in field:
                try:
                    answer = dns.resolver.query(host, 'MX')
                    for a in answer:
                        mx_a = dns.resolver.query(str(a).split()[1])
                        for mx_ip in mx_a:
                            ips.append(mx_ip.to_text())
                except:
                    pass
        return(ips)
    else:
        return(None)


def ip_list(host):
    ips = list()
    try:
        answer = dns.resolver.query(host, 'TXT')
    except:
        exit(1)
    for rdata in answer:
        ips = spf2ip(rdata.to_text(), host)
        if ips:
            return(ips)
    for rdata in answer:
        if "redirect" in rdata.to_text():
            answer = dns.resolver.query(
                    rdata.to_text().split()[1].split("=")[1][:-1], 'TXT'
                    )
            for rdata in answer:
                if "include" not in rdata.to_text():
                    ips = spf2ip(rdata.to_text(), host)
                    if ips:
                        return(ips)
                else:
                    for include in [include for include in rdata.to_text().split() if "include" in include]:
                        answer = dns.resolver.query(include.split(":")[1], 'TXT')
                        for rdata in answer:
                            include_ips = list()
                            ips = spf2ip(rdata.to_text(), host)
                            if ips:
                                include_ips += ips
                        return(include_ips)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host')
    args = parser.parse_args()
    settings = vars(args)
    if ip_list(settings['host']):
        for ip in ip_list(settings['host']):
            try:
                ipaddress.ip_network(str(ip))
                print(ip)
            except:
                pass
