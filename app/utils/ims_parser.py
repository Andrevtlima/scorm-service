import xml.etree.ElementTree as ET
from typing import Tuple


def parse_manifest(manifest_path: str) -> Tuple[str, list]:
    """Parse imsmanifest.xml returning course title and list of resource hrefs."""
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = {'ns': 'http://www.imsglobal.org/xsd/imscp_v1p1'}
    # title
    title_elem = root.find('.//{*}organization/{*}title')
    title = title_elem.text.strip() if title_elem is not None and title_elem.text else 'Untitled'
    resources = []
    for res in root.findall('.//{*}resource'):
        href = res.attrib.get('href')
        if href:
            resources.append(href)
    return title, resources
