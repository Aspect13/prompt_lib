from datetime import datetime, timedelta

from pylon.core.tools import web, log

from tools import rpc_tools, db, VaultClient, auth, api_tools

from ..models.pd.legacy.config_pd import ModelsConfig, TokenPD

TOKEN_NAME = 'ai_token'


class RPC:
    @web.rpc('prompts_get_config', 'get_config')
    def get_config(self, project_id: int, user_id: int, **kwargs) -> ModelsConfig:
        secrets = VaultClient(project_id).get_all_secrets()
        url = ''.join([
            secrets['galloper_url'],
            secrets.get('ai_project_api_url', '/api/v1')
        ])

        all_tokens = auth.list_tokens(
            user_id=user_id,
            name=TOKEN_NAME
        )
        try:
            token = all_tokens[0]
            # token_encoded, expires = token.encoded, token.expires.isoformat(timespec='seconds')
            # log.info(f'config.token {token}')
        except IndexError:
            # token_encoded = expires = None
            token = None

        ai_integrations = self.context.rpc_manager.call.integrations_get_all_integrations_by_section(
            project_id=project_id,
            section_name='ai'
        )

        personal_project_id = self.context.rpc_manager.timeout(2).projects_get_personal_project_id(user_id)

        data = ModelsConfig(
            url=url,
            project_id=project_id,
            personal_project_id=personal_project_id,
            token=token,
            integrations=[i.dict(include={'id', 'uid', 'name', 'is_default', 'config'}) for i in ai_integrations]
        )
        return data

    @web.rpc('prompts_regenerate_token', 'regenerate_token')
    def regenerate_token(self, user_id: int) -> TokenPD:
        all_tokens = auth.list_tokens(
            user_id=user_id,
            name=TOKEN_NAME
        )
        for i in all_tokens:
            auth.delete_token(token_id=i['id'])

        expires = datetime.now() + timedelta(days=30)
        token_id = auth.add_token(
            user_id=user_id,
            name=TOKEN_NAME,
            expires=expires,
        )
        token = TokenPD(
            id=token_id,
            user_id=user_id,
            expires=expires,
            name=TOKEN_NAME
        )

        return token
