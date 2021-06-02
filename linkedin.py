from logging import raiseExceptions
import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def linkedin():

    # Credentials you get from registering a new application
    client_id = os.environ['LINKEDIN_CLIENT_ID']
    client_secret = os.environ['LINKEDIN_CLIENT_SECRET']

    # OAuth endpoints given in the LinkedIn API documentation
    authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'

    # scope (url encoded) https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication?context=linkedin/context#permission-types
    scope = 'r_liteprofile'
    # scope = 'r_liteprofile%20r_emailaddress%20w_member_social'

    from requests_oauthlib import OAuth2Session
    from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

    linkedin = OAuth2Session(client_id, scope=scope, redirect_uri='http://127.0.0.1')
    linkedin = linkedin_compliance_fix(linkedin)

    # Redirect user to LinkedIn for authorization
    authorization_url, state = linkedin.authorization_url(authorization_base_url)

    code = request.args.get('code')
    state = request.args.get('state')

    if code and state:
        full_url = "127.0.0.1{0}".format(request.full_path)
        print("FULL URL :::: {0} ".format(full_url))
        token = linkedin.fetch_token(token_url, code=code, include_client_id=True, client_secret=client_secret, authorization_response=full_url)
        print("TOKEN :::: {0}" .format(token))
        access_token = token['access_token']
        print("ACCESS TOKEN :::: {0}".format(access_token))
        p = profile(access_token)
        return p
    return render_template('index.html', authorization_url=authorization_url)



def profile(access_token):
    endpoint = 'https://api.linkedin.com/v2/me'
    headers = {"Authorization": "Bearer {0}".format(access_token)}
    r = requests.get(endpoint, headers=headers)
    return r.text