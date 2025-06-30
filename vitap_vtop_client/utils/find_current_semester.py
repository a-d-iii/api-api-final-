from bs4 import BeautifulSoup


def find_current_sem_sub_id(html: str) -> str | None:
    """Parse semesterSubId from a page containing a semester select."""
    soup = BeautifulSoup(html, 'html.parser')

    select = soup.find('select', attrs={"name": "semesterSubId"})
    if select:
        option = select.find("option", selected=True)
        if option and option.get("value"):
            value = option["value"].strip()
            if value:
                return value

        for opt in select.find_all("option"):
            value = opt.get("value", "").strip()
            if value:
                return value

    input_el = soup.find('input', attrs={'name': 'semesterSubId'})
    if input_el and input_el.get('value'):
        return input_el['value']
    return None

