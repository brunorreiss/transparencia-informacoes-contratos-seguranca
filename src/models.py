from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Union


class Orgao(str, Enum):
    tipo_30 = 'FUNDO MUNICIPAL DE POLITICAS SOBRE DROGAS'
    tipo_39 = 'GUARDA MUNICIPAL DE FORTALEZA'
    tipo_63 = 'SECRETARIA MUNICIPAL DA SEGURANCA CIDADA'
    tipo_33 = 'FUNDO MUNICIPAL DE SEGURANCA CIDADA'


class ResponseSite(BaseModel):
    ID: Optional[Union[int, str]] = ''
    ANOCONTRATO: Optional[Union[int, str]] = ''
    NUMEROCONTRATOSISTEMA: Optional[Union[int, str]] = ''
    NUMEROCONTRATOINSTITUICAO: Optional[Union[int, str]] = ''
    CONTRATADO: Optional[Union[int, str]] = ''
    OBJETOCONTRATO: Optional[Union[int, str]] = ''
    IDUO: Optional[Union[int, str]] = ''
    DESCRICAOUO: Optional[Union[int, str]] = ''
    VALORCONTRATO: Optional[float] = 0.0
    IDCONTRATO: Optional[Union[int, str]] = ''
    ANEXOS: Optional[Union[int, str]] = ''
    QTDADITIVOS: Optional[Union[int, str]] = ''
    CODIGOCOMPLETOUO: Optional[Union[int, str]] = ''
    MODALIDADEPROCESSO: Optional[Union[int, str]] = ''
    MODALIDADEAPLICACAO: Optional[Union[int, str]] = ''
    IDCONTRATOORIGEM: Optional[Union[int, str]] = ''

class ResponseDefault(BaseModel):
    code: int
    message: str
    datetime: str
    results: List[ResponseSite]

class ResponseError(BaseModel):
    code: int
    message: str