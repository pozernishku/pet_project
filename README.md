# pet_project

## Run

Change working folder

```sh
cd prices_scrape
```

Run with default options (`zip_code=01067 , family_coverage=False, drone_coverage=False`)
```sh
scrapy crawl hellogetsafe
```

Or by explicitly specifying options

```sh
scrapy crawl hellogetsafe -a family_coverage=True -a drone_coverage=True -a zip_code=12249
```

Redirect output to file
```
scrapy crawl hellogetsafe -O output.jl
```

Or

```sh
scrapy crawl hellogetsafe -O output.jl -a family_coverage=True -a drone_coverage=True -a zip_code=12249
```

## Tests

Crawler testing isn't a common thing.

The data and structures of the websites are constantly changing and thus correcting/supporting spiders for the website
change consumes 90% of developer's time.
<br/>
Tests can be written based on webpage fixtures, but the relevance of these fixtures can quickly change and the tests
won't reflect the real state of affairs.
<br/>
Built-in contracts in Scrapy weakly support POST Requests (which aren't that rare). Therefore, the choice of testing
model on a specific project is a subject to discuss being quite a challenging task. Manual testing within a project isn't so
uncommon. It's better to use monitors such as https://spidermon.readthedocs.io/en/latest/index.html
