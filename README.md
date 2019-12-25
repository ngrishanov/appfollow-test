# appfollow-test
Test task for Appfollow: [Hacker News](https://news.ycombinator.com/) parser.

How to run
----------
1. Make sure docker-compose is installed
2. Execute `prepare.sh`
3. Execute `run.sh` to run parser and API. API will be available on `http://localhost:8000`
4. Execute `run-tests.sh` to run tests

API usage example
-----------------

**Request**

```
http://localhost:8000/posts?limit=3&offset=10&order=created&direction=desc
```

**Response**

```
{
    "success": true,
    "result": [
        {
            "id": 21875906,
            "title": "Hippy: React Native Alternative by Tencent",
            "url": "https://github.com/Tencent/Hippy",
            "created": "2019-12-25T16:00:15.399447+00:00"
        },
        {
            "id": 21876818,
            "title": "Drones flying nighttime patterns over NE Colorado leave law enforcement stumped",
            "url": "https://www.denverpost.com/2019/12/23/drones-mystery-colorado/",
            "created": "2019-12-25T16:00:15.399447+00:00"
        },
        {
            "id": 21878292,
            "title": "Grumpy Website – a blog about everything wrong with modern web & tech",
            "url": "https://grumpy.website",
            "created": "2019-12-25T16:00:15.399447+00:00"
        }
    ]
}
```

Libraries and tools used in project
-----------------------------------
- sanic (web server)
- pypika (SQL query builder)
- asyncpg (PostgreSQL asyncio driver)
- beautifulsoup4
- requests
- PostgreSQL
- Docker and Docker-compose
