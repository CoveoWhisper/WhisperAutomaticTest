import unittest
from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import whisper_response_to_suggestions

EXAMPLE_WHISPER_RESPONSE = '''
{
    "questions": [
        {
        "title":"What is your name?",
        "summary":null
        },
        {
        "title":"Did you try this?",
        "summary":null
        }
    ],
    "suggestedDocuments": [
        {
        "title":"Goodbye GSA, Hello Intelligent Search in the Cloud - Coveo Blog",
        "uri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
        "printableUri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
        "summary":null,
        "excerpt": "Here is some excerpt"
        },
        {
        "title":"Interface ISearchEndpointOptions",
        "uri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
        "printableUri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
        "summary":null,
        "excerpt": "Here is another excerpt"
        }
    ]
}
'''

EXAMPLE_WHISPER_RESPONSE_ONLY_QUESTIONS = '''
{
    "questions": [
        {
        "title":"What is your name?",
        "summary":null
        },
        {
        "title":"Did you try this?",
        "summary":null
        }
    ],
    "suggestedDocuments":null
}
'''

EXAMPLE_WHISPER_RESPONSE_ONLY_LINKS = '''
{
    "questions":null,
    "suggestedDocuments": [
        {
        "title":"Goodbye GSA, Hello Intelligent Search in the Cloud - Coveo Blog",
        "uri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
        "printableUri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
        "summary":null,
        "excerpt": "Here is some excerpt"
        },
        {
        "title":"Interface ISearchEndpointOptions",
        "uri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
        "printableUri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
        "summary":null,
        "excerpt": "Here is another excerpt"
        }
    ]
}
'''


class TestWhisperApiAdapterV11(unittest.TestCase):
    def test_convert_whisper_response_to_suggestions(self):
        suggestions = whisper_response_to_suggestions('11', EXAMPLE_WHISPER_RESPONSE)
        self.assertEquals(4, len(suggestions))
        self.assertEquals('link', suggestions[0].get_type())
        self.assertEquals('link', suggestions[1].get_type())
        self.assertEquals('question', suggestions[2].get_type())
        self.assertEquals('question', suggestions[3].get_type())
        self.assertEquals(
            'https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/',
            suggestions[0].get_data()
        )
        self.assertEquals(
            'https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html',
            suggestions[1].get_data()
        )
        self.assertEquals(
            'What is your name?',
            suggestions[2].get_data()
        )
        self.assertEquals(
            'Did you try this?',
            suggestions[3].get_data()
        )

    def test_convert_whisper_response_to_suggestions_with_only_questions(self):
        suggestions = whisper_response_to_suggestions('11', EXAMPLE_WHISPER_RESPONSE_ONLY_QUESTIONS)
        self.assertEquals(2, len(suggestions))
        self.assertEquals('question', suggestions[0].get_type())
        self.assertEquals('question', suggestions[1].get_type())
        self.assertEquals(
            'What is your name?',
            suggestions[0].get_data()
        )
        self.assertEquals(
            'Did you try this?',
            suggestions[1].get_data()
        )

    def test_convert_whisper_response_to_suggestions_with_only_links(self):
        suggestions = whisper_response_to_suggestions('11', EXAMPLE_WHISPER_RESPONSE_ONLY_LINKS)
        self.assertEquals(2, len(suggestions))
        self.assertEquals('link', suggestions[0].get_type())
        self.assertEquals('link', suggestions[1].get_type())
        self.assertEquals(
            'https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/',
            suggestions[0].get_data()
        )
        self.assertEquals(
            'https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html',
            suggestions[1].get_data()
        )
