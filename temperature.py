import requests
import xml.etree.ElementTree as ElementTree


def get_tempf_from_file(file_name):
    temperatures_f = []
    with open(file_name) as f:
        while True:
            temperature_s = f.readline().split()
            if not temperature_s:
                break
            temperatures_f.append(int(temperature_s[0]))
    return temperatures_f


def fahrenheit_to_celsius(temp_f):
    headers = {'Content-Type': 'text/xml'}
    data = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <FahrenheitToCelsius xmlns="https://www.w3schools.com/xml/">
          <Fahrenheit>{temp_f}</Fahrenheit>
        </FahrenheitToCelsius>
      </soap:Body>
    </soap:Envelope>'''
    res = requests.post("https://www.w3schools.com/xml/tempconvert.asmx",
                        data=data,
                        headers=headers)
    namespaces = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
    data = ElementTree.fromstring(res.text)
    return float(data[0][0][0].text)


temps_f = get_tempf_from_file('temps.txt')
mid_temp_f = sum(temps_f) / len(temps_f)
print('Средняя температура в градусах Цельсия:',
      round(fahrenheit_to_celsius(mid_temp_f), 2))
