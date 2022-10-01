from dataclasses import dataclass
import src.CommonOperations as cmnops

NOT_PROVIDED = "Not_Provided"


@dataclass
class BibDataFormat:
    Original_File_Name: str = NOT_PROVIDED
    Default_Key: str = NOT_PROVIDED
    Title: str = NOT_PROVIDED
    Journal: str = NOT_PROVIDED
    Volume: int = NOT_PROVIDED
    Pages: str = NOT_PROVIDED
    Year: int = NOT_PROVIDED
    ISSN: str = NOT_PROVIDED
    DOI: str = NOT_PROVIDED
    Hashed_DOI: str = NOT_PROVIDED
    URL: str = NOT_PROVIDED
    Author: list[str] = NOT_PROVIDED
    Keywords: list[str] = NOT_PROVIDED
    Abstract: str = NOT_PROVIDED


@dataclass
class TexDataFormat:
    Chapter_Number: int = NOT_PROVIDED
    Chapter_Name: str = NOT_PROVIDED
    Content: list[str | list[str]] = NOT_PROVIDED


@dataclass
class _JsonDataFormat:
    Index: int = "NOT PROIDED"
    Content: BibDataFormat | TexDataFormat = NOT_PROVIDED


@dataclass
class JsonDataFormat:
    JsonData: list[_JsonDataFormat]
