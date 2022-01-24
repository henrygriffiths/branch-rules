import requests
import json

with open('config.json') as json_file:
    config = json.load(json_file)

username = config['username']
password = config['password']

for repo in config['repos']:
    repo_owner = repo['repository'].split('/')[0]
    repo_name = repo['repository'].split('/')[1]
    if 'repoteam' in repo:
        repoteam = repo['repoteam']
    else:
        repoteam = ""
    for branch in repo['branches']:
        print(repo_owner, repo_name, repoteam, branch)
        data = {}

        inputconfig = config['data']

        if inputconfig['Require status checks to pass before merging'] == True:
            data['required_status_checks'] = {}
            if inputconfig['Require branches to be up to date before merging'] == True:
                data['required_status_checks']['strict'] = True
            else:
                data['required_status_checks']['strict'] = False
            data['required_status_checks']['checks'] = []
            for check in inputconfig['Status checks that are required']:
                if isinstance(check['App ID'], int):
                    data['required_status_checks']['checks'].append({'context': check['Name'], 'app_id': check['App ID']})
                else:
                    data['required_status_checks']['checks'].append({'context': check['Name']})
        else:
            data['required_status_checks'] = None

        if inputconfig['Include administrators'] == True:
            data['enforce_admins'] = True
        else:
            data['enforce_admins'] = None

        if inputconfig['Require a pull request before merging'] == True:
            data['required_pull_request_reviews'] = {}
            data['required_pull_request_reviews']['dismissal_restrictions'] = {}
            data['required_pull_request_reviews']['dismissal_restrictions']['users'] = []
            data['required_pull_request_reviews']['dismissal_restrictions']['teams'] = []
            for user in inputconfig['Restrict who can dismiss pull request reviews']:
                if isinstance(user, str) and len(user) > 0:
                    if user == "${REPOTEAM}":
                        user = repoteam
                    if '/' in user:
                        data['required_pull_request_reviews']['dismissal_restrictions']['teams'].append(user.split('/')[1])
                    else:
                        data['required_pull_request_reviews']['dismissal_restrictions']['users'].append(user)
            if data['required_pull_request_reviews']['dismissal_restrictions']['users'] == []:
                del data['required_pull_request_reviews']['dismissal_restrictions']['users']
            if data['required_pull_request_reviews']['dismissal_restrictions']['teams'] == []:
                del data['required_pull_request_reviews']['dismissal_restrictions']['teams']
            if inputconfig['Dismiss stale pull request approvals when new commits are pushed'] == True:
                data['required_pull_request_reviews']['dismiss_stale_reviews'] = True
            else:
                data['required_pull_request_reviews']['dismiss_stale_reviews'] = False
            if inputconfig['Require review from Code Owners'] == True:
                data['required_pull_request_reviews']['require_code_owner_reviews'] = True
            else:
                data['required_pull_request_reviews']['require_code_owner_reviews'] = False
            if isinstance(inputconfig['Required approvals count'], int) and inputconfig['Required approvals count'] >= 0 and inputconfig['Required approvals count'] <= 6:
                data['required_pull_request_reviews']['required_approving_review_count'] = inputconfig['Required approvals count']
            else:
                data['required_pull_request_reviews']['required_approving_review_count'] = 0
            data['required_pull_request_reviews']['bypass_pull_request_allowances'] = {}
            data['required_pull_request_reviews']['bypass_pull_request_allowances']['users'] = []
            data['required_pull_request_reviews']['bypass_pull_request_allowances']['teams'] = []
            for user in inputconfig['Allow specified actors to bypass pull request requirements']:
                if isinstance(user, str) and len(user) > 0:
                    if user == "${REPOTEAM}":
                        user = repoteam
                    if '/' in user:
                        data['required_pull_request_reviews']['bypass_pull_request_allowances']['teams'].append(user.split('/')[1])
                    else:
                        data['required_pull_request_reviews']['bypass_pull_request_allowances']['users'].append(user)
            if data['required_pull_request_reviews']['bypass_pull_request_allowances']['users'] == []:
                del data['required_pull_request_reviews']['bypass_pull_request_allowances']['users']
            if data['required_pull_request_reviews']['bypass_pull_request_allowances']['teams'] == []:
                del data['required_pull_request_reviews']['bypass_pull_request_allowances']['teams']
        else:
            data['required_pull_request_reviews'] = None

        data['restrictions'] = {}
        data['restrictions']['users'] = []
        data['restrictions']['teams'] = []
        for user in inputconfig['Restrict who can push to matching branches']:
            if isinstance(user, str) and len(user) > 0:
                if user == "${REPOTEAM}":
                    user = repoteam
                if '/' in user:
                    data['restrictions']['teams'].append(user.split('/')[1])
                else:
                    data['restrictions']['users'].append(user)
        if data['restrictions']['users'] == [] and data['restrictions']['teams'] == []:
            data['restrictions'] = None

        if inputconfig['Require linear history'] == True:
            data['required_linear_history'] = True
        else:
            data['required_linear_history'] = False

        if inputconfig['Allow force pushes'] == True:
            data['allow_force_pushes'] = True
        else:
            data['allow_force_pushes'] = False

        if inputconfig['Allow deletions'] == True:
            data['allow_deletions'] = True
        else:
            data['allow_deletions'] = False

        if inputconfig['Require conversation resolution before merging'] == True:
            data['required_conversation_resolution'] = True
        else:
            data['required_conversation_resolution'] = False

        if inputconfig['Require signed commits'] == True:
            data['required_signatures'] = True
        else:
            data['required_signatures'] = False




        try:
            r = requests.delete('https://api.github.com/repos/{}/{}/branches/{}/protection'.format(repo_owner, repo_name, branch), headers = {'Accept': 'application/vnd.github.v3+json'}, auth = (username, password))
            print(r.json())
        except:
            pass
        r = requests.put('https://api.github.com/repos/{}/{}/branches/{}/protection'.format(repo_owner, repo_name, branch), data = json.dumps(data), headers = {'Accept': 'application/vnd.github.v3+json'}, auth = (username, password))
        print(r.json())

print('Done!')