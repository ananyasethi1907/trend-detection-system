class TopicRanker:

    GENERIC_WORDS = {

        "video",
        "post",
        "photo",
        "picture",
        "caption",
        "bio",
        "instagram",
        "comment",
        "comments",
        "people",
        "person",
        "makers",
        "official",
        "team",
        "group",
        "player"

    }

    EVENT_WORDS = {

        "marriage",
        "married",
        "wedding",
        "release",
        "released",
        "launch",
        "launched",
        "championship",
        "world cup",
        "joins",
        "joined",
        "wins",
        "won",
        "beats",
        "beat",
        "debut",
        "election",
        "death",
        "dies"

    }

    CONNECTOR_WORDS = {

        "vs",
        "v",
        "at",
        "in",
        "for",
        "with"

    }

    # spaCy frequently tags zodiac sign names as PERSON (they're
    # capitalized proper-noun-shaped words), so they survive entity
    # extraction and can combine into candidates like "Leo, Aquarius"
    # that score well on entity coverage despite not being a real topic.
    # A candidate made ENTIRELY of zodiac words is astrology noise, not
    # a story -- penalize it outright rather than trying to strip zodiac
    # words from entity extraction generally, which would also break
    # legitimate topics like "Leo DiCaprio".
    ZODIAC_WORDS = {

        "leo",
        "aquarius",
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "pisces"

    }

    @staticmethod
    def score(
        candidate,
        entities
    ):

        score = 0

        candidate = candidate.strip()

        if not candidate:

            return score

        words = candidate.split()

        lower = candidate.lower()

        ###################################################
        # Zodiac-only combination
        ###################################################

        stripped_words = [

            word.strip(",").lower()

            for word in words

        ]

        if stripped_words and all(

            word in TopicRanker.ZODIAC_WORDS

            for word in stripped_words

        ):

            return -100

        ###################################################
        # Length
        ###################################################

        if 2 <= len(words) <= 5:

            score += 20

        elif len(words) == 1:

            score += 8

        else:

            score -= 20

        ###################################################
        # Entity Coverage
        ###################################################

        matched_entities = 0

        for entity in entities:

            entity_text = entity[0].lower()

            confidence = 1.0

            if len(entity) >= 4:

                confidence = entity[3]

            if entity_text in lower:

                matched_entities += 1

                score += int(25 * confidence)

        ###################################################
        # Coverage Bonus
        ###################################################

        if matched_entities >= 2:

            score += 15

        if matched_entities >= 3:

            score += 10

        ###################################################
        # Event Bonus
        ###################################################

        contains_event = False

        for event in TopicRanker.EVENT_WORDS:

            if event in lower:

                contains_event = True

                score += 20

        ###################################################
        # Connector Bonus
        ###################################################

        for connector in TopicRanker.CONNECTOR_WORDS:

            if f" {connector} " in f" {lower} ":

                score += 10

                break

        ###################################################
        # Context Bonus
        ###################################################

        if matched_entities > 0 and contains_event:

            score += 20

        ###################################################
        # Specificity Bonus
        ###################################################

        meaningful_words = 0

        for word in words:

            if word.lower() not in TopicRanker.GENERIC_WORDS:

                meaningful_words += 1

        if meaningful_words >= 3:

            score += 10

        ###################################################
        # Generic Penalty
        ###################################################

        generic_count = 0

        for word in TopicRanker.GENERIC_WORDS:

            if word in lower:

                generic_count += 1

        if generic_count > 0:

            if matched_entities == 0:

                score -= generic_count * 15

            else:

                score -= generic_count * 5

        ###################################################
        # Duplicate Words
        ###################################################

        lowered_words = []

        for word in words:

            lowered_words.append(

                word.lower()

            )

        if len(lowered_words) != len(set(lowered_words)):

            score -= 20

        ###################################################
        # Very Short Candidate
        ###################################################

        if len(candidate) < 3:

            score -= 100

        return score