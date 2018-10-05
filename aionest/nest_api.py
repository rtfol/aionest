# -*- coding: utf-8 -*-

"""Main module."""
import logging
import uuid

import aiohttp
from aiohttp_sse_client import client as sse_client


ACCESS_TOKEN_URL = 'https://api.home.nest.com/oauth2/access_token'
AUTHORIZE_URL = 'https://home.nest.com/login/oauth2?client_id={0}&state={1}'
API_URL = 'https://developer-api.nest.com'
LOGIN_URL = 'https://home.nest.com/user/login'

_LOGGER = logging.getLogger(__name__)


class NestApi(object)
    """Represent Nest API."""
    def __init__(self, product_id=None, access_token=None, web_session=None):
         """Initialize Nest API.
         
         :param product_id: Product ID
         :param access_token: Access Token
         :param web_sesion: aiohttp Client Session
         """
         self._product_id = product_id
         self._product_secret = product_secret
         self._access_token = access_token
         self._need_close_session = web_session is None
         self._web_session = web_session or aiohttp.ClientSession()
         self._event_stream = None
         
    def get_authorize_url(self, state=None):
        """Generate authorize URL."""
        self._auth_state = state or str(uuid.uuid4())
        return AUTHORIZE_URL.format(self._client_id, self._auth_state)

    async def authenticate(self, pin, product_secret, state=None):
        """Authenticate via given pin, product id and secret.
        
        return (access_token, expires_in) if authentication passed
        return None if failed
        """
        if state is not None and state != self._state:
            raise ValueError('state is not correct')
            
        data = {'client_id': self._product_id,
                'client_secret': product_secret,
                'code': pin,
                'grant_type': 'authorization_code'}
        async with self._web_session.post(
            ACCESS_TOKEN_URL, data=data        
        ) as response:
            result = await response.json()
            return result['access_token'], int(result['expires_in'])
        
    def __aiter__(self):
        """Return."""
        return self

    async def connect(self):
        """Conenct to Nest Stream API."""
        self._event_stream = sse_client.EventSource(
            API_URL + '/', headers={'Authorization': 'Bearer {}'.format(
                self._access_token)})
        await self._event_stream.connect()
        
    async def __anext__(self):
        """Process events."""
        async for event in self._event_stream:
            event_type = event.event
            if event_type == 'open' or event_type == 'keep-alive':
                continue
            elif event_type == 'auth_revoked':
                raise ValueError('auth_revoked')
            elif event_type == 'error':
                raise ValueError(event.data)
            elif event_type == 'put':
                queue.appendleft(json.loads(event.data))
                return event.data
