from enum import Enum


class RecommenderType(Enum):
    LongQuerySearchRecommender = 1
    PreprocessedQuerySearchRecommender = 2
    AnalyticsSearchRecommender = 3
    FacetQuestionRecommender = 4
