# An example to get the remaining rate limit using the Github GraphQL API.

import requests
from dataSources.github.queries import repo_query, company_query
import json
from tqdm import tqdm
from datetime import datetime
from dataSources.github.secrets.github_key import API_TOKEN_GITHUB
from repository.githubRepo import GithubRepo

headers = {"Authorization": f"token {API_TOKEN_GITHUB}"}

ORDER_FIELD = ['UPDATED_AT', 'PUSHED_AT', 'NAME', 'STARGAZERS', 'CREATED_AT']
ORDER_DIRECTION = ['ASC', 'DESC']
PATH = f'data/github_result_{str(datetime.now())}.json'


class GithubForRabbitMQ():
    def __init__(self, db):
        self.db = db
        self.logins = set()
        self.companies = set()
        self.empty_users = set()

    def run_query(self, query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def read_json(self, path):
        try:
            with open(path, "r", encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
            return data
        except FileNotFoundError:
            return {}

    def write_json_file(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def update_json(self, path, new_login, new_company_info):
        data = self.read_json(path)
        data[new_login] = new_company_info
        self.write_json_file(path, data)

    def save_info(self, path, login, company):
        data = self.read_json(path)
        if data:
            self.update_json(path, login, company)
        else:
            self.write_json_file(path, {login: company})

    def look_into_results(self, edges):
        for edge in tqdm(edges):
            login = edge["node"]["owner"]["login"]
            if login in self.logins:
                continue
            self.logins.add(login)
            comp_query = company_query(login)
            company_result = self.run_query(comp_query)
            try:
                company = company_result["data"]["user"]["company"]
                if company and company not in self.companies:
                    # self.save_info(PATH, f'company_{len(self.companies)}', company)
                    self.db.insert_company({'company_name': company,
                                            'source': 'github',
                                            'saved_timestamp': str(datetime.now()),
                                            'company_or_login': 'company'})
                self.companies.add(company)
            except TypeError:
                if login in self.empty_users:
                    continue
                self.empty_users.add(login)
                # self.save_info(PATH, f'no_user{len(self.empty_users)}', login)
                self.db.insert_company({'company_name': login,
                                        'source': 'github',
                                        'saved_timestamp': str(datetime.now()),
                                        'company_or_login': 'login'})
                # print(f"No user with that login")

    def run(self):
        for order_field in ORDER_FIELD:
            for order_direction in ORDER_DIRECTION:
                next_cursor = None
                page_cursor = ''
                page = 1
                while page <= 15:
                    if next_cursor:
                        page_cursor = f'after: "{next_cursor}"'
                    result = self.run_query(repo_query(order_field=order_field, order_direction=order_direction, page_cursor=page_cursor)) # Execute the query
                    print(f'Order field: {order_field}, order direction: {order_direction}, page: {page}')
                    self.look_into_results(result["data"]["topic"]["repositories"]["edges"])

                    if result['data']['topic']['repositories']['pageInfo']['hasNextPage']:
                        next_cursor = result['data']['topic']['repositories']['pageInfo']['endCursor']
                        page += 1
                    else:
                        break


if __name__ == '__main__':
    repo = GithubRepo()

    helper = GithubForRabbitMQ(db=repo)
    helper.run()
