import requests

PROXY_URL = "https://proxylist.geonode.com/api/proxy-list?page=%s"


def main():
    proxy_list = list()
    for index in range(40):
        print(f"index: {index}")
        proxy_json = requests.get(PROXY_URL % index)
        proxy_list += [{"ip": item["ip"], "port": item.get("port")} for item in proxy_json.json()["data"]]

    print(len(proxy_list))
    for proxy in proxy_list:
        if proxy["port"]:
            proxy_dict = {"http": f"{proxy['ip']}:{proxy['port']}", "https": f"{proxy['ip']}:{proxy['port']}"}
        else:
            proxy_dict = {"http": f"{proxy['ip']}", "https": f"{proxy['ip']}"}

        try:
            r = requests.get("http://api.my-ip.io/ip", proxies=proxy_dict, timeout=5)
            print(r.text)
        except Exception as error:
            print(f"ERROR: {error}")


if __name__ == "__main__":
    main()
