from collections import OrderedDict
import re


class CandidateGenerator:

    PERSON_EVENT_WORDS = {

        "marriage",
        "married",
        "wedding",
        "wins",
        "won",
        "joins",
        "joined",
        "launch",
        "launched",
        "released",
        "release",
        "beats",
        "beat",
        "championship",
        "world cup",
        "debut",
        "election",
        "death",
        "dies"

    }

    RELATIONSHIP_WORDS = {

        "marriage",
        "married",
        "wedding",
        "dating",
        "relationship",
        "engaged",
        "engagement",
        "divorce",
        "couple"

    }

    @staticmethod
    def clean(text: str):

        text = text.strip()

        text = re.sub(r"^[\[\(\"'`]+", "", text)

        text = re.sub(r"[\]\"'`)]+$", "", text)

        text = text.replace("’s", "")

        text = text.replace("'s", "")

        text = " ".join(text.split())

        return text

    # Legitimate single entities are almost never longer than this. A span
    # longer than this is very likely the entity extractor merging two or
    # more distinct entities into one (e.g. an org name + its abbreviation
    # + an unrelated person's name all stitched into one NER span). This
    # is a permanent structural rule, not a one-off patch -- candidate
    # generation should never blindly trust an entity span's length.
    MAX_ENTITY_WORDS = 4

    @staticmethod
    def _is_plausible_entity(entity_text):

        word_count = len(entity_text.split())

        if word_count == 0:

            return False

        if word_count > CandidateGenerator.MAX_ENTITY_WORDS:

            return False

        return True

    ####################################################
    # IMPROVEMENT 2 helper
    #
    # Decides whether two entities are allowed to be combined into a
    # single candidate. Instead of trusting proximity (same post) or a
    # global "was a relationship word mentioned anywhere" flag, this
    # requires the relationship word to appear *between the two entity
    # mentions* when raw post text is available, or attached to a keyword
    # that mentions both entities when it isn't.
    #
    # This deliberately does NOT use sentence segmentation or dependency
    # parsing -- Instagram captions don't segment reliably, so a simple
    # token-gap / co-mention check is the more robust signal here.
    ####################################################

    @staticmethod
    def _find_gap_text(ent1_text, ent2_text, post_text):

        if not post_text:

            return None

        lower_post = post_text.lower()

        i1 = lower_post.find(ent1_text.lower())

        i2 = lower_post.find(ent2_text.lower())

        if i1 == -1 or i2 == -1:

            return None

        if i1 < i2:

            start = i1 + len(ent1_text)

            end = i2

        else:

            start = i2 + len(ent2_text)

            end = i1

        if start >= end:

            return ""

        return lower_post[start:end]

    @staticmethod
    def _has_relationship_evidence(

        ent1_text,

        ent2_text,

        keywords,

        post_text="",

        max_gap_words=8

    ):

        gap = CandidateGenerator._find_gap_text(

            ent1_text,

            ent2_text,

            post_text

        )

        if gap is not None:

            if len(gap.split()) > max_gap_words:

                return False

            for word in CandidateGenerator.RELATIONSHIP_WORDS:

                if word in gap:

                    return True

            return False

        # No raw post text available -- fall back to requiring a keyword
        # that mentions BOTH entities together and contains a relationship
        # word. This is weaker than the gap check but still far stricter
        # than "any relationship word anywhere in the post".

        n1 = ent1_text.lower()

        n2 = ent2_text.lower()

        for keyword in keywords:

            lower = keyword.lower()

            if n1 in lower and n2 in lower:

                for word in CandidateGenerator.RELATIONSHIP_WORDS:

                    if word in lower:

                        return True

        return False

    ####################################################
    # IMPROVEMENT 1 helper
    #
    # A keyword-based candidate must be anchored to a real entity. If it
    # is anchored to MORE THAN ONE distinct entity with no event or
    # relationship word present, it's very likely an unrelated mash-up
    # (e.g. "royal challengers bangalore rcb drake",
    # "aanandita vagahani ria bhatia") rather than a genuine topic phrase.
    ####################################################

    @staticmethod
    def _keyword_entity_matches(

        keyword_text,

        persons,

        orgs,

        events,

        works,

        gpes,

        products

    ):

        matches = []

        kw_tokens = set(keyword_text.lower().split())

        for group in (persons, orgs, events, works, gpes, products):

            for ent_text in group:

                ent_tokens = set(ent_text.lower().split())

                if kw_tokens & ent_tokens:

                    matches.append(ent_text)

        return matches

    @staticmethod
    def generate(

        entities,

        keywords,

        post_text=""

    ):

        candidates = []

        persons = []

        orgs = []

        events = []

        works = []

        gpes = []

        products = []

        ####################################################

        # Separate entities

        ####################################################

        for entity in entities:

            text = CandidateGenerator.clean(

                entity[0]

            )

            label = entity[1]

            if not text:

                continue

            if not CandidateGenerator._is_plausible_entity(text):

                # Rejects implausibly long spans that are very likely
                # multiple entities merged into one by the extractor,
                # e.g. "Royal Challengers Bangalore RCB Drake".
                continue

            if label == "PERSON":

                persons.append(text)

            elif label == "ORG":

                orgs.append(text)

            elif label == "EVENT":

                events.append(text)

            elif label == "WORK_OF_ART":

                works.append(text)

            elif label in ("GPE", "LOC"):

                gpes.append(text)

            elif label == "PRODUCT":

                products.append(text)

        ####################################################
        # PERSON + EVENT
        ####################################################

        for person in persons:

            for keyword in keywords:

                lower = keyword.lower()

                for event in CandidateGenerator.PERSON_EVENT_WORDS:

                    if event in lower:

                        candidates.append(

                            f"{person} {event.title()}"

                        )

        ####################################################
        # PERSON + PERSON
        #
        # CHANGED: now checks relationship evidence per-pair instead of a
        # post-wide flag combined with an arbitrary persons[0] + persons[1]
        # pick. Iterates every pair; only combines pairs with actual
        # evidence linking them.
        ####################################################

        for i in range(len(persons)):

            for j in range(i + 1, len(persons)):

                p1 = persons[i]

                p2 = persons[j]

                if CandidateGenerator._has_relationship_evidence(

                    p1,

                    p2,

                    keywords,

                    post_text

                ):

                    candidates.append(

                        f"{p1} {p2}"

                    )

        ####################################################
        # Individual entities ONLY
        ####################################################

        candidates.extend(persons)

        candidates.extend(orgs)

        candidates.extend(events)

        candidates.extend(products)

        candidates.extend(works)

        candidates.extend(gpes)

        ####################################################
        # Keywords
        #
        # CHANGED: keyword candidates now require an entity anchor
        # (Improvement 1). If a keyword touches 2+ distinct entities with
        # no event/relationship word present, it's rejected (Improvement 2
        # applied to raw keyword phrases, not just explicit combinations).
        ####################################################

        BLOCKED_KEYWORDS = {

            "tweet",
            "tweets",
            "post",
            "posts",
            "photo",
            "photos",
            "picture",
            "pictures",
            "image",
            "images",
            "video",
            "videos"

        }

        for keyword in keywords:

            keyword = CandidateGenerator.clean(

                keyword

            )

            if not keyword:

                continue

            if len(keyword.split()) > 5:

                continue

            if keyword.lower() in BLOCKED_KEYWORDS:

                continue

            matched_entities = CandidateGenerator._keyword_entity_matches(

                keyword,

                persons,

                orgs,

                events,

                works,

                gpes,

                products

            )

            if not matched_entities:

                # No entity anchor at all -- e.g. "genz mindset",
                # "street interview", "short baddies". Reject.

                continue

            distinct_entities = set(

                m.lower() for m in matched_entities

            )

            if len(distinct_entities) >= 2:

                lower = keyword.lower()

                has_event_word = False

                for word in CandidateGenerator.PERSON_EVENT_WORDS | CandidateGenerator.RELATIONSHIP_WORDS:

                    if word in lower:

                        has_event_word = True

                        break

                if not has_event_word:

                    # Multiple unrelated entities glued into one phrase
                    # with no relationship signal. Reject.

                    continue

            candidates.append(

                keyword

            )

        ####################################################
        # Remove duplicates
        ####################################################

        cleaned = []

        seen = set()

        for candidate in candidates:

            candidate = CandidateGenerator.clean(

                candidate

            )

            if not candidate:

                continue

            key = candidate.lower()

            if key in seen:

                continue

            seen.add(

                key

            )

            cleaned.append(

                candidate

            )

        return cleaned