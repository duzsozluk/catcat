import subprocess
import requests

def get_ip_address(website):
  """
  Bu fonksiyon, bir web sitesinin IP adresini ping komutunu kullanarak alır.

  Parametreler:
    website (str): Web sitesinin URL'si.

  Dönüş Değeri:
    str: Web sitesinin IP adresi.
  """
  ping_command = ["ping", "-c", "1", website]
  process = subprocess.Popen(ping_command, stdout=subprocess.PIPE)
  output, _ = process.communicate()
  ip_address = output.decode("utf-8").split(" ")[3]
  return ip_address

def get_all_subdomains(ip_address):
  """
  Bu fonksiyon, bir IP adresinin tüm alt domainlerini alır.

  Parametreler:
    ip_address (str): IP adresi.

  Dönüş Değeri:
    list: IP adresine ait tüm alt domainlerin listesi.
  """
  subdomains = []
  try:
    response = requests.get(f"https://api.shodan.io/dns/search?ip={ip_address}&key=YOUR_SHODAN_API_KEY")
    if response.status_code == 200:
      data = response.json()
      for domain in data["domains"]:
        subdomains.append(domain)
  except Exception as e:
    print(f"Shodan API'ye bağlanırken hata oluştu: {e}")
  return subdomains

def check_for_takeover(subdomains):
  """
  Bu fonksiyon, verilen alt domainlerin takeover olup olmadığını kontrol eder.

  Parametreler:
    subdomains (list): Alt domainlerin listesi.

  Dönüş Değeri:
    list: Takeover olan alt domainlerin listesi.
  """
  takeover_domains = []
  for subdomain in subdomains:
    try:
      response = requests.get(f"http://{subdomain}")
      if response.status_code == 200:
        if "This site is under construction" in response.text:
          takeover_domains.append(subdomain)
    except Exception as e:
      print(f"{subdomain} adresine bağlanırken hata oluştu: {e}")
  return takeover_domains

def main():
  """
  Ana fonksiyon.
  """
  website = input("Web sitesi URL'sini giriniz: ")
  ip_address = get_ip_address(website)
  subdomains = get_all_subdomains(ip_address)
  takeover_domains = check_for_takeover(subdomains)

  if takeover_domains:
    print(f"Takeover olan alt domainler: {takeover_domains}")
  else:
    print("Herhangi bir takeover tespit edilmedi.")

if __name__ == "__main__":
  main()
