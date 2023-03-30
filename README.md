# RabbitMQ

- requests -> gets banned by anti-crawler 403
- scrapy -> gets banned by anti-crawler 403
- selenium -> slow but it works -> we can explore this way

## Setup

- Install dependencies
- Create [Mongodb](https://hub.docker.com/_/mongo)

```bash
docker run -d --name rabbitmq_customers \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=rabbitmq_user \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo
```

**Note: To store to local dir add `-v /my/own/datadir:/data/db` to previous command. Substitute `/my/own/datadir` for your host dir.
**Note2: Create db dump: `docker exec rabbitmq_customers sh -c 'exec mongodump -d <database_name> --archive' > /some/path/on/your/host/all-collections.archive`

- Restart db with `docker restart rabbitmq_customers`
- (Optional): Consider using [Compass](https://formulae.brew.sh/cask/mongodb-compass) to check on the database.

## Known Issues

### Indeed scrapper

- Empty result page not handled properly
- Some attributes are None or not found in some offers
- Improve: Look for a render-less / silent version of the scrapper
- Add proper logger


## Mongo Compass

### Get distinct companies pipeline
``` 
[
  {
    $unwind: {
      path: '$company_name',
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $group: {
      _id: null,
      uniqueCompanies: { $addToSet: '$company_name' }
    }
  }
]
```
