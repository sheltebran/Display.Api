from fastapi import HTTPException
import httpx
import xml.etree.ElementTree as ET

async def fetch_external_data(external_url: str):
    """Calls an external URL and returns its content.

    Parameters
    ----------
    external_url : str
        The URL to fetch data from.

    Returns
    -------
    dict
        The content of the URL parsed as a dictionary.
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            response.raise_for_status()

            headlines_list = parse_items_from_rss(response.text)

            return headlines_list
        
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting {exc.request.url!r}.")
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    

def parse_xml(xml_string: str):
    """Parses an XML string into a dictionary.

    Parameters
    ----------
    xml_string : str
        The XML string to parse.

    Returns
    -------
    dict
        The parsed XML as a dictionary.
    """

    root = ET.fromstring(xml_string)

    xml_dict = {}

    for child in root:
        xml_dict[child.tag] = child.text
        for subchild in child:
            xml_dict[subchild.tag] = subchild.text

    return xml_dict if xml_dict else None


def parse_items_from_rss(xml_string: str):

    root = ET.fromstring(xml_string)

    items = []

    # Find all <item> elements
    for item in root.findall('./channel/item'):
        item_data = {}
        for elem in item:
            tag = elem.tag
            # Remove namespace from tag
            if '}' in tag:
                tag = tag.split('}', 1)[1]

            # If element has sub-elements (like media:content -> media:thumbnail)
            extract_subitems(item_data, elem, tag)

        items.append(item_data)

    return items if items else None


def extract_subitems(item_data, elem, tag):
    """Extracts subitems from an XML element and adds them to the item data.

    Parameters
    ----------
    item_data : dict
        The dictionary to store the extracted data.
    elem : xml.etree.ElementTree.Element
        The XML element to extract subitems from.
    tag : str
        The tag name of the current element.
    """ 
    
    if list(elem):
        subitems = {}
        for sub in elem:
            subtag = sub.tag
            if '}' in subtag:
                subtag = subtag.split('}', 1)[1]
            subitems[subtag] = sub.attrib
        item_data[tag] = {'attributes': elem.attrib, 'children': subitems}
    else:
        item_data[tag] = elem.text.strip() if elem.text else ''
