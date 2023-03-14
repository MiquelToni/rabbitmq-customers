
def repo_query(order_field='STARGAZERS', order_direction='ASC', page_cursor=''):
    repo_query = """
    {
        topic(name: "rabbitmq") {
            repositories(
            affiliations: COLLABORATOR
            first: 100
            orderBy: {field: %s, direction: %s}
            %s
            ) {
                edges {
                    node {
                        id
                        name
                        nameWithOwner
                        owner {
                            id
                            url
                            login
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
    """ % (order_field, order_direction, page_cursor)
    return repo_query

def company_query(username):
    company_query = """
    {
        user(login: "%s") {
            company
        }
    }
    """ % (username)
    return company_query