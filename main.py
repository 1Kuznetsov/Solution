import requests
import time
start_time = time.time()

search = input()
gender = input()

url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + search + '&submit=y&gender_section=' + gender
part_url = 'https://www.lamoda.ru/p/'
r = requests.get(url)
text = r.text

count = ''
articles = []
names = []
brands = []
prices = []
discounts = []
countries = []
data = ''
links = []

for k in range(len(text)):
    ptr = text[k:k+6]
    if ptr == 'найден':
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

last = count % 60

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

    while 'product-name\">' in text:
        for j in range(14, len(text)):
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

print(count, pages)
print(len(links), links)
print(len(prices))
print(prices)
print(len(articles))
print(articles)
print(len(names))
print(names)
print(len(brands))
print(brands)
print("--- %s seconds ---" % (time.time() - start_time))
