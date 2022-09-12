from dataclasses import asdict, dataclass, fields


@dataclass
class BibDataFormat:
    Default_Key: str = "NOT PROVIDED"
    Title: str = "NOT PROVIDED"
    Journal: str = "NOT PROVIDED"
    Volume: int = "NOT PROVIDED"
    Pages: str = "NOT PROVIDED"
    Year: int = "NOT PROVIDED"
    ISSN: str = "NOT PROVIDED"
    DOI: str = "NOT PROVIDED"
    Hashed_DOI: str = "NOT PROVIDED"
    URL: str = "NOT PROVIDED"
    Author: str = "NOT PROVIDED"
    Keywords: str = "NOT PROVIDED"
    Abstract: str = "NOT PROVIDED"


@dataclass
class TexDataFormat:
    Chapter_Number: int = "NOT PROVIDED"
    Chapter_Name: str = "NOT PROVIDED"
    Content: list[str] = "NOT PROVIDED"
