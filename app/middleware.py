from fastapi import Request, Response

from app.utils.logger import logger


async def log_middleware(request: Request, call_next):

    response = await call_next(request)

    # if response.status_code>=400 :
        # return response

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    
    log_response = f"{request.method} - {request.url.path} - [RESPONSE]\n{response_body.decode("utf-8")}"

    logger.info(log_response)

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
