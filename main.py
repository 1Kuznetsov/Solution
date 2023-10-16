import requests
import ru_local as ru

search = input(ru.SEARCH)
gender = input(ru.GENDER)

if gender == ru.MEN:
    gender = 'men'
elif gender == ru.WOMEN:
    gender = 'women'

url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + search + '&submit=y&gender_section=' + gender
part_url = 'https://www.lamoda.ru/p/'
r = requests.get(url)
text = r.text

count = ''
data = ''
articles = []
names = []
brands = []
prices = []
discounts = []
countries = []
links = []
result = []

for k in range(len(text)):
    ptr = text[k:k+6]
    if ptr == ru.FOUND:
        for j in range(k, len(text)):
            if count == '' and not text[j].isdigit():
                continue
            elif text[j].isdigit():
                count += text[j]
            else:
                break

count = int(count)

if count % 60 == 0:
    pages = count // 60
else:
    pages = count // 60 + 1

for t in range(1, 2):
    if t != 1:
        cur_url = url + '&page=' + str(t)
        r = requests.get(cur_url)
        text = r.text

    text_initial = text

    index_0 = text_initial.find('<a href=\"/p/')
    text = text_initial[index_0:]

    while '<a href=\"/p/' in text:
        for j in range(12, len(text)):
            if text[j] != '\"':
                data += text[j]
            else:
                links.append(part_url + data)
                data = ''
                text = text[j:]
                index_0 = text.find('<a href=\"/p/')
                text = text[index_0:]
                break

    index_1 = text_initial.find('\"price_amount\":')
    text = text_initial[index_1:]

    while '\"price_amount\":' in text:
        for j in range(15, len(text)):
            if text[j].isdigit():
                data += text[j]
            elif data != '':
                prices.append(data)
                data = ''
                text = text[j:]
                index_1 = text.find('\"price_amount\":')
                text = text[index_1:]
                break

    index_2 = text_initial.find('\"short_sku\":\"')
    text = text_initial[index_2:]

    while '\"short_sku\":\"' in text:
        for j in range(13, len(text)):
            if text[j] != '\"':
                data += text[j]
            else:
                if data not in articles:
                    articles.append(data)
                data = ''
                text = text[j:]
                index_2 = text.find('\"short_sku\":\"')
                text = text[index_2:]
                break

    index_3 = text_initial.find('product-name\">')
    text = text_initial[index_3:]

    while 'product-name\"> ' in text:
        for j in range(15, len(text)):
            if text[j] != '<':
                data += text[j]
            elif data != '':
                names.append(data)
                data = ''
                text = text[j:]
                index_3 = text.find('product-name\">')
                text = text[index_3:]
                break

    index_4 = text_initial.find('brand-name\">')
    text = text_initial[index_4:]

    while 'brand-name\">' in text:
        for j in range(12, len(text)):
            if text[j] != '<':
                data += text[j]
            elif data != '':
                brands.append(data)
                data = ''
                text = text[j:]
                index_4 = text.find('brand-name\">')
                text = text[index_4:]
                break

    for i in links:
        r = requests.get(i)
        text = r.text
        if '"Страна производства","value":' in text:
            index_country = text.find('"Страна производства"')
            text = text[index_country:]
            index_country_value = text.find('value"')
            index_country_value_start = text.find(':')
            index_country_value_end = text.find('}')
            res = text[index_country_value_start + 2:index_country_value_end - 1]
            countries.append(res)
        else:
            countries.append(None)
        if 'percent"' in text:
            index_country = text.find('percent"')
            text = text[index_country:]
            index_country_value_start = text.find(':')
            index_country_value_end = text.find('percent_accumulated')
            text = int(text[index_country_value_start + 1:index_country_value_end - 2])
            discounts.append(text)
        else:
            discounts.append(None)

# for t in range(len(articles)):
#     result.append([articles[t], names[t], brands[t], prices[t], countries[t]])
# result = sorted(result, key=lambda x: x[3])
#
# with open('output.txt', 'w') as f_out:
#     print('|{:13}| {:35}| {:30}| {:7}| {:20}|'.format(ru.ARTICLE, ru.NAME, ru.BRAND, ru.PRICE, ru.COUNTRY), file=f_out)
#     for elem in result:
#         print('|{:13}| {:35}| {:30}| {:7}| {:20}|'.format(*elem), file=f_out)



for t in range(len(articles)):
    result.append([articles[t], names[t], brands[t], prices[t], discounts[t], countries[t]])
result = sorted(result, key=lambda x: x[3])

with open('output.txt', 'w') as f_out:
    print('|{:13}| {:31}| {:30}| {:7}| {:6}| {:15}|'.format(ru.ARTICLE, ru.NAME, ru.BRAND, ru.PRICE, ru.DISCOUNT, ru.COUNTRY), file=f_out)
    for elem in result:
        print('|{:13}| {:31}| {:30}| {:7}| {:6}| {:15}|'.format(*elem), file=f_out)
