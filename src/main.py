from dataSources.indeed.indeed_scrapper import IndeedScrapper
from repository.IndeedRepo import IndeedRepo


def main():
    print("Hello World!")
    indeed_repo = IndeedRepo()
    indeed_scrapper = IndeedScrapper(indeed_repo)
    indeed_scrapper.crawl_page("rabbitmq")


if __name__ == "__main__":
    main()
