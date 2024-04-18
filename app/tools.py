import dns.resolver


def get_dns_txt_entries(domain: str):
    results = []
    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(domain, "TXT")
    except dns.resolver.NoAnswer:
        return results

    for server in answers:
        server_content: str = server.to_text()
        server_content = server_content.replace('"', "")
        results.append(server_content)
    return results


def check_dns_txt_entry(domain: str, content: str):
    resuls = get_dns_txt_entries(domain)
    for result in resuls:
        if result == content:
            return True
    return False


if __name__ == "__main__":
    for res in get_dns_txt_entries("google.com"):
        print(res)
    print(check_dns_txt_entry("google.com", "test"))
