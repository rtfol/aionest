# -*- coding: utf-8 -*-

"""Main module."""
import logging
import uuid
from datetime import datetime, timedelta

import aiohttp
from aiohttp_sse_client import client as sse_client


ACCESS_TOKEN_URL = 'https://api.home.nest.com/oauth2/access_token'
AUTHORIZE_URL = 'https://home.nest.com/login/oauth2?client_id={0}&state={1}'
API_URL = 'https://developer-api.nest.com'
LOGIN_URL = 'https://home.nest.com/user/login'

_LOGGER = logging.getLogger(__name__)


class NestApi(object):
    """Represent Nest API."""
    def __init__(self, product_id, 
                 access_token=None,
                 access_token_expires_at=None,
                 session=None):
        """Initialize Nest API.
         
        :param product_id: Product ID
        :param access_token: Access Token
        :param access_token_expires_at: Access Token will expires at
        :param session: aiohttp Client Session
        """
        self._product_id = product_id
        self._access_token = access_token
        self._need_close_session = session is None
        self._session = session
        self._event_stream = None
        self._auth_state = None
        self._access_token_expires_at = access_token_expires_at
         
    def get_authorize_url(self, state=None):
        """Generate authorize URL."""
        self._auth_state = state or str(uuid.uuid4())
        return AUTHORIZE_URL.format(self._product_id, self._auth_state)

    async def authenticate(self, pin, product_secret, state=None):
        """Authenticate via given pin, product id and secret.
        
        return (access_token, expires_in) if authentication passed
        return None if failed
        """
        if state is not None and state != self._auth_state:
            raise ValueError('state is not correct')

        if self._session is None:
            self._session = aiohttp.ClientSession()
        if self._session.closed:
            raise ConnectionRefusedError('session is closed')

        data = {'client_id': self._product_id,
                'client_secret': product_secret,
                'code': pin,
                'grant_type': 'authorization_code'}
        async with self._session.post(
            ACCESS_TOKEN_URL, data=data        
        ) as response:
            result = await response.json()
            self._access_token = result['access_token']
            self._access_token_expires_at = datetime.utcnow() + timedelta(
                seconds=int(result['expires_in'])
            )
            return self._access_token, self._access_token_expires_at
        
    def __aiter__(self):
        """Return."""
        return self

    async def connect(self):
        """Connect to Nest Stream API."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        if self._session.closed:
            raise ConnectionRefusedError('session is closed')

        if (self._access_token_expires_at is not None and
                self._access_token_expires_at < datetime.utcnow()):
            raise ConnectionRefusedError('access token is expired')

        self._event_stream = sse_client.EventSource(
            API_URL + '/',
            headers={'Authorization': 'Bearer {}'.format(self._access_token)},
            session=self._session
        )
        await self._event_stream.connect()
        
    async def close(self):
        """Close connection."""
        if self._event_stream is not None:
            await self._event_stream.close()
        if self._need_close_session and self._session is not None:
            await self._session.close()

    async def __anext__(self):
        """Process events."""
        async for event in self._event_stream:
            event_type = event.type
            if event_type == 'open' or event_type == 'keep-alive':
                continue
            elif event_type == 'auth_revoked':
                raise ValueError('auth_revoked')
            elif event_type == 'error':
                raise ValueError(event.data)
            elif event_type == 'put':
                return event.data
