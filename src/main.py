from bs4 import BeautifulSoup
from dataSources.indeed.DataResolver import DataResolver as IndeedDataResolver

indeedDataResolver = IndeedDataResolver()

html = indeedDataResolver.get_data_html("rabbitmq", 0)


soup = BeautifulSoup(html)
print(soup.prettify())
