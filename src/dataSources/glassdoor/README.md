# Glassdoor scrapper

## How to get Job listing offer

1. Visit `https://www.glassdoor.com/Job/rabbitmq-jobs-SRCH_KO0,8_IP1.htm?includeNoSalaryJobs=true`
2. Get from the response `window.appCache.jlData.jobListings`
    - or parse as text `/window\.appCache = {(.*?)};/` and access `jlData.jobListings`
3. Visit next page by increment the uri index {n+1} `https://www.glassdoor.com/Job/rabbitmq-jobs-SRCH_KO0,8_IP{n+1}.htm?includeNoSalaryJobs=true`
