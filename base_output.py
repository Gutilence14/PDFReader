from dataclasses import dataclass
from transformers.utils import ModelOutput
from typing import Optional, Tuple

@dataclass
class BasePdfOutput(ModelOutput):
    """
    base pdf output used in huggingface
    """
    Page: int = None
    Title: str = None
    Text: str = None
    Table: list = None
    Figure: list = None

@dataclass
class PdfOutput(ModelOutput):
    Pdf: Optional[Tuple[BasePdfOutput, ...]] = None


@dataclass
class BaseWordOutput(ModelOutput):
    """
    base pdf output used in huggingface
    """
    Page: int = None
    Title: str = None
    Text: str = None
    Table: list = None
    Figure: list = None

@dataclass
class WordOutput(ModelOutput):
    Word: Optional[Tuple[BaseWordOutput, ...]] = None