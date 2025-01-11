# MaaZ Lab


## Installation


```bash
cd ../ansible
# before install keycloak review and change variable
cat ansible/inventories/group_vars/keycloak.yml

# deploy keycloak service with ansible
ansible-playbook -i inventories/host.yaml playbook/keycloak.yaml --tags=keycloak-installation
```

## Configuration

- Create Realm MaaZ
    - Top left selction menu
    - Create Realm
    - Realm name: MaaZ
- Create group students in MaaZ Realm
    - Mange
    - Groups
    - Create group
    - name: students
- Enable username 
  - Configure
  - Realm settings
  - Login tab
  - User info settings
  - Edit username : Off
  - Edit Email as username: Off
  - and check that you can set username while creating it. not just email.
- Create user maaz
  - Manage
  - Users
  - set username
  - Join to students group
  - Set password for user from credentials tab --> set password --> temporary : Off ---> Save user

## Integration with Gitlab

`Step1:` Create a client for gitlab on keycloak

Example:
- **Client type:** OpenID Connect
- **Client ID:** gitlab
- **Name:** gitlab (Not necessary) 
- **Description:** keycloak client for gitlab (Not necessary)
- **Always display in UI:** It's Optional. If you enable this option, when the user logs in, he will see this client on his page.
- **Client authentication:** On
- **authorization:** Off
- **Authentication flow:** standard flow: yes others: no
- **Root URL:** https://git.maaz.ir
- **Home URL:** https://git.maaz.ir
- **Valid redirect URIs:** https://git.maaz.ir/users/auth/openid_connect/callback
- **Valid post logout redirect URIs:** 
- **Web origins:** https://git.maaz.ir
Next 
Check all of these:

| Option | Value |
| ------ | ------ |
| Client ID | gitlab |
| Name | gitlab |
| Root URL | https://git.maaz.ir|
| Home URL | https://git.maaz.ir|
|Valid redirec URIs| https://git.maaz.ir/users/auth/openid_connect/callback |
|Web origins| https|//git.maaz.ir |
|Admin URL| https://git.maaz.ir |
|Client authentication| On |
|Authorization| Off |
|Standard flow| yes |
|Direct access grants| no |
|Implicit flow| no |
|Service accounts roles| no |
|OAuth 2.0 Device Authorization Grant| no |
|OIDC CIBA Grant| no |
|Front channel logout| On |
|Backchannel logout session required| On |
### Client Secret is on Credentials tab of client.

`Step2:` Add these lines to gitlab compose file:

```bash
        # Keycloak
        gitlab_rails['omniauth_allow_single_sign_on'] = ['openid_connect']
        gitlab_rails['omniauth_block_auto_created_users'] = true
        gitlab_rails['omniauth_auto_link_user'] = ['openid_connect']
        gitlab_rails['omniauth_providers'] = [
          {
            name: "openid_connect", # do not change this parameter
            label: "Keycloak", # optional label for login button, defaults to "Openid Connect"
            args: {
              name: "openid_connect",
              scope: ["openid", "profile", "email"],
              response_type: "code",
              issuer:  "https://auth.maaz.ir/realms/MaaZ",
              client_auth_method: "query",
              discovery: true,
              uid_field: "preferred_username",
              pkce: true,
              client_options: {
                identifier: "gitlab",
                secret: "******************************",
                redirect_uri: "https://git.maaz.ir/users/auth/openid_connect/callback"
              }
            }
          }
        ]
```

## Integration with MinIo
`Step1:`  Create a client for minio on keycloak

Example:
- **Client type:** OpenID Connect
- **Client ID:** minio_client_id
- **Name:** minio_client_name (Not necessary) 
- **Description:** keycloak client for minio (Not necessary)
- **Always display in UI:** It's Optional. If you enable this option, when the user logs in, he will see this client on his page.
- **Client authentication:** On
- **authorization:** Off
- **Authentication flow:** standard flow: yes others: no
- **Root URL:** https://object.maaz.ir
- **Home URL:** https://object.maaz.ir
- **Valid redirect URIs:** https://object.maaz.ir/*
- **Valid post logout redirect URIs:** 
- **Web origins:** https://object.maaz.ir

Next check all of these:
| Option | Value |
| ------ | ------ |
| Client ID | minio_client_id |
| Name | minio_client_name |
| Root URL | https://object.maaz.ir |
| Home URL | https://object.maaz.ir |
|Valid redirec URIs| https://object.maaz.ir/* |
|Web origins| https://object.maaz.ir |
|Admin URL| https://object.maaz.ir |
|Client authentication| On |
|Authorization| Off |
|Standard flow| yes |
|Direct access grants| no |
|Implicit flow| no |
|Service accounts roles| no |
|OAuth 2.0 Device Authorization Grant| no |
|OIDC CIBA Grant| no |
|Front channel logout| On |
|Backchannel logout session required| On |

`Step2:` Set this on students group Attributes
| Key | Value |
| ------ | ------ |
| policy | readonly |


`Step3:` Create Client Scope

Example:
| Option | Value |
| ------ | ------ |
| Name | minio_client_scope |
| Description |  |
| Type |  Default |
| Display on consent screen | On |
| Include in token scope | On |

`Step4:` Mapper

Example:
| Option | Value |
| ------ | ------ |
| Mapper type | User Attribute |
| Name |  minio-policy-mapper
| User Attribute | policy |
| Token Claim Name | policy |
| Claim JSON Type | String |
| Add to ID token | On |
| Add to access token | On |
|Add to lightweight access token | Off |
| Add to userinfo | On |
| Add to token introspection | On |
| Multivalued | On |
| Aggregate attribute values | Off | 

then add it to minio_client_id

`Step5:` From Panel https://object.maaz.ir 
> Administration

> Identity

> OpenID

> Create Configuration

Example:

| Option | Value |
| ------ | ------ |
| Config URL | https://auth.maaz.ir/realms/MaaZ/.well-known/openid-configuration |
| Client ID | minio_client_id |
| Client Secret | ****************************** |
| Claim Name | |
| Display Name | MaaZ |
| Claim Prefix | |
| Scopes | openid |
| Redirect URI | |
| Role Policy | readonly |
| Claim User Info | Disabled |
| Redirect URI Dynamic | Enabled |
### Client Secret is on Credentials tab of client.
For Separate Access to buckets due to student group in Keycloak change the Configuration like example bellow and make sure that policies in Minio have the same name like groups in Keycloak:

Example:

| Option | Value |
| ------ | ------ |
| Config URL | https://auth.maaz.ir/realms/MaaZ/.well-known/openid-configuration |
| Client ID | minio |
| Client Secret | ****************************** |
| Claim Name | |
| Display Name | MaaZ |
| Claim Prefix | |
| Scopes | openid |
| Redirect URI | |
| Role Policy | readonly |
| Claim User Info | Enabled |
| Redirect URI Dynamic | Disabled |


## Integration with Grafana
`Step1:`  Create a client for grafana on keycloak

Example:
- **Client type:** OpenID Connect
- **Client ID:** grafana-oauth
- **Name:** grafana (Not necessary) 
- **Description:** keycloak client for grafana (Not necessary)
- **Always display in UI:** It's Optional. If you enable this option, when the user logs in, he will see this client on his page.
- **Client authentication:** On
- **authorization:** Off
- **Authentication flow:** standard flow: yes Direct access grants: yes others: no
- **Root URL:** https://grafana.observability.maaz.ir
- **Home URL:** https://grafana.observability.maaz.ir
- **Valid redirect URIs:** https://grafana.observability.maaz.ir/login/generic_oauth/*
- **Valid post logout redirect URIs:** 
- **Web origins:** https://grafana.observability.maaz.ir
Next 
Check all of these:

| Option | Value |
| ------ | ------ |
| Client ID | grafana-oauth |
| Name | grafana-oauth |
| Root URL | https://grafana.observability.maaz.ir |
| Home URL | https://grafana.observability.maaz.ir |
|Valid redirec URIs| https://grafana.observability.maaz.ir/login/generic_oauth/* |
|Web origins| https://grafana.observability.maaz.ir |
|Admin URL| https://grafana.observability.maaz.ir |
|Client authentication| On |
|Authorization| Off |
|Standard flow| yes |
|Direct access grants| no |
|Implicit flow| no |
|Service accounts roles| no |
|OAuth 2.0 Device Authorization Grant| no |
|OIDC CIBA Grant| no |
|Front channel logout| On |
|Backchannel logout session required| On |

`Step2:` Add these lines to grafana compose file:
```bash
    volumes:
      - ./grafana_config.ini:/etc/grafana/grafana.ini
    environment:
      - GF_PATHS_CONFIG=/etc/grafana/grafana.ini
      - GF_SERVER_ROOT_URL=https://grafana.observability.maaz.ir
```
`Step3:` Put this in grafana_config.ini file:
```bash
[auth.generic_oauth]
enabled = true
name = Keycloak-OAuth
allow_sign_up = true
client_id = grafana-oauth
client_secret = ******************************
scopes = openid email profile offline_access roles
email_attribute_path = email
login_attribute_path = username
name_attribute_path = full_name
auth_url = https://auth.maaz.ir/realms/MaaZ/protocol/openid-connect/auth
token_url = https://auth.maaz.ir/realms/MaaZ/protocol/openid-connect/token
api_url = https://auth.maaz.ir/realms/MaaZ/protocol/openid-connect/userinfo
role_attribute_path = contains(roles[*], 'admin') && 'Admin' || contains(roles[*], 'editor') && 'Editor' || 'Viewer'
```

## Integration with kc-ssh-pam
`Step1:` Keycloak Cleint Creation

Example:
- **Client type:** OpenID Connect
- **Client ID:** ssh-login
- **Name:** ssh-login (Not necessary) 
- **Description:** keycloak client for ssh (Not necessary)
- **Always display in UI:** It's Optional. If you enable this option, when the user logs in, he will see this client on his page.
- **Client authentication:** On
- **authorization:** Off
- **Authentication flow:** standard flow: yes Direct access grants: yes others: no
- **Root URL:** 
- **Home URL:** 
- **Valid redirect URIs:** urn:ietf:wg:oauth:2.0:oob
- **Valid post logout redirect URIs:** 
- **Web origins:** 
Next 
Check all of these:

| Option | Value |
| ------ | ------ |
| Client ID | ssh-login |
| Name | ssh-login |
| Root URL |    |
| Home URL |    |
|Valid redirec URIs| urn:ietf:wg:oauth:2.0:oob |
|Web origins|    |
|Admin URL|    |
|Client authentication| On |
|Authorization| Off |
|Standard flow| yes |
|Direct access grants| no |
|Implicit flow| no |
|Service accounts roles| no |
|OAuth 2.0 Device Authorization Grant| no |
|OIDC CIBA Grant| no |
|Front channel logout| On |
|Backchannel logout session required| On |

`Step2:` Download and install kc-ssh-pam
```bash
wget https://github.com/kha7iq/kc-ssh-pam/releases/download/v0.1.4/kc-ssh-pam_amd64.deb
sudo dpkg -i kc-ssh-pam_amd64.deb
```
`Step3:` Change /opt/kc-ssh-pam/config.toml

Example:
```bash
realm = "test"
endpoint = "https://auth.maaz.ir"
clientid = "ssh-login"
clientsecret = "******************************"
clientscope = "openid"
```

`Step4:` Edit /etc/pam.d/sshd and add the following at the top of file
```bash
auth sufficient pam_exec.so expose_authtok      log=/var/log/kc-ssh-pam.log     /opt/kc-ssh-pam/kc-ssh-pam
```

# Configure SMTP Keycloak
 
`Step1:` Configure --> In Realm Settings --> Email tab

Example:

check all of these:
| Option | Value |
| ------ | ------ |
| From (reply-to) | m.ahmadizarei@gmail.com |
| From display name |  |
| Reply to |  |
| Reply to display name  |  |
| Envelope from |  |
| Host| smtp.gmail.com |
| Port | 587  |
| Enable SSK | No |
| Enable StartTLS | Yes |
| Authentication | Enabled |
| Username | m.ahmadizarei@gmail.com |
`Step2:` First give a apppassword from your google acount https://myaccount.google.com/apppasswords  
| Password | put the apppass here |

`Step3:` Save! Then set email for your user and then Test Connection.


## Links
| Tools | Links |
| ------ | ------ |
| Gitlab | [configure-keycloak](https://docs.gitlab.com/ee/administration/auth/oidc.html#configure-keycloak) |
| MinIo | [Configure MinIO for Authentication using Keycloak](https://min.io/docs/minio/container/operations/external-iam/configure-keycloak-identity-management.html) |
| Grafana | [Configure Keycloak OAuth2 authentication](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/keycloak/#configure-keycloak-oauth2-authentication) |
| SSH | [kc-ssh-pam](https://github.com/kha7iq/kc-ssh-pam) |
| Keycloak | [Open Source Identity and Access Management](https://www.keycloak.org/) |

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>


   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
