# pet_project

Run.

Change directory to prices_scrape and run:

scrapy crawl hellogetsafe -a family_coverage=True -a drone_coverage=True -a zip_code=12249

It is possible to extract to a file by adding: -O output.jl to see extracted data

scrapy crawl hellogetsafe -O output.jl

default values:

zip_code=01067

family_coverage=False 

drone_coverage=False

Tests.

I can clearly explain why tests with crawlers is not a common thing.

The data and structures of the sites are constantly changing and correcting/supporting spiders under the site change is 90% of the work of the developer.
You can write tests based on saved web pages, but the relevance of these web pages can quickly change and the tests will no longer be objective.
Built-in contracts in Scrapy weakly support POST Requests (which are not rare). Therefore, the choice of testing model on a specific project is very dependent and is enough challenging task. Manual testing on a project is not uncommon. I'm more inclined to use monitors like https://spidermon.readthedocs.io/en/latest/index.html
