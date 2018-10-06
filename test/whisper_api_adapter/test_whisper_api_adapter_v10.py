import unittest
from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import whisper_response_to_suggestions

EXAMPLE_WHISPER_RESPONSE = '''
[
  {
  "title":"Goodbye GSA, Hello Intelligent Search in the Cloud - Coveo Blog",
  "uri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
  "printableUri":"https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/",
  "summary":null
  },
  {
  "title":"Interface ISearchEndpointOptions",
  "uri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
  "printableUri":"https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html",
  "summary":null
  },
  {
  "title":"What is your name?",
  "summary":null
  },
  {
  "title":"Did you try this?",
  "summary":null
  }
]
'''


class TestWhisperApiAdapterV10(unittest.TestCase):
    def test_convert_whisper_response_with_links_to_suggestions(self):
        suggestions = whisper_response_to_suggestions('10', EXAMPLE_WHISPER_RESPONSE)
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
