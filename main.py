import requests


search = input()
gender = input()

url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + search +'&submit=y&gender_section=' + gender
r = requests.get(url)
text = r.text
count = ''
prices = []
articles = []
names = []
brands = []
discounts = []
data = ''

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


if int(count) % 60 == 0:
    pages = int(count) // 60
else:
    pages = int(count) // 60 + 1

for t in range(1, pages + 1):
    if t != 1:
        cur_url = url + '&page=' + str(t)
        r = requests.get(cur_url)
        text = r.text
    for i in range(len(text)):
        ptr_1 = text[i:i + 15]
        ptr_2 = text[i:i + 13]
        ptr_3 = text[i:i + 14]
        ptr_4 = text[i:i + 12]
        ptr_5 = text[i:i + 11]
        if ptr_1 == '\"price_amount\":':
            for j in range(i + 15, len(text)):
                if text[j].isdigit():
                    data += text[j]
                elif data == '':
                    continue
                else:
                    prices.append(data)
                    data = ''
                    break
        elif ptr_2 == '\"short_sku\":\"':
            for j in range(i + 13, len(text)):
                if text[j] != '\"':
                    data += text[j]
                else:
                    if data not in articles:
                        articles.append(data)
                    data = ''
                    break
        if ptr_3 == 'product-name\">':
            for j in range(i + 15, len(text)):
                if text[j] != '<':
                    data += text[j]
                elif data != '':
                    names.append(data)
                    data = ''
                    break
        elif ptr_4 == 'brand-name\">':
            for j in range(i + 12, len(text)):
                if text[j] != '<':
                    data += text[j]
                elif data != '':
                    brands.append(data)
                    data = ''
                    break


print(count, pages)
print(text)
print(len(prices))
print(prices)
print(len(articles))
print(articles)
print(len(names))
print(names)
print(len(brands))
print(brands)
