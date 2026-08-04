from src.nlp.topic_ranker import TopicRanker
from src.ai.llm_canonical_resolver import LLMCanonicalResolver


class CanonicalSelector:

    MIN_ACCEPTABLE_SCORE = 0

    @staticmethod
    def select(
        candidates,
        entities,
        caption=None
    ):
        if not candidates:

            print("[CanonicalSelector] No candidates found.")

            ####################################################
            # Still try the LLM using the caption
            ####################################################

            if caption:

                print("Sending caption to LLM...\n")

                llm_result = LLMCanonicalResolver.resolve(

                    caption,

                    []

                )

                print("\n============== LLM RESULT ==============")
                print(llm_result)
                print("========================================\n")

                if isinstance(llm_result, str):

                    print("[CanonicalSelector] Using LLM headline.\n")

                    return llm_result

            return None

        scored = []

        for candidate in candidates:

            score = TopicRanker.score(
                candidate,
                entities
            )

            scored.append(
                (
                    score,
                    candidate
                )
            )

        scored.sort(reverse=True)

        print("\n================ CANDIDATES ================")

        for score, candidate in scored[:10]:
            print(f"{score:>4} | {candidate}")

        print("============================================\n")

        best_score, best_candidate = scored[0]

        ####################################################
        # Try LLM FIRST
        ####################################################

        if caption:

            print("Sending caption to LLM...\n")

            # IMPORTANT:
            # Do NOT poison the LLM with keyword/entity candidates.
            # Let it understand the caption on its own.
            llm_result = LLMCanonicalResolver.resolve(
                caption,
                []
            )

            print("\n============== LLM RESULT ==============")
            print(llm_result)
            print("========================================\n")

            if isinstance(llm_result, str):

                print("[CanonicalSelector] Using LLM headline.\n")

                return llm_result

            if llm_result is False:

                print("[CanonicalSelector] LLM rejected caption.\n")

                return None

            print("[CanonicalSelector] LLM failed. Falling back.\n")

        ####################################################
        # Rule-based fallback
        ####################################################

        if best_score <= CanonicalSelector.MIN_ACCEPTABLE_SCORE:

            print("[CanonicalSelector] Best score too low.")

            return None

        print(f"[CanonicalSelector] FALLBACK -> {best_candidate}\n")

        return best_candidate