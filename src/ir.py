from gsearch import get_relevant_pages
from wiki import get_abstract


class IR():
    def __init__(self) -> None:
        pass

    def __call__(self, q: str, n: int = 1, summary_only: bool = True) -> list:
        return self.retrieve_from_web(q, n, summary_only=summary_only)

    def retrieve_from_web(
            self, q: str, n: int = 1,
            buf_size: int = 10,  # prefatch googlw search and cached to save search quota
            summary_only: bool = True) -> list:
        results = []
        links, summaries = get_relevant_pages(q=q, n=buf_size)
        for i, page in enumerate(links[:n]):
            if len(summaries[i]) > 0:
                results.append(summaries[i])
                if summary_only:
                    continue

            abstract = get_abstract(page)
            if len(abstract) > 0:
                results.append(abstract)
        return results
