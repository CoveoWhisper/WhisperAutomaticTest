from enum import Enum, auto


class RecommenderType(Enum):
    LongQuerySearch = auto()
    PreprocessedQuerySearch = auto()
    AnalyticsSearch = auto()
    FacetQuestion = auto()
    NearestDocuments = auto()
