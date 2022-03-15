# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot_unittest import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new', 'object': {
        'message': {'date': 1637726776, 'from_id': 566982261, 'id': 453, 'out': 0, 'peer_id': 566982261,
                    'text': 'привет', 'attachments': [], 'conversation_message_id': 54, 'fwd_messages': [],
                    'important': False, 'is_hidden': False, 'random_id': 0}, 'client_info': {
            'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe',
                               'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True,
            'lang_id': 0}}, 'group_id': 208757128, 'event_id': '50721f208c8e4edf1e4ffbcb6f0a2f39cd994c2d'}

    def test_ok(self):
        count = 5
        obj = {'a': 1}
        events = [{}] * count  # [obj,obj,...]
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot_refactoring.vk_api.VkApi'):
            with patch('bot_refactoring.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        with patch('bot_refactoring.vk_api.VkApi'):
            with patch('bot_refactoring.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock

                bot.on_event(event)
        send_mock.assert_called_once_with(message=self.RAW_EVENT['object']['message']['text'],
                                          random_id=ANY,
                                          peer_id=self.RAW_EVENT['object']['message']['peer_id'])
