import os
import logging
from enum import Enum


class EventType(Enum):
    ADDED_TO_SPACE = 'ADDED_TO_SPACE'
    MESSAGE = 'MESSAGE'
    CARD_CLICKED = 'CARD_CLICKED'
    REMOVED_FROM_SPACE = 'REMOVED_FROM_SPACE'


class SpaceType(Enum):
    ROOM = 'ROOM'
    DIRECT_MESSAGE = 'DM'


class UserType(Enum):
    HUMAN = 'HUMAN'
    BOT = 'BOT'


class HangoutsChatHandler:
    SpaceType = SpaceType
    EventType = EventType
    ActionMethod = Enum

    def __init__(self, logger=None, parameters=None, debug=False):
        if parameters is None:
            self.parameters = os.environ
        if logger is None:
            logger = logging.getLogger(__name__)
        self.log = logger
        self.debug = debug

    def handle_chat_event(self, event, sent_asynchronously=False):
        try:
            self.sent_asynchronously = sent_asynchronously
            event_type = EventType(event['type'])
            space_type = SpaceType(event['space']['type'])
            if event_type == EventType.ADDED_TO_SPACE:
                return self.handle_added_to_space(space_type, event)
            elif event_type == EventType.REMOVED_FROM_SPACE:
                return self.handle_removed_from_space(space_type, event)
            elif event_type == EventType.CARD_CLICKED:
                action_method = self.ActionMethod(event['action']['actionMethodName'])
                action_parameters = self._parse_action_parameters(event['action']['parameters'])
                return self.handle_card_clicked(action_method, action_parameters, event)
            elif event_type == EventType.MESSAGE:
                message = event['message']['text']
                return self.handle_message(message, event)
        except Exception as e:
            logging.exception('Error handling chat event')
            return self.handle_exception(e, event)

    def handle_exception(self, e, event=None):
        if self.debug:
            return {'text': str(e)}

    def handle_added_to_space(self, space_type, event):
        pass

    def handle_message(self, message, event):
        pass

    def handle_card_clicked(self, action_method, action_parameters, event):
        pass

    def handle_removed_from_space(self, space_type, event):
        pass

    def _parse_action_parameters(self, parameters):
        parsed_parameters = {}
        for p in parameters:
            key = p['key']
            value = p['value']
            parsed_parameters[key] = value
        return parsed_parameters
