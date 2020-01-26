import re
from itertools import compress


def get_members(document):
    is_matched = []
    for page in document:
        is_matched.append(any([re.match('prezes zarządu', sent, re.IGNORECASE) for sent in page]))
    candidate_pages = list(compress(document, is_matched))
    candidate_page = candidate_pages.pop()

    positions = ['Prezes Zarządu', 'Wiceprezes Zarządu', 'Członek Zarządu']
    position_indices = []
    for position in positions:
        try:
            position_indices.append(candidate_page.index(position))
        except ValueError as e:
            position_indices.append(None)
    members_indices = [i-1 for i in position_indices]

    date_search = [re.search(r'\d{4}\.\d{2}\.\d{2}', candidate_page[i]) for i in range(len(candidate_page))]
    date_search = [i.group() for i in date_search if i]
    if not date_search:
        date_search.append('')

    people = []
    for pos_index, mem_index in zip(position_indices, members_indices):
        if pos_index is None:
            pass
        people.append((date_search[0], candidate_page[mem_index], candidate_page[pos_index]))

    return str(people)
