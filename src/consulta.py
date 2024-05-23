# Importando libs
# stdlib imports
from os import environ as env
from datetime import datetime

# 3rd party imports
import aiohttp
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi import status

# Local imports
from src.models import *
from utils.util import get_headers

# Captura variáveis de ambiente e cria constantes
TIMEOUT = env.get('TIMEOUT', default=180)

#-----------------------------------------------------------------------------------------------------
async def fetch(ano: int, orgao: str ):
    if not ano or not orgao:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"code": 422, "message": "Unprocessable Entity",
                     "datetime": datetime.now().isoformat()}
        )

    orgao_dict = {
        'FUNDO MUNICIPAL DE POLITICAS SOBRE DROGAS': 11902,
        'GUARDA MUNICIPAL DE FORTALEZA': 17102,
        'SECRETARIA MUNICIPAL DA SEGURANCA CIDADA': 17101,
        'FUNDO MUNICIPAL DE SEGURANCA CIDADA': 17901,
    }

    if orgao in orgao_dict:
        orgao = orgao_dict[orgao]
    else:
        return JSONResponse(
            status_code=status.HTTP_513_REQUEST_HEADER_FIELDS_TOO_LARGE,
            content={"code": 513, "message": "Argumentos invalidos", 
                     "datetime": datetime.now().isoformat()}
        )
    
    logger.info(f"Consulta: {ano} - {orgao}")
    
    # Configura os timeouts
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    session = aiohttp.ClientSession(timeout=timeout)
    
    # Configurando headers
    session.headers.update(get_headers())
    
    session.headers.update({'Referer': 'https://portaltransparencia.fortaleza.ce.gov.br'})
    
    
    try:
        url = f'https://portaltransparencia-back.sepog.fortaleza.ce.gov.br/api/contratos/{ano}?orgao={orgao}'
        async with session.get(url, ssl=False, allow_redirects=True) as resp:
            logger.debug(f"Consulta: {resp.status} - {url}")
            response_data = await resp.json()
            
            if not response_data:
                result = ResponseDefault(
                    code=0,
                    message='Nenhum contrato encontrado para o ano e orgao informados.',
                    results=[],
                    datetime=str(datetime.now()),
                )
            else:
                results = [ResponseSite(**item) for item in response_data]  # Cria uma lista de ResponseSite
                result = ResponseDefault(
                    code=0,
                    message='Contratos encontrados com sucesso.',
                    results=results,
                    datetime=str(datetime.now()),
                )

    except aiohttp.ClientError as e:
        logger.exception('Erro durante a consulta API')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'code': 500,
                'message': f'INTERNAL_SERVER_ERROR: {str(e)}'
            }
        )
    except Exception as e:
        logger.exception('Erro inesperado durante a consulta API')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'code': 500,
                'message': f'INTERNAL_SERVER_ERROR: {str(e)}'
            }
        )

    logger.info(f"Consulta finalizada: {result}")
    await session.close()
    return result
