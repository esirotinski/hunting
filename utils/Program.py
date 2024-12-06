import os
from dotenv import load_dotenv
from typing import Set
from utils.requests_sessions import get_h1_requests_session
load_dotenv()


class Program:
    def __init__(self, handle: str, automated_tests_allowed=True | False) -> None:
        self.handle = handle.lower()
        self.h1_session = get_h1_requests_session()
        self.handle_url = os.getenv("H1_BASE_URL") + f"{self.handle}"
        self.automated_tests_allowed = automated_tests_allowed

    def get_scope_assets(self, eligible_for_submission=True | False, asset_type=None) -> Set:
        in_scope_attributes = set()

        if asset_type not in ('URL', 'WILDCARD'):
            raise ValueError("asset_type is required: URL or WILDCARD")

        try:
            response = self.h1_session.get(url=self.handle_url, timeout=(15, 15))
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Error", e)
        else:
            response = response.json()
            if response['attributes']['submission_state'] == 'open':
                relationships = response['relationships']
                for scope in relationships['structured_scopes']['data']:
                    attributes = scope['attributes']
                    if (attributes['eligible_for_submission'] is eligible_for_submission
                            and attributes['asset_type'] == asset_type):
                        in_scope_attributes.add(attributes['asset_identifier'])
                return in_scope_attributes
            else:
                raise Exception(f'Submission closed for {self.handle}')

