from dataSources.indeed.indeed_scrapper import IndeedScrapper
from dataSources.glassdoor.glassdoor_scrapper import GlassDoorScrapper
from dataSources.linkedIn.linkedin_scrapper import LinkedInScrapper
from repository.unified_repo import UnifiedRepo


def main():
    unified_repo = UnifiedRepo()

   # indeed_scrapper = IndeedScrapper(unified_repo)
   # indeed_scrapper.run("rabbitmq")

    glassdoor_scrapper = GlassDoorScrapper(unified_repo)
    glassdoor_scrapper.run()

    linkedin_scrapper = LinkedInScrapper(unified_repo)
    linkedin_scrapper.run()

if __name__ == "__main__":
    main()
