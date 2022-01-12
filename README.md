# Web Crawler (Backend-Focused)
Create a web crawler to scrape phone numbers from web pages. The web crawler should take a starting page and follow any links on that page to other pages, collecting phone numbers it finds along the way. When the crawling is done it should output all the phone numbers it found. Do not just drop in an existing web crawler or web crawling framework, you should write the crawling code yourself (but can use libraries for other things). Getting phone number detection exactly perfect isn't a requirement so don't spend too much time on that aspect.



Once you've completed the minimum requirements, take some time to impress us with extra features. Some ideas: parallelism, tests, obeying robots.txt, controlling crawl-depth, etc. Whatever shows off your strengths is what we want to see!



You can develop against our test page or use pages on the broader internet.

When provided with the test page the crawler should output:

555-555-1234

555-555-2345

555-555-9872

(order isn't important)

# Sample Output

Visited sites: \
https://therecount.github.io/interview-materials/project-a/3.html \
https://therecount.github.io/interview-materials/project-a/2.html \
https://therecount.github.io/interview-materials/project-a/1.html

Phone numbers collected: \
555-555-1234 \
555-555-2345 \
555-555-9876

Count of numbers per domain: \
{'therecount.github.io': 3}
