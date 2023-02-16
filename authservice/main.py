# Copyright 2022. Huawei Technologies Co., Ltd. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import asyncio

from agconnect.auth_server import AGCAuthException
from agconnect.auth_server import AGCAuth
from agconnect.common_server import logger
from agconnect.common_server import logging_config
from agconnect.common_server import AGCClient
from agconnect.common_server import CredentialParser

credential = CredentialParser.to_credential("[PATH]/agc-apiclient-xxx-xxx.json")
your_client_name = "abc"
AGCClient.initialize(your_client_name, credential, "CN")
authService = AGCAuth.get_instance(your_client_name)

# get privateKey and publicKey
keypair = authService.generate_keys()
print(f"privateKey: {keypair.get_private_key()}")
print(f"publicKey: {keypair.get_public_key()}")

# do sign and get jwt
jwt = authService.sign("uid", "userName", "url", keypair.get_private_key())
logger.info(f"generate jwt: {jwt.get_token()}")
logger.info(f"generate jwt expiration time: {jwt.get_expiration_time()}")

loop = asyncio.get_event_loop()

try:
    # export user info to file:[PATH]/xxx.json
    loop.run_until_complete(authService.export_user_data("./resources"))
except Exception as e:
    logger.error(e)

try:
    # import user from file:[PATH]/yyy.json
    loop.run_until_complete(authService.import_user_data("./yyy.json"))
except AGCAuthException as e:
    logger.error(e.get_message())

try:
    # verify access token
    loop.run_until_complete(authService.verify_access_token("your access token", False))
except AGCAuthException as e:
    logger.error(e.get_message())

try:
    # revoke token of uid:a uid
    loop.run_until_complete(authService.revoke_refresh_tokens("a uid"))
except AGCAuthException as e:
    logger.error(e.get_message())
