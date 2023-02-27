from dataSources.indeed.indeed_scrapper import IndeedScrapper
from repository.IndeedRepo import IndeedRepo
from dataSources.glassdoor.glassdoor_scrapper import GlassDoorScrapper
from repository.glassdoor_repo import GlassdoorRepo


def main():
    # indeed_repo = IndeedRepo()
    # indeed_scrapper = IndeedScrapper(indeed_repo)
    # indeed_scrapper.run("rabbitmq")

    glassdoor_repo = GlassdoorRepo()
    glassdoor_scrapper = GlassDoorScrapper(glassdoor_repo)
    glassdoor_scrapper.run()


if __name__ == "__main__":
    main()
