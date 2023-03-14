
def repo_query(order_field='STARGAZERS', order_direction='ASC'):
    repo_query = """
    {
        topic(name: "rabbitmq") {
            repositories(
                affiliations: COLLABORATOR
                first: 100
                orderBy: {field: %s, direction: %s}
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
            }
        }
    }
    """ % (order_field, order_direction)
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