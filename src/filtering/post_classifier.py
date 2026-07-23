class PostClassifier:

    CATEGORY_RULES = {

        "Entertainment": [

            "movie",
            "film",
            "actor",
            "actress",
            "album",
            "song",
            "teaser",
            "trailer",
            "netflix",
            "hollywood",
            "bollywood",
            "celebrity",
            "married",
            "dating",
            "wedding",
            "release"
        ],

        "Sports": [

            "cricket",
            "football",
            "match",
            "world cup",
            "ipl",
            "fifa",
            "nba",
            "goal",
            "runs",
            "wicket",
            "team",
            "rcb",
            "india",
            "pakistan"
        ],

        "Politics": [

            "minister",
            "government",
            "parliament",
            "court",
            "election",
            "supreme",
            "police",
            "commission",
            "law"
        ],

        "Technology": [

            "ai",
            "chatgpt",
            "openai",
            "google",
            "apple",
            "microsoft",
            "startup",
            "software",
            "technology"
        ],

        "Podcast": [

            "podcast",
            "episode",
            "conversation",
            "interview"
        ],

        "Brand": [

            "nike",
            "adidas",
            "zara",
            "alipay",
            "heinz",
            "campaign",
            "brand",
            "launch"
        ],

        "Lifestyle": [

            "travel",
            "food",
            "fashion",
            "fitness",
            "makeup",
            "beauty"
        ]
    }

    @staticmethod
    def classify(caption: str):

        if not caption:

            return {

                "category": "Unknown",

                "confidence": 0.0
            }

        text = caption.lower()

        scores = {}

        for category, words in PostClassifier.CATEGORY_RULES.items():

            score = 0

            for word in words:

                if word in text:

                    score += 1

            scores[category] = score

        best_category = max(

            scores,

            key=scores.get
        )

        confidence = (

            scores[best_category]

            /

            max(

                len(

                    PostClassifier.CATEGORY_RULES[
                        best_category
                    ]
                ),

                1
            )
        )

        if scores[best_category] == 0:

            best_category = "General"

            confidence = 0.2

        return {

            "category": best_category,

            "confidence": round(

                confidence,

                2
            )
        }