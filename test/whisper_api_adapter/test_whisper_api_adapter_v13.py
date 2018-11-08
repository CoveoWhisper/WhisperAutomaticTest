import unittest
from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import whisper_response_to_suggestions

EXAMPLE_WHISPER_RESPONSE = '''
{
    "questions": [
        {
            "id": "fad778fc-f1ad-4fb5-9b55-82aa8718ad97",
            "text": "What @objecttype is it? Is it Blog, Answers, Video ?"
        },
        {
            "id": "d86f2789-28fa-49b1-a9d5-a8268bf8cc27",
            "text": "What @filetype is it? Is it YouTubeVideo, SalesforceItem, html ?"
        }
    ],
    "suggestedDocuments": [
        {
            "id": "270ece78-9c25-4a83-a341-f57863e1877b",
            "title": "Accessing the Coveo for Sitecore API",
            "uri": "https://docs.coveo.com/en/1514/",
            "printableUri": "https://docs.coveo.com/en/1514/",
            "summary": null,
            "excerpt": "Accessing the Coveo for Sitecore API ... Coveo for Sitecore offers APIs to configure the solution or perform actions through code. ... This article describes which service APIs are available and ho..."
        },
        {
            "id": "141c34f8-ec0a-44f9-beab-cbd20f02ce18",
            "title": "Coveo Webinar: Enhance your eCommerce experience with machine learning",
            "uri": "https://www.youtube.com/watch?v=7b8uO818FJg",
            "printableUri": "https://www.youtube.com/watch?v=7b8uO818FJg",
            "summary": null,
            "excerpt": "Every customer expects the personalization of Amazon and the superior customer service of a brick-and-mortar store. ... But how do you create this experience without developing your own machine lea..."
        }
    ]
}
'''


class TestWhisperApiAdapterV13(unittest.TestCase):
    def test_convert_whisper_response_to_suggestions(self):
        suggestions = whisper_response_to_suggestions('13', EXAMPLE_WHISPER_RESPONSE)
        self.assertEquals(4, len(suggestions))
        self.assertEquals('link', suggestions[0].get_type())
        self.assertEquals('link', suggestions[1].get_type())
        self.assertEquals('question', suggestions[2].get_type())
        self.assertEquals('question', suggestions[3].get_type())
        self.assertEquals(
            'https://docs.coveo.com/en/1514/',
            suggestions[0].get_data()
        )
        self.assertEquals(
            'https://www.youtube.com/watch?v=7b8uO818FJg',
            suggestions[1].get_data()
        )
        self.assertEquals(
            'What @objecttype is it? Is it Blog, Answers, Video ?',
            suggestions[2].get_data()
        )
        self.assertEquals(
            'What @filetype is it? Is it YouTubeVideo, SalesforceItem, html ?',
            suggestions[3].get_data()
        )
