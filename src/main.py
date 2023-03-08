from dataSources.indeed.indeed_scrapper import IndeedScrapper
from repository.IndeedRepo import IndeedRepo
from dataSources.glassdoor.glassdoor_scrapper import GlassDoorScrapper
from repository.glassdoor_repo import GlassdoorRepo
from repository.unified_repo import UnifiedRepo


def main():
    unified_repo = UnifiedRepo()

    # indeed_scrapper = IndeedScrapper(unified_repo)
    # indeed_scrapper.run("rabbitmq")

    glassdoor_scrapper = GlassDoorScrapper(unified_repo)
    glassdoor_scrapper.run()


if __name__ == "__main__":
    main()
