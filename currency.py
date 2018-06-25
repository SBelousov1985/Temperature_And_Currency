import requests
import xml.etree.ElementTree as ElementTree


def get_trip_info_from_file(file_name):
    info = []
    with open(file_name) as f:
        while True:
            info_s = f.readline().split()
            if not info_s:
                break
            info.append({'from-to': info_s[0],
                         'value': int(info_s[1]),
                         'currency': info_s[2]})
    return info


def convert_to(value, cur_from, cur_to='RUB'):
    headers = {'Content-Type': 'text/xml'}
    data = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <Convert xmlns="http://webservices.currencysystem.com/currencyserver/">
          <licenseKey>{''}</licenseKey>
          <fromCurrency>{cur_from}</fromCurrency>
          <toCurrency>{cur_to}</toCurrency>
          <amount>{value}</amount>
          <rounding>{'false'}</rounding>
          <format>{''}</format>
          <returnRate>{'curncsrvReturnRateNumber'}</returnRate>
          <time>{''}</time>
          <type>{''}</type>
        </Convert>
      </soap:Body>
    </soap:Envelope>'''
    res = requests.post("https://fx.currencysystem.com/webservices/CurrencyServer5.asmx",
                        data=data,
                        headers=headers)
    data = ElementTree.fromstring(res.text)
    return float(data[0][0][0].text)


trip_info = get_trip_info_from_file('currencies.txt')
total = 0
for info in trip_info:
    cost = convert_to(info['value'], info['currency'])
    total += cost
    print(info['from-to'], int(round(cost, 2)), 'руб.')
print('Итого:', round(total + 0.5), 'руб.')
